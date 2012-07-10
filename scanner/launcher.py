import subprocess
import os
import scan_parser

fError = open("/tmp/nmaperror.txt", 'w')
fOut = open("/tmp/nmapout.txt", 'w')

p = "nmap"
#args = "-sT -sV -O -oX /tmp/nmapxmlout.xml 192.168.126.129"
#args = "192.168.126.129"
args1 = "-sT"
args2 = "-P0"
args3 = "-sV"
args4 = "-oX"
args5 = "/tmp/nmapxmlout.xml"
args6 = "192.168.126.129"
iReturn = subprocess.call([p, args1, args2, args3, args4, args5, args6], stderr=fError, stdout=fOut)
print "subprocess.call() return: " + str(iReturn)


if os.path.exists("/tmp/nmapout.txt"):
	fOut = open("/tmp/nmapout.txt", 'r')
if os.path.exists("/tmp/nmaperror.txt"):
	fError = open("/tmp/nmaperror.txt", 'r')

sOuput = ''
sError = ''
if not fOut is None:
	sOutput = fOut.read()
if not fError is None:
	sError = fError.read()

print "STDOUT: " + sOutput
print "Errors: " + sError
fOut.close()
fError.close()

username = 'aivs'
password = 'Fish dont fry in the kitchen.'
dbhost = 'localhost'
dbname = 'aivs'

cp = scan_parser.cSQLImporter(username, password, dbhost, dbname, '/tmp/nmapxmlout.xml', 1001)
cp.process()



