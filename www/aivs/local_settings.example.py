# Django settings for AIVS project.

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

# This secret key is used as a seed for salts, etc.  Default Django values
# are 60 bytes (i.e. 60 characters from the full ascii range).
SECRET_KEY = 'ENTER YOUR SECRET KEY HERE'

