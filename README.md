# AIVScan

By PwnStars (Drexel CT491-CT496)

AIVScan is a web application for performing remote Nmap scans.  The goal is to allow home users and small businesses the ability to perform simple security assessments of their public facing IPs, and to provide easy-to-understand reports for these users.

## Setup

In a virtual environment (either a VM or using virtualenv), clone the repository and install the dependencies with pip.
<pre><code>
git@github.com:tgross/AIVScan.git
pip install -r AIVScan/config/pip-requirements.txt
</code></pre>

AIVScan has the following Django application dependencies (found in the pip-requirements script):


- django-celery
- gunicorn
- django-bootstrap (yeah, yeah, this is basically an out-of-the-box Bootstrap front-end)
- django-registration


Copy the local_settings example file to set up the environment-specific settings.  Also, optionally, set up your MySQL database at this point.
<pre><code>
cp AIVScan/www/aivs/local_settings.example.py AIVScan/www/aivs/local_settings.py
emacs AIVScan/www/aivs/local_settings.py
</code></pre>

Sync your database with the Django models, and load the fixtures found in the *scanner* app.
<pre><code>
cd AIVScan/www/aivs
python manage.py syncdb
python manage.py loaddata AIVScan/www/scanner/fixtures/known_port_fixtures.json
python manage.py loaddata AIVScan/www/scanner/fixtures/known_vuln_fixtures.json
</code></pre>

For production environments, the config directory contains configuration files and setup scripts to run AIVScan on Ubuntu 10.04LTS, using Nginx as a reverse proxy, Gunicorn as the WSGI server, and Upstart as the manager for Django and Celery.  Your mileage may vary with these scripts.