from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext

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


def index(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    
    # TODO: create authentication test; if logged in, redirect to personal profile
    if False:
        # TODO: redirect to profile once it works
        pass
    else:
        c['login_form'] = AuthenticationForm()
        c['register_form'] = UserCreationForm()
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
