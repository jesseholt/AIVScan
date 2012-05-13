#!/bin/bash

# mysql and mysql python libraries
sudo apt-get install python-dev
sudo apt-get install python-mysqldb
sudo apt-get install libmysqlclient-dev


# Python libraries
pip install -r pip-requirements

export AIVS_CONFIG=/home/aivs/AIVScan/config

# nginx
sudo apt-get install nginx

# This nginx configuration will proxy requests to gunicorn listening on port 8000
ln -s $AIVS_CONFIG/nginx_aivs.conf /etc/nginx/sites-available/nginx_aivs.conf
ln -s /etc/nginx/sites-available/nginx_aivs.conf /etc/nginx/sites-enabled/nginx_aivs.conf

# upstart
# This upstart configuration will start our gunicorn process on boot. gunicorn will
# act as a WSGI server to run our Python process.
cp $AIVS_CONFIG/gunicorn_aivs.conf /etc/init/gunicorn_aivs.conf
ln -s /lib/init/upstart-job /etc/init.d/gunicorn_aivs

# set up your MySQL db using the following MySQL commands

# mysql -u root -p
# create database aivs;
# alter database aivs character set utf8;
# create user 'aivs'@'localhost' identified by 'mypassword';
# grant all on aivs.* to 'aivs'@'localhost';
# flush privileges;
# exit;

