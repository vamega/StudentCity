from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.contrib import auth
from profile.models import *
import logging

# Builtin django forms imported:
# - class AdminPasswordChangeForm
#       A form used in the admin interface to change a user's password.
# - class AuthenticationForm
#       A form for logging a user in.
# - class PasswordChangeForm
#       A form for allowing a user to change their password.
# - class PasswordResetForm
#       A form for generating and emailing a one-time use link to reset a user's password.
# - class SetPasswordForm
#       A form that lets a user change his/her password without entering the old password.
# - class UserChangeForm
#       A form used in the admin interface to change a user's information and permissions.
# - class UserCreationForm
#       A form for creating a new user.

logger = logging.getLogger('testing')

def index(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    
    # TODO: create authentication test; if logged in, redirect to personal profile
    if request.user.is_authenticated():
        return HttpResponseRedirect("/home")
    else:
        c['login_form'] = AuthenticationForm()
        c['register_form'] = UserCreationForm()
        
        if request.GET.get('error') == '1':
            c['error'] = 1
        return render_to_response('authentication/register.html', c, context_instance=RequestContext(request))

    
def register(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    
    error_string = ''
    # if logged in, redirect to personal profile
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Make a new user
            new_user = form.save()
            logger.debug("Valid new user found:\t" + new_user.username)
            student = Student(user=new_user)
            student.save()
            privacy = PrivacySettings(student=student)
            privacy.save()
            user = auth.authenticate(username=request.POST.get("username"), password=request.POST.get("password1"))
            auth.login(request, user)
            return HttpResponseRedirect("/home")
        else:
            logger.debug("Invalid form. Probably this user already exists.")
            error_string = '?error=3'
    return HttpResponseRedirect("/"+error_string)

def login(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        logger.debug("User Name = %s, Password = %s" %(request.POST.get("username"),request.POST.get("password")))
        user = auth.authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/home")
        else:
            return HttpResponseRedirect("/?error=1")
    
