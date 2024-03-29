from django.conf import settings
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import  logout
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

'''
    This file defines a tuple that Django uses to direct HTTP Requests to the proper view.
    Note that 'profile.urls' is included for the '^home' regex.
    This means that any urls of the form "http://www.StudentCityURL.com/home/..." are redirected to the profile module.
'''

urlpatterns = patterns('',
    # The main login/register page
    url(r'^$', 'authentication.views.index'),
    # The view that handles the registration of a new user
    url(r'^register/', 'authentication.views.register'),

    # The view that will one day handle user login
    url(r'^login', 'authentication.views.login'),
    # The view that handles user logout
    url(r'^logout', logout),

    # The profile views, imported from profile/urls.py
    url(r'^home', include('profile.urls')),
    
    # The admin site
    url(r'^admin/', include(admin.site.urls)),
    # The admin docs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Serving static files
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    
    # File Upload
    (r'^fileupload/', 'fileupload.views.upload_file'),
)

