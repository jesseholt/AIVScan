#!/bin/bash

export AIVS_CONFIG=/home/aivs/AIVScan/config

# nginx
# This nginx configuration will proxy requests to gunicorn listening on port 8000
ln -s $AIVS_CONFIG/nginx_aivs.conf /etc/nginx/sites-available/nginx_aivs.conf
ln -s /etc/nginx/sites-available/nginx_aivs.conf /etc/nginx/sites-enables/nginx_aivs.conf

# upstart
# This upstart configuration will start our gunicorn process on boot. gunicorn will
# act as a WSGI server to run our Python process.
cp $AIVS_CONFIG/gunicorn_aivs.conf /etc/init/gunicorn_aivs.conf
ln -s /lib/init/upstart-job /etc/init.d/gunicorn_aivs