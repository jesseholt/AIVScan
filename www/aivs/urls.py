from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', direct_to_template, { 'template': 'index.html' }),
                       url(r'^about$', direct_to_template, { 'template': 'about.html' }),
                       url(r'^contact$', direct_to_template, { 'template': 'contact.html' }),
                       url(r'^.*$', direct_to_template, { 'template': 'index.html' }), #fallback
#    url(r'^admin/', include(admin.site.urls)),
)
