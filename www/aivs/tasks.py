import os
import subprocess

from django.conf import settings
from celery.task import task

@task
def run_scan(user, safe_ip_address, subscription_level=0):
    '''
    Executes the scan task.  If this function is called with run_scan.delay(safe_ip_address), then
    it will be placed into the Celery queue for asynchronous processing.
    IMPORTANT: The caller is responsible for validating cleaning the arguments passed to this task!
    '''
    pycmd = os.path.abspath(os.path.join(settings.ROOTDIR, '..', 'scanner', 'launcher.py'))
    subprocess.call([pycmd, safe_ip_address, str(user.id), str(subscription_level)])
    return

