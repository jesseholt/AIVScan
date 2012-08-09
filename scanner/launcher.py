#!/usr/bin/python
#
# --------------------------------------------------------------------------------
# launcher.py - Used to launch an nmap scan as part of the AIVScan system
#
#    USAGE:
#        launcher.py [IPAddress] [UserID] [SubscriptionLevel]
#
# --------------------------------------------------------------------------------

import sys
import subprocess
import os
import socket
import scan_parser
from time import gmtime, strftime

settings_path = os.path.abspath('../www/aivs')
sys.path.append(settings_path)
import local_settings


def launchParser(inputXML, UserID):
    try:
        cp = scan_parser.cSQLImporter(inputXML, UserID)
        cp.process()
    except IOError as ioE:
        print "Error parsing file: {1}".format(ioE.strerror)
    except Exception as ex:
        print "Error parsing file.\n{0}".format(ex)
        return 1

def launchScan(ipAddr, userID, subscriptionLevel):

    try:

        # get the current date & time to append to files
        sNow = strftime("%Y%m%d_%H%M%S", gmtime())

        #get log directory from the local_settings.py file
        sLogDir = local_settings.LOG_DIRECTORY

        # Declare the files to write to from STDERR and STDOUT
        sErrorFile = sLogDir + "/nmaperror." + str(userID) + "_" + sNow + ".txt"
        fError = open(sErrorFile, 'w')
        sOutFile = sLogDir + "/nmapout." + str(userID) + "_" + sNow + ".txt"
        fOut = open(sOutFile, 'w')

        # Initialize the scan variables to pass to the subprocess call
        command = "nmap"
        args1 = "-sT"
        args2 = "-sV"
        args3 = "-P0"
        args4 = "-oX"
        scr1 = "--script"
        scr2 = "smb-check-vulns,vuln,exploit"
        xmlOut = sLogDir + "/nmapxmlout_" + userID + "_" + sNow + ".xml" # Declare the XML output file that will be used by the parser
        # for the above we need to insert a date+time string into the file.  there could be multiple scans for a user
        # Launch the nmap scan with the supplied parameters
        iReturn = subprocess.call([command, args1, args2, args3, args4, xmlOut, scr1, scr2, ipAddr], stderr=fError, stdout=fOut)


        if os.path.exists(sOutFile):
                fOut = open(sOutFile, 'r')
        if os.path.exists(sErrorFile):
                fError = open(sErrorFile, 'r')

        # Initialize variables to read STDERR and STDIN
        sOuput = ''
        sError = ''
        if not fOut is None:
            sOutput = fOut.read()
        if not fError is None:
            sError = fError.read()

        if not fOut is None:
            fOut.close()
        if not fError is None:
            fError.close()
    except Exception, ex:
        print "Error launching the scan.\n{0}".format(ex)
        return 1

    try:
        launchParser(xmlOut, subscriptionLevel)
    except:
        print "Error parsing the XML scan results."
        return 1

    return 0

def printUsage():
    print "AIVScan Launcher version 0.1"
    print "\n"
    print "Usage: "
    print sys.argv[0] + " <IP address>" + " <userID>" + " <subscription level>\n\n"

def verifyIP(IPAddress):

    if (IPAddress is None) or (IPAddress == ""):
        return False

    argLength = len(IPAddress.split("."))

    if argLength == 4:
        try:
            socket.inet_aton(IPAddress)
            return True
        except:
            return False
    else:
        return False

    return False

def main():

    # Read command line parameters
    if len(sys.argv) == 4:
        ipAddr = sys.argv[1]
        userID = sys.argv[2]
        subLevel = sys.argv[3]
    else:
        printUsage()
        return 1

    if verifyIP(ipAddr):
        # Launch the nmap scan with the supplied parameters
        if (launchScan(ipAddr, userID, subLevel) == 0):
            return 0
        else:
            return 1
    else:
        print "Error: Invalid IP Address"
        return 1

    return 0

if __name__ == '__main__':
    main()
