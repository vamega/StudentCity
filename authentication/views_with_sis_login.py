# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext
from django.contrib import auth
import cookielib
import urllib, urllib2
import logging
import ssl

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
        # assert False
        if request.GET.get('error') == '1':
            c['error'] = 1
        return render_to_response('authentication/register.html', c, context_instance=RequestContext(request))

    
def register(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    
    # if logged in, redirect to personal profile
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/home")
        else:
            c['login_form'] = AuthenticationForm()
            c['register_form'] = UserCreationForm()
            return render_to_response('authentication/register.html', c, context_instance=RequestContext(request))
    else:
        c['login_form'] = AuthenticationForm()
        c['register_form'] = UserCreationForm()
        return render_to_response('authentication/register.html', c, context_instance=RequestContext(request))

def login(request):
    c = {}
    c.update(csrf(request))

    if request.method == 'POST':
        logger.debug("User Name = %s, Password = %s" %(request.POST.get("username"),request.POST.get("password")))
        user = auth.authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
        if user is not None and user.is_active:

	    #This code works but for some reason SIS will not allow it to login
            cj = cookielib.CookieJar()
            opener = urllib2.build_opener(urllib2.request.HTTPSHandler(), urllib2.HTTPCookieProcessor(cj))

            # urllib2.install_opener(urllib2.request.build_opener(urllib.request.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_TLSv1))))

            # login_data = urllib.urlencode({'username' : request.POST.get("username"), 'j_password' : request.POST.get("password")})
            login_data = urllib.urlencode({'username' : "vamega", 'j_password' : ""})
            opener.open('https://sis.rpi.edu/rss/twbkwbis.P_ValLogin', login_data)
            # opener.open('https://accounts.google.com/ServiceLogin?service=mail', login_data)
            resp = opener.open('https://sis.rpi.edu/rss/twbkwbis.P_GenMenu?name=bmenu.P_StuMainMnu')

            logger.debug(resp.read())

            auth.login(request, user)
            return HttpResponseRedirect("/home")
            
            
        else:
            return HttpResponseRedirect("/?error=1")
