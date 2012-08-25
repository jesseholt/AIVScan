from django.db import models
from django.contrib.auth.models import User

'''
This is an auto-generated Django model module, created from the scanner schema with inspectdb.
app_label was added to allow for multi-file model imports in the aivs app.
'''

class Portvulns(models.Model):
    pvid = models.IntegerField(primary_key=True)
    protocol = models.CharField(max_length=150, db_column='Protocol') # Field name made lowercase.
    portnum = models.IntegerField(db_column='PortNum') # Field name made lowercase.
    vulnstring = models.TextField(db_column='VulnString', blank=True) # Field name made lowercase.
    fixstring = models.TextField(db_column='FixString', blank=True) # Field name made lowercase.
    class Meta:
        app_label = 'scanner'
        db_table = u'PortVulns'

class Textvulns(models.Model):
    tvid = models.IntegerField(primary_key=True)
    scriptid = models.CharField(max_length=300, db_column='ScriptID') # Field name made lowercase.
    matchstring = models.CharField(max_length=600, db_column='MatchString') # Field name made lowercase.
    vulnstring = models.TextField(db_column='VulnString', blank=True) # Field name made lowercase.
    fixstring = models.TextField(db_column='FixString', blank=True) # Field name made lowercase.
    class Meta:
        app_label = 'scanner'
        db_table = u'TextVulns'

class Hosts(models.Model):
    hid = models.IntegerField(primary_key=True)
    sid = models.ForeignKey('Scans', db_column='sid')
    ip4 = models.TextField(blank=True)
    ip4num = models.IntegerField(null=True, blank=True)
    hostname = models.TextField(blank=True)
    status = models.TextField(blank=True)
    tcpcount = models.IntegerField(null=True, blank=True)
    udpcount = models.IntegerField(null=True, blank=True)
    mac = models.TextField(blank=True)
    vendor = models.TextField(blank=True)
    ip6 = models.TextField(blank=True)
    distance = models.IntegerField(null=True, blank=True)
    uptime = models.TextField(blank=True)
    upstr = models.TextField(blank=True)
    class Meta:
        app_label = 'scanner'
        db_table = u'hosts'

class Os(models.Model):
    oid = models.IntegerField(primary_key=True)
    hid = models.ForeignKey(Hosts, db_column='hid')
    name = models.TextField(blank=True)
    family = models.TextField(blank=True)
    generation = models.TextField(blank=True)
    os_type = models.TextField(blank=True, db_column='type')
    vendor = models.TextField(blank=True)
    accuracy = models.IntegerField(null=True, blank=True)
    class Meta:
        app_label = 'scanner'
        db_table = u'os'

class Ports(models.Model):
    pid = models.IntegerField(primary_key=True)
    hid = models.ForeignKey(Hosts, db_column='hid')
    port = models.IntegerField(null=True, blank=True)
    port_type = models.TextField(blank=True, db_column='type')
    state = models.TextField(blank=True)
    name = models.TextField(blank=True)
    tunnel = models.TextField(blank=True)
    product = models.TextField(blank=True)
    version = models.TextField(blank=True)
    extra = models.TextField(blank=True)
    confidence = models.IntegerField(null=True, blank=True)
    method = models.TextField(blank=True)
    proto = models.TextField(blank=True)
    owner = models.TextField(blank=True)
    rpcnum = models.TextField(blank=True)
    fingerprint = models.TextField(blank=True)
    class Meta:
        app_label = 'scanner'
        db_table = u'ports'

class Scans(models.Model):
    sid = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, db_column='userId') # Field name made lowercase.
    subscription_level = models.IntegerField(null=True, blank=True)
    version = models.TextField(blank=True)
    xmlversion = models.TextField(blank=True)
    args = models.TextField(blank=True)
    types = models.TextField(blank=True)
    starttime = models.DateTimeField(null=True, blank=True)
    startstr = models.TextField(blank=True)
    endtime = models.DateTimeField(null=True, blank=True)
    endstr = models.TextField(blank=True)
    numservices = models.IntegerField(null=True, blank=True)
    class Meta:
        app_label = 'scanner'
        db_table = u'scans'

class Sequencing(models.Model):
    sqid = models.IntegerField(primary_key=True)
    hid = models.ForeignKey(Hosts, db_column='hid')
    tcpclass = models.TextField(blank=True)
    tcpindex = models.TextField(blank=True)
    tcpvalues = models.TextField(blank=True)
    ipclass = models.TextField(blank=True)
    ipvalues = models.TextField(blank=True)
    tcptclass = models.TextField(blank=True)
    tcptvalues = models.TextField(blank=True)
    class Meta:
        app_label = 'scanner'
        db_table = u'sequencing'

class Vulns(models.Model):
    vid = models.IntegerField(primary_key=True)
    hid = models.ForeignKey(Hosts, db_column='hid')
    tvid = models.ForeignKey(Textvulns, db_column='tvid')
    class Meta:
        app_label = 'scanner'
        db_table = u'vulns'
