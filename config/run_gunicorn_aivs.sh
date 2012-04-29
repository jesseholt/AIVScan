#!/bin/bash

set -e
LOGFILE=/home/aivs/var/gunicorn.log
LOGDIR=$(dirname $LOGFILE)
PIDFILE=/home/aivs/var/gunicorn.pid

NUM_WORKERS=2
USER=aivs
GROUP=aivs
VIRTUAL_ENV=/home/aivs/.virtualenv/aivs

source ${VIRTUAL_ENV}/bin/activate
export DJANGO_SETTINGS_MODULE=aivs.settings
export AIVS_HOME=/home/aivs/AIVScan
export PYTHONPATH=/home/aivs/AIVScan/www

test -d $LOGDIR || mkdir -p $LOGDIR

cd $AIVS_HOME/www
gunicorn_django --pythonpath $PYTHONPATH -w $NUM_WORKERS --log-level=$LOGLEVEL --log-file=$LOGFILE -p $PIDFILE -b 127.0.0.1:8000 --settings $DJANGO_SETTINGS_MODULE
