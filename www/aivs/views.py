from django.http import HttpResponse
from django.contib.auth.models import User

import simplejson

from aivs import tasks

'''
This module contains the main logic of the web application.  Although the module is called views
in the Django convention, this module takes the role of Controller in the classic MVC pattern.
'''

def request_scan(request):
    if request.method == 'POST':
        # we bind a form to the POST data
        form = ScanRequestForm(request.POST)
        if form.is_valid():
            # form.cleaned_data now contains only valid data
            user_data = (
                form.cleaned_data['email_address'],
                form.cleaned_data['first_name'],
                form.cleaned_data['last_name'],
                )
            user = get_or_create_user(user_data)
            ip = get_client_ip(request)
            tasks.run_scan.delay(user, ip)
            return HttpResponseRedirect('/success/')
    else:
        # form has not been submitted, so prepare an unbound form
        form = ScanRequestForm()
    return render_to_response('submit_scan_form.html', {'form': form})

'''
def scan(request):
    form = ScanRequestForm(request.POST)
    if form.is_valid():
        form.save()
        d = {'error': 0, 'message': 'success'}
    else:
        d = {'error': 1}
        form_html = render_to_string('submit_scan_form.html',
                                     context_instance=RequestContext(request))
        d['message'] = form_html
    response = simplejson.dumps(d)
    return HttpResponse(response, mimetype='application/json')
'''

def get_or_create_user(user_data):
    '''
    Queries the database for an existing user or creates a new one with the parameters provided.
    '''
    try:
        user = User.objects.get_or_404(email=user_data[0])
    except:
        user = User()
        user.username = user_data[0] #TODO: monkeypatch User model to allow long usernames
        user.email = user_data[0]
        user.first_name = user_data[1]
        user.last_name = user_data[2]
        user.save()
    return user


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

