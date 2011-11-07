from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext
from profile.models import *


# Add profile app views here
def index(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    if (not request.user.is_authenticated()) or (request.user == None):
        return HttpResponseRedirect("/")
    c["user"] = request.user
    c["student"] = request.user.student_set.all()[0]
    # no user info is being passed right now; the template is simply being rendered
    return render_to_response("profile/personal.html", c)

    
def settings(request):
    c = {}
    c.update(csrf(request))
    u = request.user 
    s = u.student_set.all()[0]
    if request.method == 'POST':
        info_form = PersonalInformationForm(request.POST, instance=s)
        if info_form.is_valid():
            info_form.save()
            '''
            s.first_name = info_form.first_name
            s.middle_name = info_form.middle_name
            s.last_name = info_form.last_name
            s.class_year = info_form.class_year
            s.profile_picture_url = info_form.profile_picture_url
            s.save()
            '''
    '''
    initial_form_vals = {
        'first_name'          : s.first_name,
        'middle_name'         : s.middle_name,
        'last_name'           : s.last_name,
        'class_year'          : s.class_year,
        'profile_picture_url' : s.profile_picture_url,
    }
    '''
    c["user"] = u
    c["student"] = s
    c["settings_form"] = PersonalInformationForm(instance=s)
    return render_to_response('profile/settings.html', c, context_instance=RequestContext(request))
