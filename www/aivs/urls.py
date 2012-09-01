from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin

from aivs import views

'''
This module performs the routing of URLs to the appropriate views and serves as the root
URL configuration file.  It routes by inclusion to the registration and admin URLs.
'''

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', direct_to_template, { 'template': 'home.html' }, name='home'),
    url(r'^home/$', redirect_to, { 'url': '/' }),
    url(r'^about/$', direct_to_template, { 'template': 'about.html' }, name='about'),
    url(r'^contact/$', views.contact, name='contact'),

    # these urls use the same view but control template with passed arguments
    url(r'^profile/$', views.profile_and_reports, { 'template': 'profile.html' }, name='profile'),
    url(r'^reports/$', views.profile_and_reports, { 'template': 'profile_table.html' }, name='reports'),

    # scan workflow urls
    url(r'^scan/$', views.request_scan, name='scan'),
    url(r'^scan_running/$', views.slideshow, name='slideshow'),
    url(r'^report/(?P<id>\d+)/$', views.scan_report, name='scan_report'),

    # included apps
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('django.contrib.auth.urls')),
    url(r'', include('registration_backend.urls')),
)
