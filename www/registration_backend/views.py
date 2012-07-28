from django.contrib.auth import views as auth_views
from registration.views import register as reg_view
from registration_backend import forms

def register(request):
    '''
    Wraps the django-registration register view, so as to allow for different templates to be set
    in that view depending on whether or not the request is Ajax.
    '''
    if request.is_ajax():
        template_name = 'registration_modal.html'
    else:
        template_name = 'registration_form.html'

    return reg_view (request,
                     'registration_backend.AivsBackend',
                     success_url = 'registered/',
                     form_class = forms.RegistrationForm,
                     disallowed_url = 'closed/',
                     template_name = template_name)


def login(request):
    '''
    Wraps the django.contrib.auth login view, so as to allow for different templates to be set
    in that view depending on whether or not the request is Ajax.
    '''
    if request.is_ajax():
        template_name = 'login_modal.html'
    else:
        template_name = 'login.html'

    return auth_views.login(request,
                            template_name = template_name,
                            authentication_form = forms.AivsAuthenticationForm)

def forgot_password(request):
    '''
    Wraps the django.contrib.auth reset_password view, so as to allow for different templates to be
    set in that view depending on whether or not the request is Ajax.
    '''
    if request.is_ajax():
        template_name = 'forgot_password_modal.html'
    else:
        template_name = 'forgot_password.html'

    return auth_views.password_reset(request,
                                     template_name = template_name,
                                     post_reset_redirect = 'profile/')


def change_password(request):
    '''
    Wraps the django.contrib.auth reset_password view, so as to allow for different templates to be
    set in that view depending on whether or not the request is Ajax.
    '''
    if request.is_ajax():
        template_name = 'password_change_modal.html'
    else:
        template_name = 'password_change.html'

    return auth_views.password_change(request,
                                     template_name = template_name,
                                     post_change_redirect = 'profile/')
