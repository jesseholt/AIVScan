from celery.task import task

@task
def run_scan(safe_ip_address):
    '''
    Executes the scan task.  If this function is called with run_scan.delay(safe_ip_address), then
    it will be placed into the Celery queue for asynchronous processing.
    IMPORTANT: The caller is responsible for validating cleaning the arguments passed to this task!
    '''
    return 'Done!'
