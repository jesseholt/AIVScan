from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib import admin

from registration.views import activate
from registration.views import register

import aivs
from aivs import views

'''
This module performs the routing of URLs to the appropriate views.  The django-registration
URL configuration has been reimplemented here so that we can override the URLs, forms, and
templates with ones of our choosing.
TODO: we may want to swap out the default backend so that we can replace the views entirely with
our own validation logic... need to look at this in more detail.

Validation note from django-registration:
Activation keys get matched by \w+ instead of the more specific [a-fA-F0-9]{40} because a bad
activation key should still get to the view; that way it can return a sensible "invalid key" message
instead of a confusing 404.
'''

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', direct_to_template, { 'template': 'index.html' }),
                       url(r'^scan$', views.request_scan),
                       url(r'^about$', direct_to_template, { 'template': 'about.html' }),
                       url(r'^contact$', direct_to_template, { 'template': 'contact.html' }),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^activate/complete/$',
                           direct_to_template,
                           {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.default.DefaultBackend',
                            'form_class': 'aivs.registration_form',
                            'template': 'submit_scan_form.html'},
                           name='registration_register'),
                       url(r'^register/complete/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete.html'},
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           direct_to_template,
                           {'template': 'registration/registration_closed.html'},
                           name='registration_disallowed'),
                       url(r'', include('registration.auth_urls')),
                       url(r'^.*$', direct_to_template, { 'template': 'index.html' }), #fallback
)
