# -*- coding: utf-8 -*-
# Copyright 2012 Team Pwn Stars

import datetime
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

'''
This was originally an auto-generated Django model module, created from the scanner schema with inspectdb and then adapted to PEP8 and Django conventions.  But as the project has progressed we have needed to expand it and improve naming conventions and data relationships.  Note that none
of these models are showing primary key fields and that we have taken the default autoincrementing
pk from Django for safety.
'''

class KnownPort(models.Model):
    '''
    Represents a port known to AIVScan as harboring potential problems.
    '''
    # these members restrict the choices available to insert in the protocol field.
    TCP= 'tcp'
    UDP='udp'
    ICMP='icmp'
    PROTOCOLS = ((TCP,'tcp'), (UDP,'udp'),(ICMP,'icmp'))
    protocol = models.CharField(max_length=4, choices=PROTOCOLS, blank=True)

    port_number = models.IntegerField()
    description = models.TextField(blank=True)
    mitigation = models.TextField(blank=True)


class KnownVulnerability(models.Model):
    '''
    Represents a vulnerability known to AIVScan via nmap .nse scripts.
    '''
    script_id = models.CharField(max_length=300, db_index=True)  # the .nse script used
    public_id = models.CharField(max_length=20, blank=True) # the CVE or MS number
    match_string = models.CharField(max_length=600)
    description = models.TextField(blank=True)
    mitigation = models.TextField(blank=True)
    risk_level = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'known vulnerabilities'


class OperatingSystem(models.Model):
    '''
    Represents the best guess by nmap as to the operating system of the scanned host.  A host has
    one operating system.
    '''
    name = models.CharField(max_length=200, blank=True)
    family = models.CharField(max_length=200, blank=True)
    generation = models.CharField(max_length=200, blank=True)
    os_type = models.CharField(max_length=200, blank=True)
    vendor = models.CharField(max_length=200, blank=True)

    # these fields are not used in this version of AIVScan
    # accuracy = models.IntegerField(null=True, blank=True)


class Host(models.Model):
    '''
    Represents a single host scanned by nmap.  Must be associated with a scan.
    '''
    scan = models.ForeignKey('Scan', db_index=True)
    ip4 = models.CharField(max_length=16, blank=True)
    hostname = models.CharField(max_length=200, blank=True)
    operating_system = models.ForeignKey(OperatingSystem, null=True)
    mac = models.CharField(max_length=18, blank=True)
    uptime = models.CharField(max_length=200, blank=True)
    last_boot = models.CharField(max_length=200, blank=True)

    # these fields were part of the initial schema but are not used in this version of AIVScan
    # unused fields
    # status = models.CharField(max_length=200, blank=True)
    # distance = models.IntegerField(null=True, blank=True)
    # tcpcount = models.IntegerField(null=True, blank=True)
    # udpcount = models.IntegerField(null=True, blank=True)
    # ip4num = models.IntegerField(null=True, blank=True)
    # vendor = models.CharField(max_length=200, blank=True)
    # ip6 = models.CharField(max_length=200, blank=True)


class FoundPort(models.Model):
    '''
    Represents a port discovered on a host.  Hosts have many ports, but a port exists only on one
    host.
    '''
    host = models.ForeignKey(Host)

    # these members restrict the choices available to insert in the protocol field.  Although having
    # these defined both here and in the PortVulnerabilites class breaks the DRY principal, this is
    # outweighed by the convenience of class-attribute access like Port.TCP
    TCP= 'tcp'
    UDP='udp'
    ICMP='icmp'
    PROTOCOLS = ((TCP,'tcp'), (UDP,'udp'),(ICMP,'icmp'))
    protocol = models.CharField(max_length=4, choices=PROTOCOLS, blank=True)

    # these members restrict the choices available to insert in the state field, and are the 6
    # states recognized by nmap.
    OPEN='open'
    CLOSED='closed'
    FILTERED='filtered'
    UNFILTERED='unfiltered'
    OPENFILTERED='open|filtered'
    CLOSEDFILTERED='closed|filtered'
    STATES = ((OPEN,OPEN),(CLOSED,CLOSED),(FILTERED,FILTERED),(UNFILTERED,UNFILTERED),
              (OPENFILTERED,OPENFILTERED),(CLOSEDFILTERED,CLOSEDFILTERED))
    state = models.TextField(max_length=16, choices=STATES, blank=True)

    port_number = models.IntegerField(null=True, blank=True)
    service_name = models.CharField(max_length=200, blank=True)
    product = models.CharField(max_length=200, blank=True)
    version = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    fingerprint = models.CharField(max_length=200, blank=True)

    # these fields were part of the initial schema but are not used in this version of AIVScan
    # owner = models.CharField(max_length=200, blank=True)
    # rpcnum = models.CharField(max_length=200, blank=True)
    # confidence = models.IntegerField(null=True, blank=True)
    # method = models.CharField(max_length=200, blank=True)
    # tunnel = models.CharField(max_length=200, blank=True)
    # port_type = models.TextField(blank=True, db_column='type')


class FoundVulnerability(models.Model):
    '''
    Represents a KnownVulnerability that has been discovered on a host.  Found vulnerabilities
    have one and only one associated known vulnerability.  Hosts can have many found
    vulnerabilities.
    '''
    host = models.ForeignKey(Host)
    known_vuln = models.ForeignKey(KnownVulnerability)

    class Meta:
        verbose_name_plural = 'found vulnerabilities'


class Scan(models.Model):
    '''
    Represents a user-initiated nmap scan.  Users can have multiple scans, scans can have
    multiple hosts in the database but are limited due to NAT to one for practical purposes.
    '''
    user_id = models.ForeignKey(User, db_index=True)
    nmap_args = models.TextField()
    start_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(null=True, blank=True)

    # these members restrict the choices available to insert in the status field
    PENDING = 'P'
    COMPLETE = 'C'
    STATUS = (( PENDING, 'pending'), (COMPLETE, 'complete'))
    status = models.CharField(max_length=1, choices=STATUS, default=PENDING)

    # these fields were part of the initial schema but are not used in this version of AIVScan
    # subscription_level = models.IntegerField(null=True, blank=True)
    # version = models.CharField(max_length=200, blank=True)
    # xml_version = models.CharField(max_length=200, blank=True)
    # types = models.CharField(max_length=200, blank=True)
    # start_str = models.CharField(max_length=200, blank=True)
    # end_str = models.CharField(max_length=200, blank=True)
    # num_services = models.IntegerField(null=True, blank=True)


class MockModel():
    '''
    Used as an empty class to safely add dynamic attributes to for purposes of creating default
    objects at runtime.
    '''
    pass


# register all the above models with the Django admin.
admin.site.register(KnownVulnerability)
admin.site.register(KnownPort)
admin.site.register(OperatingSystem)
admin.site.register(Host)
admin.site.register(FoundVulnerability)
admin.site.register(FoundPort)
admin.site.register(Scan)



