from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # /profile/ will call the profile index view, which is the user's personal profile
    (r'^$', 'profile.views.index'),
    (r'^/course_search/$', 'profile.views.course_search'),
    (r'^/add_course/$', 'profile.views.add_course'),
    (r'^/settings/$', 'profile.views.settings'),
    (r'^/settings/edit_personal_info/', 'profile.views.edit_personal_info'),
    (r'^/settings/edit_privacy_settings/', 'profile.views.edit_privacy_settings')

)
