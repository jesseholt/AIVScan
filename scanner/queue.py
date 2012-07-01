#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       queue.py
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

class cQueueItem:
	
    def __init__(self, qId, userId, ip_address, subscription_level, scan_options, scan_running):
        self.qId = qId
        self.userId = userId
        self.ip_address = ip_address
        self.subscription_level = subscription_level
        self.scan_options = scan_options
        self.scan_running = scan_running
        
class cQueue:
	
	iRunningScans = 0
		
	def __init__(self, username, password, dbhost, dbname, max_scans):
		self.username = username
		self.password = password
		self.dbhost = dbhost
		self.dbname = dbname
		self.max_scans = max_scans
		
		#set the initial value for iRunningScans from the DB
		try:
			db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
			cursor = db.cursor()
			cursor.execute("SELECT * FROM queue_list WHERE scan_running = 1")
			self.iRunningScans = int(cursor.rowcount)
			print "Initialized queue with ", self.max_scans, " maximum running scans."
			print "Currently ", self.iRunningScans, " scan are in progress."
		except:
			print "Unable to determine number of running scans."
	
	def getNext(self):
		try:
			if (self.iRunningScans < self.max_scans):
				db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
				cursor = db.cursor()
				cursor.execute("SELECT * FROM queue_list ORDER BY qId LIMIT 1")
				for row in cursor.fetchall():
					qi = cQueueItem(row[0], row[1], row[2], row[3], row[4], row[5])
					break
				
				updateSQL = "UPDATE queue_list " \
							"SET scan_running = 1 " \
							"WHERE qId = " + str(qi.qId)
				cursor.close()
				cursor = db.cursor()
				cursor.execute(updateSQL)
				self.iRunningScans += 1
				cursor.close()
				db.close()
				return qi
			else:
				raise TooManyScanError(max_scans)
		except:
			if (self.iRunningScans >= self.max_scans):
				print "Error: unable to retrieve the next queue item.\n" \
						"\tToo many active scans"
			else:
				print "Error: unable to retrieve the next queue item.\n" \
						"\tUnknown error."
	
	def insertQueueItem(self, userId, ip_address, subscription_level, scan_options, scan_running):
		try:
			db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
			cursor = db.cursor()
			SQLStatement = "INSERT INTO queue_list (userId, ip_address, " \
								"subscription_level, scan_options, scan_running) values (" + \
								str(userId) + ",'" + str(ip_address) +  "'," + str(subscription_level) + \
								",'" + str(scan_options) + "'," + str(scan_running) + ")"
			cursor.execute(SQLStatement)
			cursor.close()
			db.close()
			return 0
		except:
			print "Error inserting new queue item."
			return 1
			
	def deleteQueueItem(self, qId):
		try:
			db = MySQLdb.connect(host=dbhost, user=username, passwd=password, db=dbname)
			cursor = db.cursor()
			SQLStatement = "DELETE FROM queue_list WHERE scan_running = 1" \
							" AND qId = " + str(qId)
			cursor.execute(SQLStatement)
			self.iRunningScans -= 1
			cursor.close()
			db.close()			
			return 0
		except:
			print "Error removing queue item."
			return 1
		
	
	



if __name__ == '__main__':
	
	username = 'aivscan'
	password = 'Fish dont fry in the kitchen.'
	dbhost = 'localhost'
	dbname = 'queue'

	#create a Queue object
	q = cQueue(username, password, dbhost, dbname, 10)
	
	#insert some queue items, just to test
	q.insertQueueItem(1001, "192.168.0.55", 1, "-sV -sT -P0 -O", 0)
	q.insertQueueItem(1002, "192.168.0.56", 2, "-sV -sT -P0 -O", 0)
	q.insertQueueItem(1003, "192.168.0.57", 1, "-sV -sT -P0 -O", 0)
	
	#get the next queue item (from the top) 
	qi = q.getNext()
	if qi is None:
		print "Failed to retrieve queue item."
	else:
		print "Retrieved queue item..."
		print "queue id: \t", qi.qId
		print "user id: \t", qi.userId
		print "ip address: \t", qi.ip_address
		print "subscription: \t", qi.subscription_level
		print "scan options: \t", qi.scan_options
		print "scan running: \t", qi.scan_running
	
		print "deleting queue item id ", qi.qId, "..."
		q.deleteQueueItem(qi.qId) #takes qId as the parameter


