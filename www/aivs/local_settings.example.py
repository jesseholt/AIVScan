# Django settings for AIVS project.
import os

LOGDIR = os.path.abspath('/path/to/log/files')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'aivs',
        'USER': 'aivs',
        'PASSWORD': 'ENTER YOUR PASSWORD HERE',
        'HOST': '', # leaves as default
        'PORT': '', # leaves as default
    }
}

# ALTERNATE
# If you would rather use a sqlite3 database for local development, use django.db.backends.sqlite3 as the ENGINE, and change NAME to the absolute file path to the database file (it will be automatically created for you.)  Leave USER, PASSWORD, HOST, and PORT blank.


# This secret key is used as a seed for salts, etc.  Default Django values
# are 60 bytes (i.e. 60 characters from the full ascii range).
SECRET_KEY = 'ENTER YOUR SECRET KEY HERE'

# Settings for sending email from the server
# to test email use
# python -m smtpd -n -c DebuggingServer localhost:1025
EMAIL_USE_TLS = True
EMAIL_HOST = 'localhost'  # 'smtp.example.com'
EMAIL_HOST_USER  = 'aivscan@example.com'
EMAIL_HOST_PASSWORD = 'YourPasswordHere'
EMAIL_PORT = 1025 # 587
DEFAULT_FROM_EMAIL = 'aivscan@example.com'
SERVER_EMAIL = 'aivscan@example.com'
