#!/bin/bash
set -e
AIVS_VIRTUALENV=/home/aivs/.virtualenv/aivs
AIVS_HOME=/home/aivs

PYTHONPATH=/home/aivs/AIVScan/www
AIVS_SETTINGS_PATH=aivs.settings
USER=aivs
GROUP=aivs
NUM_WORKERS=2
LOG_FILE=$AIVS_HOME/var/aivs.log

cd $AIVS_HOME/AIVScan/www/aivs
source $AIVS_VIRTUALENV/bin/activate
exec $AIVS_VIRTUALENV/bin/gunicorn_django -u $USER -g $GROUP --pythonpath=$PYTHONPATH --preload -w $NUM_WORKERS --worker-class gevent --log-level debug --log-file $LOG_FILE -b 127.0.0.1:8000 --settings $AIVS_SETTINGS_PATH &