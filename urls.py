from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'authentication.views.index'),
    url(r'^login', 'authentication.views.index'),
    url(r'^home', include('profile.urls')),
    
    # admin
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # delete before pushing
    (r'^static_files/(?P<path>.*)$', 
        'serve', {
            'document_root': 'C:/Users/bellok/code/classes/sdd/StudentCity/static_files/',
            'show_indexes': True 
        }
    ),
)

'''
try:
    from local_urls import *
except ImportError:
    pass
'''