#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       scan_parser.py
#       
#       Copyright 2012 Ketchup <ketchup@fluffybunny>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       
#       

import MySQLdb
from lib import Parser

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
	db = None
	username = ''
	password = ''
	dbhost = ''
	dbname = ''
	XMLfilename = ''
	userId = 0

	def __init__(self, username, password, dbhost, dbname, XMLfilename, userId):
		self.username = username
		self.password = password
		self.dbhost = dbhost
		self.dbnmae = dbname
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
			db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
			cursor = db.cursor()
			cursor.execute(SQL)
			scanid = cursor.lastrowid
			cursor.close()
					
			#parse hosts
			for h in self.p.all_hosts():
				try:
					print "parsing host " + h.ipv4 + "..."
					SQL = "CALL pInsertHost(" \
							+ str(scanid) + ", " \
							+ "'" + h.ipv4 + "', " \
							+ "'" + h.hostname + "', " \
							+ "'" + h.status + "', " \
							+ "'" + h.macaddr + "', " \
							+ "'" + h.vendor + "', " \
							+ "'" + h.ipv6 + "', " \
							+ str(h.distance) + ", " \
							+ "'" + h.uptime + "', " \
							+ "'" + h.lastboot + "')"
							
					cursor = db.cursor()
					cursor.execute(SQL)
					hostid = cursor.lastrowid
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

						cursor = db.cursor()
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
						
						cursor = db.cursor()
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
						
						cursor = db.cursor()
						cursor.execute(SQL)
						cursor.close()	
				except:
					print "Error parsing host information."
					
			db.close()	
			return 0
		except IOError as ioE:
			print "Error processing file: {1}".format(ioE.strerror)
		except:
			print "Error processing file."
			return 1





if __name__ == '__main__':
	
	username = 'aivscan'
	password = 'Fish dont fry in the kitchen.'
	dbhost = 'localhost'
	dbname = 'queue'

	cp = cSQLImporter(username, password, dbhost, dbname, 'test.xml', 1001)
	cp.process()



