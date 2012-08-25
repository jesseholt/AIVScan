#!/usr/bin/python
'''this module used to parse nmap's xml report'''
__author__ =  'yunshu(wustyunshu@hotmail.com)'
__version__=  '0.2'
__modified_by = 'ketchup'

import sys
import pprint
import scanner.lib.Session
import scanner.lib.Host
import scanner.lib.Script
import xml.dom.minidom

class Parser:

    '''Parser class, parse a xml format nmap report'''

    def __init__( self, xml_input ):

        '''constructor function, need a xml file name as the argument'''
        try:
            self.__dom = xml.dom.minidom.parseString(xml_input)
            self.__session = None
            self.__hosts = { }
            for host_node in self.__dom.getElementsByTagName('host'):
                __host =  Host.Host(host_node)
            self.__hosts[__host.ip] = __host
        except Exception as ex:
            logging.error(ex)

    def get_session( self ):

        '''get this scans information, return a Session object'''

        run_node = self.__dom.getElementsByTagName('nmaprun')[0]
        hosts_node = self.__dom.getElementsByTagName('hosts')[0]

        finish_time = self.__dom.getElementsByTagName('finished')[0].getAttribute('timestr')

        nmap_version = run_node.getAttribute('version')
        start_time =  run_node.getAttribute('startstr')
        scan_args = run_node.getAttribute('args')

        total_hosts = hosts_node.getAttribute('total')
        up_hosts = hosts_node.getAttribute('up')
        down_hosts = hosts_node.getAttribute('down')

        MySession = { 'finish_time': finish_time,
                        'nmap_version' : nmap_version,
                        'scan_args' : scan_args,
                        'start_time' : start_time,
                        'total_hosts' : total_hosts,
                        'up_hosts' : up_hosts,
                        'down_hosts' : down_hosts }

        self.__session = Session.Session( MySession )

        return self.__session

    def get_host( self, ipaddr ):

        '''get a Host object by ip address'''

        return self.__hosts.get(ipaddr)

    def all_hosts( self, status = '' ):

        '''get a list of Host object'''

        if( status == '' ):
            return self.__hosts.values( )

        else:
            __tmp_hosts = [ ]

            for __host in self.__hosts.values( ):

                if __host.status == status:
                    __tmp_hosts.append( __host )

            return __tmp_hosts

    def all_ips( self, status = '' ):

        '''get a list of ip address'''
        __tmp_ips = [ ]

        if( status == '' ):
            for __host in self.__hosts.values( ):

                __tmp_ips.append( __host.ip )

        else:
            for __host in self.__hosts.values( ):

                if __host.status == status:
                    __tmp_ips.append( __host.ip )

        return __tmp_ips

if __name__ == '__main__':

    parser = Parser( '/tmp/test_pwn01.xml' )

    print '\nscan session:'
    session = parser.get_session()
    print "\tstart time:\t" + session.start_time
    print "\tstop time:\t" + session.finish_time
    print "\tnmap version:\t" + session.nmap_version
    print "\tnmap args:\t" + session.scan_args
    print "\ttotal hosts:\t" + session.total_hosts
    print "\tup hosts:\t" + session.up_hosts
    print "\tdown hosts:\t" + session.down_hosts

    for h in parser.all_hosts():

        print 'host ' +h.ip + ' is ' + h.status

        for port in h.get_ports( 'tcp', 'open' ):
            print "\tservice of tcp port " + port + ":"
            s = h.get_service( 'tcp', port )

            if s == None:
                print "\t\tno service"

            else:
                print "\t\t" + s.name
                print "\t\t" + s.product
                print "\t\t" + s.version
                print "\t\t" + s.extrainfo
                print "\t\t" + s.fingerprint

        print "Script output:"
        for scr in h.get_scripts():
            print "Script ID: " + scr.scriptId
            print "Output: "
            print scr.output

    pprint.pprint( parser.all_ips() )
