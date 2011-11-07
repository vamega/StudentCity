from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 


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
    return render_to_response("profile/settings.html")
