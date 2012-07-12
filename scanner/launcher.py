#!/usr/bin/python
#
# --------------------------------------------------------------------------------
# launcher.py - Used to launch an nmap scan as part of the AIVScan system
#
#	USAGE:
#		launcher.py [IPAddress] [UserID] [SubscriptionLevel]
#
# --------------------------------------------------------------------------------

import sys
import subprocess
import os
import scan_parser


def launchParser(inputXML, UserID):
	try:
		cp = scan_parser.cSQLImporter(inputXML, UserID)
		cp.process()
	except IOError as ioE:
		print "Error parsing file: {1}".format(ioE.strerror)
	except:
		print "Error parsing file."
		return 1

def launchScan(ipAddr, userID, subscriptionLevel):
	
	try:

		# Declare the files to write to from STDERR and STDOUT
		sErrorFile = "/tmp/nmaperror." + str(userID) + ".txt"
		fError = open(sErrorFile, 'w')
		sOutFile = "/tmp/nmapout." + str(userID) + ".txt"
		fOut = open(sOutFile, 'w')

		# Initialize the scan variables to pass to the subprocess call
		command = "nmap"
		args1 = "-sT"
		args2 = "-sV"
		args3 = "-P0"
		args4 = "-oX"
		xmlOut = "/tmp/nmapxmlout_" + userID + ".xml" # Declare the XML output file that will be used by the parser
		# for the above we need to insert a date+time string into the file.  there could be multiple scans for a user

		# Launch the nmap scan with the supplied parameters
		iReturn = subprocess.call([command, args1, args2, args3, args4, xmlOut, ipAddr], stderr=fError, stdout=fOut)


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
	except:
		print "Error launching the scan."
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
def main():	

	# Read command line parameters
	if len(sys.argv) == 4:
		ipAddr = sys.argv[1]
		userID = sys.argv[2]
		subLevel = sys.argv[3]
	else:
		printUsage()
		return 1
	
	#we should do some work on the above, namely sanitize the input

	# Launch the nmap scan with the supplied parameters
	launchScan(ipAddr, userID, subLevel)	

	return 0

if __name__ == '__main__':
	main()
