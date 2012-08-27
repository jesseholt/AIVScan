# -*- coding: utf-8 -*-
# Copyright 2012 Team Pwn Stars

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

'''
This is an auto-generated Django model module, created from the scanner schema with inspectdb,
and then adapted to PEP8 and Django conventions.
'''

class VulnerablePort(models.Model):
    pvid = models.AutoField(primary_key=True)
    protocol = models.CharField(max_length=150, db_column='Protocol')
    port_number = models.IntegerField(db_column='PortNum')
    description = models.TextField(db_column='VulnString', blank=True)
    mitigation = models.TextField(db_column='FixString', blank=True)

    class Meta:
        app_label = 'scanner'
        db_table = u'PortVulns'

class KnownVulnerability(models.Model):
    tvid = models.AutoField(primary_key=True)
    script_id = models.CharField(max_length=300, db_column='ScriptID', db_index=True)
    public_id = models.CharField(max_length=20, blank=True)
    match_string = models.CharField(max_length=600, db_column='MatchString')
    description = models.TextField(db_column='VulnString', blank=True)
    mitigation = models.TextField(db_column='FixString', blank=True)
    risk_level = models.PositiveSmallIntegerField()

    class Meta:
        app_label = 'scanner'
        db_table = u'TextVulns'
        verbose_name_plural = 'known vulnerabilities'

class Host(models.Model):
    hid = models.AutoField(primary_key=True)
    scan = models.ForeignKey('Scan', db_column='sid')
    ip4 = models.TextField(blank=True)
    hostname = models.TextField(blank=True)
    status = models.TextField(blank=True)
    mac = models.TextField(blank=True)
    distance = models.IntegerField(null=True, blank=True)
    uptime = models.TextField(blank=True)
    last_boot = models.TextField(blank=True, db_column='upstr')

    # unused fields
    # tcpcount = models.IntegerField(null=True, blank=True)
    # udpcount = models.IntegerField(null=True, blank=True)
    # ip4num = models.IntegerField(null=True, blank=True)
    # vendor = models.TextField(blank=True)
    # ip6 = models.TextField(blank=True)

    class Meta:
        app_label = 'scanner'
        db_table = u'hosts'


class OperatingSystem(models.Model):
    oid = models.AutoField(primary_key=True)
    host = models.ForeignKey(Host, db_column='hid')
    name = models.TextField(blank=True)
    family = models.TextField(blank=True)
    generation = models.TextField(blank=True)
    os_type = models.TextField(blank=True, db_column='type')
    vendor = models.TextField(blank=True)

    # unused fields
    # accuracy = models.IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'scanner'
        db_table = u'os'


class Port(models.Model):
    pid = models.AutoField(primary_key=True)
    host = models.ForeignKey(Host, db_column='hid')
    port_number = models.IntegerField(null=True, blank=True, db_column='port')
    state = models.TextField(blank=True)
    service_name = models.TextField(blank=True, db_column='name')
    product = models.TextField(blank=True)
    version = models.TextField(blank=True)
    description = models.TextField(blank=True, db_column='extra')
    proto = models.TextField(blank=True)
    fingerprint = models.TextField(blank=True)

    # unused fields
    # owner = models.TextField(blank=True)
    # rpcnum = models.TextField(blank=True)
    # confidence = models.IntegerField(null=True, blank=True)
    # method = models.TextField(blank=True)
    # tunnel = models.TextField(blank=True)
    # port_type = models.TextField(blank=True, db_column='type')

    class Meta:
        app_label = 'scanner'
        db_table = u'ports'


class Scan(models.Model):
    sid = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, db_column='userId') # Field name made lowercase.
    subscription_level = models.IntegerField(null=True, blank=True)
    version = models.TextField(blank=True)
    nmap_args = models.TextField(blank=True, db_column='args')
    start_time = models.DateTimeField(null=True, blank=True, db_column='starttime')
    end_time = models.DateTimeField(null=True, blank=True, db_column='endtime')

    # unused fields
    # xml_version = models.TextField(blank=True)
    # types = models.TextField(blank=True) # unused
    # start_str = models.TextField(blank=True) # unused
    # end_str = models.TextField(blank=True) # unused
    # num_services = models.IntegerField(null=True, blank=True) # unused

    class Meta:
        app_label = 'scanner'
        db_table = u'scans'

class FoundVulnerability(models.Model):
    vid = models.AutoField(primary_key=True)
    host = models.ForeignKey(Host, db_column='hid')
    known_vuln = models.ForeignKey(KnownVulnerability, db_column='tvid')

    class Meta:
        app_label = 'scanner'
        db_table = u'vulns'
        verbose_name_plural = 'found vulnerabilities'


class MockModel():
    pass

admin.site.register(FoundVulnerability)
admin.site.register(Scan)
admin.site.register(Port)
admin.site.register(OperatingSystem)
admin.site.register(Host)
admin.site.register(KnownVulnerability)
admin.site.register(VulnerablePort)
