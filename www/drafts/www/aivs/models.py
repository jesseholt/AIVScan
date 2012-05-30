from Crypto.Cipher import Blowfish
import base64

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

'''
This module defines the object-relational mapping between Python/Django objects and the MySQL
database.  The User model provided by the Django auth module already contains all the information
we want about our users.
'''


class ScanResult(models.Model):
    '''
    Defines the results of a completed scan.  We have symmetrically-encrypted the scan results.
    Note that this only protects the database as a standalone entity (ex. if backup drives are stolen).
    Because the application needs to be able to read-in unencrypted values, there is no way to prevent
    someone who compromises the application from accessing the unencrypted database values.  If
    we want to encrypt additional information, it might make more sense to override the TextField
    model field with an EncryptedTextField to eliminate the need to create accessors for each field.
    '''
    user = models.ForeignKey(User)
    completion_dt = models.DateTimeField()

    # note: don't call for scan_results directly; use propery accessor methods defined below
    # so that we're setting/getting encrypted values.  Other than encryption, the results are just
    # getting stored in a text blob for now.
    scan_results = models.TextField()

    def _get_results(self):
        blowfish = Blowfish.new(settings.SECRET_KEY)
        encrypted = base64.b64decode(self.scan_results)
        decrypted = u'{0}'.format(blowfish.decrypt(encrypted).rstrip())
        return decrypted

    def _set_results(self, results_value):
        blowfish = Blowfish.new(settings.SECRET_KEY)
        padding = ' ' * (8 - (len (val) % 8)) # algorithm requires multiples of 8 chars
        unencrypted = results_value + padding
        encrypted = base64.b64encode(blowfish.encrypt(results_value))
        self.scan_results = encrypted

    results = property(_get_results, _set_results)
