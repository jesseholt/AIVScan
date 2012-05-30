from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin

from aivs import views

'''
This module performs the routing of URLs to the appropriate views and serves as the root
URL configuration file.  It routes by inclusion to the registration and admin URLs.
'''

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', direct_to_template, { 'template': 'index.html' }, name='home'),
                       url(r'^about$', direct_to_template, { 'template': 'about.html' }, name='about'),
                       url(r'^contact$', direct_to_template, { 'template': 'contact.html' }, name='contact'),
                       url(r'^scan$', views.request_scan),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('registration_backend.urls')),
#                       url(r'', include('registration.auth_urls')),
)
