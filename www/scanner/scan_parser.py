# -*- coding: utf-8 -*-
# Copyright 2012 Team Pwn Stars

import os, sys
import logging
import datetime

from scanner.lib import Parser
from scanner.script_parser import NmapScriptParser
from scanner.models import *

class SessionError(Exception):
    pass

class ScanImporter:

    def __init__(self, xml_results, scan_id, user_id):
        self.xml_results = xml_results
        self.scan_id = scan_id
        self.user_id = user_id

    def process(self):
        try:
            logging.debug('parsing scan results...')
            self.results = Parser.Parser(self.xml_results)
            session = self.results.get_session()
            if session is None:
                raise SessionError('Unable to read scan session')

            ''' taken from the original pInsertScan sproc:
            CREATE PROCEDURE pInsertScan(IN v_userid INT, IN v_version TEXT, IN v_args TEXT,
               IN v_startstr TEXT, IN v_endstr TEXT)
            BEGIN
            INSERT INTO scans (userId, version, args, startstr, endstr)
            values ( v_userid, v_version, v_args, v_startstr, v_endstr );
            SELECT @@identity;
            END '''
            logging.debug('building scan object')
            try:
                scan = Scan.objects.get(pk=self.scan_id)
            except Scan.DoesNotExist:
                scan = Scan()
            scan.user = User.objects.get(pk=int(self.user_id))
            scan.nmap_version = session.nmap_version
            scan.nmap_args = session.scan_args
            scan.end_time = datetime.datetime.strptime(session.finish_time, '%a %b %d %H:%M:%S %Y')
            scan.save()
            logging.debug('scanid is {0}'.format(scan.pk))

            # save host information
            for h in self.results.all_hosts():
                try:
                    ''' taken from the original pInsertHost sproc:
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
                    host = Host()
                    host.scan = scan
                    host.ip4 = h.ipv4
                    host.hostname = h.hostname
                    host.status = h.status
                    host.mac = h.macaddr
                    # host.ip6 = h.ipv6
                    host.distance = h.distance
                    host.uptime = h.uptime
                    host.last_boot = h.lastboot
                    host.save()
                    logging.debug('hostid is {0}'.format(host.pk))

                    for os_node in h.get_OS():
                        ''' taken from the original pInsertOS sproc:
                        CREATE PROCEDURE pInsertOS (IN v_hid INT, IN v_name TEXT, IN v_family TEXT,
                            IN v_generation TEXT, IN v_type TEXT, IN v_vendor TEXT, IN v_accuracy INT)
                        BEGIN
                        INSERT INTO os (hid, name, family, generation, type, vendor, accuracy)
                        VALUES ( v_hid, v_name, v_family, v_generation, v_type, v_vendor, v_accuracy);
                        END '''
                        os = OperatingSystem()
                        os.name = os_node.name
                        os.family = os_node.family
                        os.generation = os_node.generation
                        os.os_type = os_node.os_type
                        os.vendor = os_node.vendor
                        os.save()
                        host.operating_system = os
                        host.save()

                    # parse TCP and UDP ports
                    self.parse_ports(h, host, proto='tcp')
                    self.parse_ports(h, host, proto='udp')

                    #parse script output
                    try:
                        nsp = NmapScriptParser()
                        for scr in h.get_scripts():
                            vulnId = nsp.parse_output(scr.scriptId, scr.output, host.pk)
                    except Exception as ex:
                        logging.error('Error parsing script output:\n{0}'.format(ex))

                except Exception as ex:
                    logging.error('Error parsing host information.\n{0}'.format(ex))

            scan.state = Scan.COMPLETE
            scan.save()

            from scanner.tasks import send_scan_report # importing here prevents a circular reference
            send_scan_report.delay(scan.pk)

        except Exception as ex:
            logging.error('Error processing results:\n{0}'.format(ex))


    def parse_ports(self, h, host, proto='tcp'):
        '''
        taken from the original pInsertPort sproc:
        CREATE PROCEDURE pInsertPort (IN v_hid INT, IN v_port INT, IN v_state TEXT, IN v_name TEXT,
           IN v_product TEXT, IN v_version TEXT, IN v_fingerprint TEXT, IN v_proto TEXT)
        BEGIN
        INSERT INTO ports (hid, port, state, name, product, version, fingerprint, proto )
        VALUES (v_hid, v_port, v_state, v_name, v_product, v_version, v_fingerprint, v_proto);
        END '''
        logging.debug('number of open {0} ports {1}'.format(proto.upper(),
                                                            len(h.get_ports(proto, 'open'))))
        for p in h.get_ports(proto, 'open'):
            try:
                known_port = KnownPort.objects.get(protocol=proto, port_number=int(p))
            except KnownPort.DoesNotExist:
                known_port = KnownPort()
                known_port.protocol = proto
                known_port.port_number = int(p)
                known_port.risk_level = 3
                known_port.description = 'This port is not in our database'
                known_port.mitigation = 'This port is not in our database'
                known_port.save()

            port = FoundPort()
            port.host = host
            port.state = FoundPort.OPEN
            port.known_port = known_port
            service = h.get_service(proto, p)
            if service:
                port.service_name = service.name
                port.product = service.product
                port.version = service.version
                port.fingerprint = service.fingerprint
                port.save()




