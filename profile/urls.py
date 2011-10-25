from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # /profile/ will call the profile index view, which is the user's personal profile
    (r'^$', 'profile.views.index'),
)
