from django.conf.urls.defaults import *
from views import *

"""
  A url beginning with /home/ will be redirected to this profile app url list.
"""

urlpatterns = patterns('',
    # View the user's homepage.
    (r'^$', 'profile.views.index'),
    # Search for a course in the database.
    (r'^/course_search/$', 'profile.views.course_search'),
    # Register a student for a course.
    (r'^/add_course/$', 'profile.views.add_course'),
    # View a course group.
    (r'^/course_group/$', 'profile.views.course_group'),
    # View and change your profile and privacy settings.
    (r'^/settings/$', 'profile.views.settings'),
    # Save changes to a Student profile.
    (r'^/settings/edit_personal_info/', 'profile.views.edit_personal_info'),
    # Save changes to privacy settings.
    (r'^/settings/edit_privacy_settings/', 'profile.views.edit_privacy_settings'),
    # View a user's public profile.
    (r'^/profile/(?P<student_id>\d+)/', 'profile.views.profile_page'),
    # View past ratings for a course.
    (r'^/ratings/(?P<course_id>\d+)/', 'profile.views.ratings'),
    # Save a new rating record for a course.
    (r'^/edit_ratings/', 'profile.views.edit_ratings'),
    # View past reccomendations for a course.
    (r'^/recommendations/(?P<course_id>\d+)/', 'profile.views.recommendations'),
    # Save a new reccomendation record for a course.
    (r'^/edit_recommendations/', 'profile.views.edit_recommendations'),
    # View your private messages.
    (r'^/message/(?P<student_id>\d+)/(?P<previous_message_id>\d+)/', 'profile.views.message'),
    # Send a private message.
    (r'^/send_message/', 'profile.views.send_message'),
    # View a specific private message.
    (r'^/view_message/(?P<message_id>\d+)/', 'profile.views.view_message'),
    # Create a new study group.
    (r'^/create_study_group/', 'profile.views.create_study_group'),
    # View a study group's details and members.
    (r'^/view_study_group/(?P<study_group>\w+)/', 'profile.views.view_study_group'),
    # Make a reccomendation for a course.
    (r'^/course_recommendation/(?P<student_id>\d+)/', 'profile.views.course_recommendation'),
)
