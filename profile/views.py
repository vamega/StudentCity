from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 


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
    return render_to_response("profile/settings.html")
