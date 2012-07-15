from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

import simplejson

from aivs import tasks
from aivs.models import ScanResult
from aivs.forms import ContactForm, ScanRequestForm
'''
This module contains the main logic of the web application.  Although the module is called views
in the Django convention, this module takes the role of Controller in the classic MVC pattern.
'''

@login_required(login_url='/login/')
def request_scan(request):
    ip = get_client_ip(request)
    if request.method == 'POST':
        # we bind a form to the POST data
        form = ScanRequestForm(request.POST)
        if form.is_valid():
            # form.cleaned_data now contains only valid data
            user = request.user
            tasks.run_scan.delay(user, ip)
            return HttpResponseRedirect('/profile/') # <- this should redirect to success page
    else:
        # form has not been submitted, so prepare an unbound form
        form = ScanRequestForm()
    return render_to_response('scan.html', {'form': form, 'ip': ip}, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def profile(request):
    user = request.user
    scans = ScanResult.objects.filter(user=user).order_by('-completion_dt')
    return render_to_response('profile.html', {'user':user, 'scans': scans},
                              context_instance=RequestContext(request))

def contact(request):
    if request.method == 'POST':
        # bind a form to the POST data
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.cleaned_data now contains only valid data
            user_email = form.cleaned_data['email_address']
            message = form.cleaned_data['message']
            tasks.send_admin_email(user_email, message)
            return HttpResponseRedirect('/')
    else:
        # the form has not been submitted, so prepare an unbound form
        form = ContactForm()
    return render_to_response('contact.html',
                              {'form': form},
                              context_instance=RequestContext(request))

def get_client_ip(request):
    '''
    Gets the client IP address from the request headers, including handling proxies.
    TODO: this is where we should validate format of the IP address.
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

