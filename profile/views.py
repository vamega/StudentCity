from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import *
from django.template import RequestContext
from profile.models import Student, PrivacySettings
from profile.forms import StudentForm, PrivacySettingsForm

# Add profile app views here
def index(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    c["user"] = request.user
    # no user info is being passed right now; the template is simply being rendered
    return render_to_response("profile/personal.html", c)
    
    # TODO: write the "profile/personal.html" to accept POST data or cookies and show personal page, 
    #       then uncomment and adjust the below code to handle it
    
    # if logged in, redirect to personal profile
    #if request.method == 'POST':
    #    form = UserCreationForm(request.POST)
    #    if form.is_valid():
    #        # TODO: Add POST data (user info) to 'c' variable
    #        render_to_response("profile/personal.html", c)
    #else:
    #    return HttpResponseRedirect('/login')

def settings(request):
    c = {}
    c.update(csrf(request))
    c["user"] = request.user
    query_set = request.user.student_set.all()
    instance = None
    query_set2 = None
    for student in query_set:
        instance = student
        query_set2 = student.privacysettings_set.all()
    c["pi_form"] = StudentForm(request.POST or None, instance=instance)
    for settings in query_set2:
        instance = settings
    c["ps_form"] = PrivacySettingsForm(request.POST or None, instance=instance)
    return render_to_response("profile/settings.html", c, context_instance=RequestContext(request))
    
def edit_personal_info(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.save()
    return HttpResponseRedirect("/home/settings/")
    
def edit_privacy_settings(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = PrivacySettingsForm(request.POST)
        if form.is_valid():
            new_privacy_settings = form.save(commit=False)
            new_privacy_settings.save()
    return HttpResponseRedirect("/home/settings/")