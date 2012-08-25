# -*- coding: utf-8 -*-
# Copyright 2012 Team Pwn Stars

import tempfile
import subprocess
from django.conf import settings
import logging
from celery.task import task

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
        'nmap',
        '-sT',
        '-sV',
        '-P0',
        '-oX',
        '-', # output the XML to stdout rather than a real file so we can capture it
        '--script',
        'smb-check-vulns,vuln,exploit', # run these nse scripts
        safe_ip_address
        ]
    #try:
    std_out = tempfile.mkstemp() # generates a secure temp file with no race conditions
    success = subprocess.check_call(nmap_args, stdout=std_out[0])
    if success == 0:
        f = open(std_out[1], 'r') # read the file-like back into memory.
        xml_results = f.read()
        f.close()
        si = ScanImporter(xml_results, user.id)
        si.process()
    #except Exception as ex:
    #    logging.error('Task failed to initiate\n'.format(ex))
