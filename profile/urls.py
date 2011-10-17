from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    (r'^$', 'profile.views.index'),
)
