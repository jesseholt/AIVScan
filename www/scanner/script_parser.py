#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#
#       Copyright 2012 Team Pwn Stars
#

import MySQLdb
import logging
import sys, os

#import local_settings.py for database creds
import os, sys
settings_path = os.path.abspath('../www/aivs')
sys.path.append(settings_path)
import local_settings

class cScriptParser:

    dbconn = None
    username = local_settings.DATABASES['default']['USER']
    password = local_settings.DATABASES['default']['PASSWORD']
    dbhost = local_settings.DATABASES['default']['HOST']
    dbname = local_settings.DATABASES['default']['NAME']

    def __init__(self):
        self.dbconn = None

    #returns vulnId if matched, 0 if not matched
    def parseOutput(self, scriptID, sOutput):
        try:
            #init DB connection
            dbconn = MySQLdb.connect(host=self.dbhost, user=self.username, \
                        passwd=self.password, db=self.dbname)
            cursor = dbconn.cursor()

            cursor.callproc("pGetTextVulnRef_byScriptID", ([scriptID]))

            rows = cursor.fetchall()
            for row in rows:
                MatchString = row[2] #match string
                vulnId = row[0]
                if MatchString in sOutput:
                    #print "found match: " + MatchString    + " for tvid: " + str(vulnId)
                    cursor.close()
                    return vulnId
                    break

        except:
            e = sys.exc_info()[0]
            logging.error('Error parsing script output: %s',  str(e))
            return 0

        return 0


if __name__ == '__main__':

    scriptID = 'smb-check-vulns'
    sOutput = 'bla bla MS08-067: VULNERABLE bla bla'

    sp = cScriptParser()
    sp.parseOutput(scriptID, sOutput)

