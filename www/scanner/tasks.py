import os
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
        'nmap'
        '-sT',
        '-sV',
        '-P0',
        '-oX',
        '--script',
        'smb-check-vulns,vuln,exploit', # run these nse scripts
        safe_ip_address
        ]
    try:
        # by using check_call we can get the stdout from nmap and then pipe that as a string
        # directly into the scan_parsing module without having to do file I/O
        xml_results = subprocess.check_call(nmap_args)
        si = ScanImporter(xml_results, user.id)
        si.process()
    except Exception as ex:
        logging.error(ex)
