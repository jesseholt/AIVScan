from django.contrib import admin
from aivs.models import ScanResult

'''
This module registers our ORM classes with the Django admin.
'''

admin.site.register(ScanResult)
