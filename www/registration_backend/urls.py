from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

from registration.views import activate, register

'''
The django-registration URL configuration has been reimplemented here so that we can override
the URLs, forms, and templates with ones of our choosing.

Validation note from django-registration:
Activation keys get matched by \w+ instead of the more specific [a-fA-F0-9]{40} because a bad
activation key should still get to the view; that way it can return a sensible "invalid key" message
instead of a confusing 404.
'''

urlpatterns = patterns('',
                       url(r'^activate/complete/$',
                           direct_to_template,
                           {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration_backend.AivsBackend'},
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           {'backend': 'registration_backend.AivsBackend',
                            'form_class': 'aivs.forms.RegistrationForm',
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
)
