from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

'''
This module monkey patches the validator for usernames so that they are suitably long enough to
contain email addresses.  This code is per the StackOverflow discussion here:
http://stackoverflow.com/questions/2610088/can-djangos-auth-user-username-be-varchar75-how-could-that-be-done

To modify the table:
django-admin.py dbshell
alter table auth_user modify column username varchar(200);
'''

NEW_USERNAME_LENGTH = 200

def monkey_patch_username():
    username = User._meta.get_field('username')
    username.max_length = NEW_USERNAME_LENGTH
    for v in username.validators:
        if isinstance(v, MaxLengthValidator):
            v.limit_value = NEW_USERNAME_LENGTH

monkey_patch_username()
