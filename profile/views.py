from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import *
from django.template import RequestContext

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
    return render_to_response("profile/settings.html", {}, context_instance=RequestContext(request))
    
def search(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))
    
    if search.has_looked():
        return HttpResponseRedirect("profile/course_search")
    else:
	found_classes = {}
	found_dep = {}
	found_number = {}
	found_name = {}
	
        #c['search_form'] = SearchForm()
        
        for i in course_search.course_department:
	    if i == models.Model.course_department:
		temp = models.Model.course_department + ' ' + models.Model.course_number + ' ' + models.Model.course_name
		found_dep.append(temp)
		
	for i in course_search.course_number:
	    if i == models.Model.course_department:
		temp = models.Model.course_department + ' ' + models.Model.course_number + ' ' + models.Model.course_name
		found_number.append(temp)

	for i in course_search.course_name:
	    if i == models.Model.course_department:
		temp = models.Model.course_department + ' ' + models.Model.course_number + ' ' + models.Model.course_name
		found_name.append(temp)
	    
        
        if request.GET.get('error') == '1':
            c['error'] = 1
        
        
        return render_to_response('profile/course_search.html', c, context_instance=RequestContext(request))
