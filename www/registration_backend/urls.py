from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template
from django.contrib.auth import urls as auth_urls
from django.contrib.auth import views as auth_views

from registration.views import activate, register
import registration_backend
from registration_backend import forms

'''
The django-registration URL configuration has been reimplemented here so that we can override
the URLs, forms, and templates with ones of our choosing.

Registration workflow is:
register/       The user requests a scan and we take his name and email address.
registered/   After form validation, we tell the user to await an email from us.
activate/      The link the user clicks on from the email we send.
activated/    We have verified the user and queue the first scan.

Validation note from django-registration:
Activation keys get matched by \w+ instead of the more specific [a-fA-F0-9]{40} because a bad
activation key should still get to the view; that way it can return a sensible "invalid key" message
instead of a confusing 404.
'''

urlpatterns = patterns(
    '',
    url(r'^register/$',
        register,
        {'backend': 'registration_backend.AivsBackend',
         'success_url': 'registered/',
         'form_class': forms.RegistrationForm,
         'disallowed_url': 'closed/',
         'template_name': 'registration.html'},
        name='registration_register'),
    url(r'^register/registered/$',
        direct_to_template,
        {'template': 'registered.html'},
        name='registration_complete'),
    url(r'^activated/$',
        direct_to_template,
        {'template': 'activated.html'},
        name='registration_activation_complete'),
    url(r'^activate/(?P<activation_key>\w+)/$',
        activate,
        {'backend': 'registration_backend.AivsBackend'},
        name='registration_activate'),
    url(r'^closed/$',
        direct_to_template,
        {'template': 'closed.html'},
        name='registration_disallowed'),
    url(r'^login/$', auth_views.login, {'template_name':'registration/login.html',
                                        'authentication_form': forms.AivsAuthenticationForm}, name='auth_login'),
)
