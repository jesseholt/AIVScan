from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, Template

import re
import simplejson

from aivs.forms import ContactForm, ScanRequestForm
from scanner import tasks
from scanner.models import *
'''
This module contains the main logic of the web application.  Although the module is called views
in the Django convention, this module takes the role of Controller in the classic MVC pattern.
'''

@login_required(login_url='/login/')
def request_scan(request):
    ip = get_client_ip(request)
    if not ip:
        return HttpResponseForbidden # invalid client IP address sent

    if request.method == 'POST':
        # we bind a form to the POST data
        form = ScanRequestForm(request.POST)
        if form.is_valid():
            # form.cleaned_data now contains only valid data
            user = request.user
            tasks.run_scan.delay(user, ip)
            return HttpResponseRedirect('/profile/')
    else:
        # form has not been submitted, so prepare an unbound form
        form = ScanRequestForm()
    return render_to_response('scan.html', {'form': form, 'ip': ip},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def profile_and_reports(request, template='profile.html'):
    '''
    Gets the user profile and serves the Ajax call to get the table of scans.
    '''
    scans = list(Scan.objects.filter(user_id=request.user).order_by('-start_time'))
    for scan in scans:
        try:
            host = Host.objects.get(scan=scan.pk)
            scan.ip = host.ip4
            scan.hostname = host.hostname
        except Host.DoesNotExist:
            scan.ip = None
            scan.hostname = 'pending...'
    return render_to_response(template, {'scans': scans},
                              context_instance=RequestContext(request))

@login_required(login_url='/login/')
def slideshow(request):
    return render_to_response('slideshow.html',
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def scan_report(request, id):
    '''
    Generates the in-browser report.
    '''
    user = request.user
    try:
        report = Scan.objects.get(pk=id, user_id=user.id)
        report_contents = get_report_contents(report)
        return render_to_response('report.html',
                                  context_instance=RequestContext(request, report_contents))
    except Scan.DoesNotExist:
        return HttpResponseRedirect('/profile/') # TODO: do some kind of proper error handling here

def get_report_contents(report):
    '''
    Helper function to query a scan and gets its related objects to build a dict suitable to construct a
    Context or RequestContext from for use in a template.  Get used by scan_report view and by
    the scanner task that sends email reports.
    '''
    host = Host.objects.get(scan=report.pk)
    ports = KnownPort.objects.filter(foundport__host=host.pk)
    vulns = KnownVulnerability.objects.filter(foundvulnerability__host=host.pk)
    try:
        OS = host.os
    except:
        OS = MockModel()
        OS.name = 'No OS information detected.'
    return { 'report':report, 'host': host, 'ports': ports, 'vulns': vulns, 'OS': OS }


def contact(request):
    if request.method == 'POST':
        # bind a form to the POST data
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.cleaned_data now contains only valid data
            user_email = form.cleaned_data['email_address']
            message = form.cleaned_data['message']
            tasks.send_admin_email(user_email, message)
            return HttpResponseRedirect('/')
    else:
        # the form has not been submitted, so prepare an unbound form
        form = ContactForm()
    return render_to_response('contact.html', {'form': form},
                              context_instance=RequestContext(request))


ip_regex_pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')

def get_client_ip(request):
    '''
    Gets the client IP address from the request header set by the Nginx proxy, and performs some
    simple validation.  If the check fails in a debug environment (ex. local development without
    Nginx proxy), fill in the local IP.
    In a production environment, we might not want to use this header by itself, as load balancers
    might show up as the IP.
    '''
    ip = request.META.get('HTTP_X_REAL_IP', None)
    if ip and ip_regex_pattern.match(ip):
        return ip
    elif settings.DEBUG:
        return 'localhost'
    else:
        return None


