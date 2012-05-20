from django.contrib.sites.models import RequestSite

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default import DefaultBackend

'''
This module overrides selected methods of the default django-registration backend.
'''

class AivsBackend(DefaultBackend):

    def register(self, request, **kwargs):
        '''
        We want to use the email address of the user as the user name and save the first name and last
        name in the first pass, rather than having the user come back to do it later.  This method is
        otherwise identical to the one overriden in DefaultBackend.
        '''
        first_name, last_name = kwargs['first_name'], kwargs['last_name']
        email, password = kwargs['email'], kwargs['password']
        user_name = email
        site = RequestSite(request)

        new_user = RegistrationProfile.objects.create_inactive_user(user_name, email, password, site)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
