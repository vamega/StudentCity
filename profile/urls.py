from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # /profile/ will call the profile index view, which is the user's personal profile
    (r'^$', 'profile.views.index'),
    (r'^/course_search/$', 'profile.views.course_search'),
    (r'^/add_course/$', 'profile.views.add_course'),
    (r'^/course_group/$', 'profile.views.course_group'),
    (r'^/settings/$', 'profile.views.settings'),
    (r'^/settings/edit_personal_info/', 'profile.views.edit_personal_info'),
    (r'^/settings/edit_privacy_settings/', 'profile.views.edit_privacy_settings'),
    (r'^/profile/(?P<student_id>\d+)/', 'profile.views.profile_page'),
    (r'^/ratings/(?P<course_id>\d+)/', 'profile.views.ratings'),
    (r'^/edit_ratings/', 'profile.views.edit_ratings'),
    (r'^/recommendations/(?P<course_id>\d+)/', 'profile.views.recommendations'),
    (r'^/edit_recommendations/', 'profile.views.edit_recommendations'),
)
