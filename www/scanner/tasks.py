# -*- coding: utf-8 -*-
# Copyright 2012 Team Pwn Stars

import tempfile
import subprocess
import logging, traceback

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from celery.task import task

from scanner.models import Scan
from scanner.scan_parser import ScanImporter


@task
def run_scan(user, safe_ip_address, subscription_level=0):
    '''
    Executes the scan task.  If this function is called with run_scan.delay(safe_ip_address), then
    it will be placed into the Celery queue for asynchronous processing.
    IMPORTANT: The caller is responsible for validating / cleaning the arguments passed to this task!
    '''
    # Initialize the scan variables to pass to the subprocess call
    nmap_args = [
        '/usr/local/bin/nmap',
        '-sT',
        '-sV',
        '-P0',
        '-oX',
        '-', # output the XML to stdout rather than a real file so we can capture it
        '--script',
        'smb-check-vulns,vuln,exploit', # run these nse scripts
        safe_ip_address
        ]
    try:
        scan = Scan()
        scan.user = user
        scan.state = Scan.PENDING
        scan.save()
        scan_id = scan.pk
        std_out = tempfile.mkstemp() # generates a secure temp file with no race conditions
        success = subprocess.check_call(nmap_args, stdout=std_out[0])
        if success == 0:
            f = open(std_out[1], 'r') # read the file-like back into memory.
            xml_results = f.read()
            f.close()
            si = ScanImporter(xml_results, scan_id, user.id)
            si.process()
    except Exception as ex:
        logging.error('Task failed to initiate\n{0}'.format(ex))


@task
def send_scan_report(scan_id):
    '''
    Executes the tasks of rendering the email-based report and then sending the scan results back to
    the user in an email.  If this function is called with send_scan_report.delay(scan_id), it will be
    placed into the Celery queue for async.
    '''
    from aivs.views import get_report_contents
    try:
        scan = Scan.objects.get(pk=scan_id)
        context = get_report_contents(scan)
        html_email_body = render_to_string('report_email.html', context)
        text_email_body = strip_tags(html_email_body)
        email_subject = 'Your AIVScan is complete!'
        msg = EmailMultiAlternatives(email_subject, text_email_body,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [scan.user.email])
        msg.attach_alternative(html_email_body, 'text/html')
        msg.send()
    except Scan.DoesNotExist:
        logging.error('Failed to send email.\n{0}'.format(ex))
        return None


