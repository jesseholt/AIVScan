#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2012 Team Pwn Stars

import os, sys
import logging
from django.conf.settings import settings

from scanner.lib import Parser
import scanner.script_parser
from scanner.models import *


class cSQLImporter:

	def __init__(self, xml_results, user_id):
		self.xml_results = xml_results
		self.user_id = user_id

	def process(self):
		try:
            logging.debug('parsing scan results...')
			self.results = Parser.Parser(self.xml_results)
			session = self.results.get_session()
			if session is None:
				raise SessionError('Unable to read scan session')

            ''' taken from pInsertScan sproc:
            CREATE PROCEDURE pInsertScan(IN v_userid INT, IN v_version TEXT, IN v_args TEXT,
                 IN v_startstr TEXT, IN v_endstr TEXT)
            BEGIN
            INSERT INTO scans (userId, version, args, startstr, endstr)
                        values ( v_userid, v_version, v_args, v_startstr, v_endstr );
            SELECT @@identity;
            END'''
            logging.debug('building scan object')
            scan = Scans()
            scan.userid = User.objects.get(pk=int(user_id))
            scan.subscription_level = 0
            scan.version = session.nmap_version
            scan.args = session.scan_args
            scan.starttime = session.start_time
            scan.endtime = session.finish_time
            scan.save()
            logging.debug('scanid is {0}'.format(scan.id))

            # save host information
            for h in self.results.all_hosts():
                try:
                    ''' taken from pInsertHost sproc:
                    CREATE PROCEDURE pInsertHost(, IN v_sid INT, IN v_ip4 TEXT, IN v_hostname TEXT,
                        IN v_status TEXT, IN v_mac TEXT, IN v_vendor TEXT, IN v_ip6 TEXT, IN v_distance INT,
                        IN v_uptime TEXT, IN v_upstr TEXT)
                    BEGIN
                    INSERT INTO hosts ( sid, ip4, hostname, status, mac, vendor, ip6, distance, uptime,
                    upstr) VALUES ( v_sid, v_ip4, v_hostname, v_status, v_mac, v_vendor, v_ip6, v_distance,
                    v_uptime, v_upstr);
                    SELECT @@identity;
                    END '''
                    logging.debug('parsing host {0}'.format(h.ipv4))
                    host = Hosts()
                    host.sid = scan
                    host.ip4 = h.ipv4
                    host.hostname = h.hostname
                    host.status = h.status
                    host.mac = h.macaddr
                    host.ip6 = h.ipv6
                    host.distance = h.distance
                    host.uptime = h.uptime
                    host.upstr = h.lastboot
                    host.save()
                    logging.debug('hostid is {0}'.format(host.id))

                    for os_node in h.get_OS():
                        ''' taken from pInsertOS sproc:
                        CREATE PROCEDURE pInsertOS (IN v_hid INT, IN v_name TEXT, IN v_family TEXT,
                            IN v_generation TEXT, IN v_type TEXT, IN v_vendor TEXT, IN v_accuracy INT)
                        BEGIN
                        INSERT INTO os (hid, name, family, generation, type, vendor, accuracy)
                        VALUES ( v_hid, v_name, v_family, v_generation, v_type, v_vendor, v_accuracy);
                        END '''
                        os = Os()
                        os.hid = host
                        os.name = os_node.name
                        os.family = os_node.family
                        os.generation = os_node.generation
                        os.os_type = os_node.os_type
                        os.vendor = os_node.vendor

					#parse TCP ports
					logging.debug('number of open TCP ports: %s', str(len(h.get_ports('tcp', 'open'))))
					for port in h.get_ports('tcp', 'open'):
                        ''' taken from pInsertPort sproc:
                        CREATE PROCEDURE pInsertPort (IN v_hid INT, IN v_port INT, IN v_state TEXT,
                            IN v_name TEXT, IN v_product TEXT, IN v_version TEXT, IN v_fingerprint TEXT,
                            IN v_proto TEXT)
                        BEGIN
                        INSERT INTO ports (hid, port, state, name, product, version, fingerprint, proto )
                        VALUES (v_hid, v_port, v_state, v_name, v_product, v_version, v_fingerprint, v_proto);
                        END '''
                        service = h.get_service('tcp', port)
                        tcp_port = Ports()
                        tcp_port.state = 'open'
                        tcp_port.proto = 'tcp'
                        if service:
                            tcp_port.name = service.name
                            tcp_port.product = service.product
                            tcp_port.version = service.version
                            tcp_port.fingerprint = service.fingerprint
                        tcp_port.save()

                    # parse UDP ports
					logging.debug('number of open UDP ports: %s', str(len(h.get_ports('udp', 'open'))))
					for port in h.get_ports('udp', 'open'):
                        ''' taken from pInsertPort sproc:
                        CREATE PROCEDURE pInsertPort (IN v_hid INT, IN v_port INT, IN v_state TEXT,
                            IN v_name TEXT, IN v_product TEXT, IN v_version TEXT, IN v_fingerprint TEXT,
                            IN v_proto TEXT)
                        BEGIN
                        INSERT INTO ports (hid, port, state, name, product, version, fingerprint, proto )
                        VALUES (v_hid, v_port, v_state, v_name, v_product, v_version, v_fingerprint, v_proto);
                        END '''
                        service = h.get_service('udp', port)
                        udp_port = Ports()
                        udp_port.state = 'open'
                        udp_port.proto = 'udp'
                        if service:
                            udp_port.name = service.name
                            udp_port.product = service.product
                            udp_port.version = service.version
                            udp_port.fingerprint = service.fingerprint
                        udp_port.save()

					#parse script output
					try:
						nsp = script_parser.NmapScriptParser()
						for scr in h.get_scripts():
							vulnId = nsp.parse_output(scr.scriptId, scr.output, host.id)
					except Exception as ex:
						logging.error('Error parsing script output:\n{0}'.format(ex))

                except Exception as ex:
					logging.error('Error parsing host information.\n{0}'.format(ex))

		except Exception as ex:
			logging.error('Error processing results:\n{0}'.format(ex))

if __name__ == '__main__':
	cp = cSQLImporter('/tmp/test_pwn01.xml', 1001)
	cp.process()



