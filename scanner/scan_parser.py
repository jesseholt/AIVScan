#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       scan_parser.py
#       
#       Copyright 2012 Team Pwn Stars
#       
#       
#       

import MySQLdb
from lib import Parser
import script_parser

#import local_settings.py for database creds
import os, sys
settings_path = os.path.abspath('../www/aivs')
sys.path.append(settings_path)
import local_settings


class cQueueItem:
	
    def __init__(self, qId, userId, ip_address, subscription_level, scan_options, scan_running):
        self.qId = qId
        self.userId = userId
        self.ip_address = ip_address
        self.subscription_level = subscription_level
        self.scan_options = scan_options
        self.scan_running = scan_running
        
class cSQLImporter:
	p = None
	dbconn = None
	username = local_settings.DATABASES['default']['USER']
	password = local_settings.DATABASES['default']['PASSWORD']
	dbhost = local_settings.DATABASES['default']['HOST']
	dbname = local_settings.DATABASES['default']['NAME']
	XMLfilename = ''
	userId = 0

	def __init__(self, XMLfilename, userId):
		self.XMLfilename = XMLfilename
		self.userId = userId

	def process(self):
		try:
			scanid = 0
			hostid = 0
			
			print "initializing parser..."
			self.p = Parser.Parser(self.XMLfilename)
			
			#session (scan) informaiton 
			print "parsing scan information..."
			session = self.p.get_session()
			
			if (session is None):
				raise SessionError('Unable to read scan session')
			SQL = "call pInsertScan(" \
					+ str(self.userId) + ", " \
					+ "'" + session.nmap_version + "', " \
					+ "'" + session.scan_args + "', " \
					+ "'" + session.start_time + "', " \
					+ "'" + session.finish_time + "')"
			dbconn = MySQLdb.connect(host=self.dbhost, user=self.username, \
									passwd=self.password, db=self.dbname)
			cursor = dbconn.cursor()
			#import pdb; pdb.set_trace()
			cursor.callproc("pInsertScan", (self.userId, \
											session.nmap_version, \
											session.scan_args, \
											session.start_time, \
											session.finish_time))
			#cursor.execute(SQL)
			result = cursor.fetchone()
			scanid = result[0]
			#scanid = cursor.lastrowid
			#scanid=db.insert_id()
			print "** scanid: " + str(scanid)	
			cursor.close()
					
			#parse hosts
			for h in self.p.all_hosts():
				try:
					print "parsing host " + h.ipv4 + "..."
					cursor = dbconn.cursor()
					cursor.callproc("pInsertHost", (scanid, \
													h.ipv4, \
													h.hostname, \
													h.status, \
													h.macaddr, \
													h.vendor, \
													h.ipv6, \
													h.distance, \
													h.uptime, \
													h.lastboot))
					result = cursor.fetchone()
					hostid = result[0]
					print "** hostid: " + str(hostid)
					#cursor.execute(SQL)
					#hostid = cursor.lastrowid
					#hostid = db.insert_id()				
					cursor.close()
					
					#parse OS
					for OS_node in h.get_OS():
						SQL = "CALL pInsertOS(" \
								+ str(hostid) + ", " \
								+ "'" + OS_node.name + "', " \
								+ "'" + OS_node.family + "', " \
								+ "'" + OS_node.generation + "', " \
								+ "'" + OS_node.os_type + "', " \
								+ "'" + OS_node.vendor + "', " \
								+ str(OS_node.accuracy) + ")" 

						cursor = dbconn.cursor()
						cursor.execute(SQL)
						cursor.close()
										
					#parse tcp ports
					print "number of open tcp ports: " + str(len(h.get_ports('tcp', 'open')))

					for port in h.get_ports('tcp', 'open'):
						SQL = "CALL pInsertPort(" \
								+ str(hostid) + ", " \
								+ str(port) + ", "
						service = h.get_service('tcp', port)
						if not (service is None):
							SQL += "'open', " \
									+ "'" + service.name + "', " \
									+ "'" + service.product + "', " \
									+ "'" + service.version + "', " \
									+ "'" + service.fingerprint + "', " \
									+ "'tcp')"
						else:
							SQL += "'open', '', '', '', '', 'tcp')"
						
						cursor = dbconn.cursor()
						cursor.execute(SQL)
						cursor.close()						
			
					#parse udp ports
					print "number of open udp ports: " + str(len(h.get_ports('udp', 'open')))
					for port in h.get_ports('udp', 'open'):
						SQL = "CALL pInsertPort(" \
								+ str(hostid) + ", " \
								+ str(port) + ", "
						service = h.get_service('udp', port)
						if not (service is None):
							SQL += "'open', " \
									+ "'" + service.name + "', " \
									+ "'" + service.product + "', " \
									+ "'" + service.version + "', " \
									+ "'" + service.fingerprint + "', " \
									+ "'udp')"
						else:
							SQL += "'open', '', '', '', '', 'udp')"
						
						cursor = dbconn.cursor()
						cursor.execute(SQL)
						cursor.close()	
						
					#parse script output
					try:
						#import pdb; pdb.set_trace()
						sp = script_parser.cScriptParser()
						#print "getting script contents"
						for scr in h.get_scripts():
							#print "matching output"
							#import pdb; pdb.set_trace()
							vulnId = sp.parseOutput(scr.scriptId, scr.output)
							if vulnId > 0:
								print "vuln id: " + str(vulnId)
								cursor = dbconn.cursor()
								cursor.callproc("pInsertVuln", (hostid, vulnId))
								result = cursor.fetchone()
								cursor.close()
					except:
						print "Error parsing script output"
						e = sys.exc_info()[0]
						print str(e)
				except:
					print "Error parsing host information."
					
			dbconn.close()	
			return 0
		except IOError as ioE:
			print "Error processing file: {1}".format(ioE.strerror)
		except:
			print "Error processing file."
			return 1





if __name__ == '__main__':
	
	#import pdb; pdb.set_trace()


	cp = cSQLImporter('/tmp/test_pwn01.xml', 1001)
	cp.process()



