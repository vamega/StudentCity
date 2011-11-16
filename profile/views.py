from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext
from profile.models import *
from profile.forms import *
import logging

logger = logging.getLogger('testing')

# Add profile app views here
def index(request):
    # csrf is used to prevent Cross-Site Request Forgeries (i.e. XSS attacks, SQL injections, etc.)
    c = {}
    c.update(csrf(request))


    if (not request.user.is_authenticated()) or (request.user == None):
        return HttpResponseRedirect("/?error=11")
    logger.debug(request.user.username or None)
    c["user"] = request.user or None
    c["student"] = request.user.student_set.all()[0] or None
    return render_to_response("profile/personal.html", c)
 

def course_search(request):
    c = {}
    c.update(csrf(request))

    c['course_search_form'] = CourseSearchForm(request.POST or None)
    
    search_options = {}
    
    search_options['course_department'] = request.POST.get('course_department')
    search_options['course_number'] = request.POST.get('course_number')
    search_options['year'] = request.POST.get('year')
    search_options['section'] = request.POST.get('section')
    
    #assert(False)
    
    new_options = {}
    for key in search_options:
        if search_options[key] != u'':
            if key.startswith('course'):
                new_key = 'course__' + key
                new_options[new_key] = search_options[key]
            else:
                new_options[key] = search_options[key]
    
    
    c['search_results'] = CourseDetail.objects.filter(**new_options)
    c['user'] = request.user
    c['student'] = request.user.student_set.all()[0]
    
    #c['debug'] = "Search options:\n\n" + str(new_options)
    return render_to_response("profile/add_course.html", c, context_instance=RequestContext(request))
    


def add_course(request):
    c = {}
    c.update(csrf(request))
    if request.POST.get('dept') == u'' or request.POST.get('num') == u'':
        return HttpResponseRedirect("/home/course_search", c)
    logger.debug(request.POST.get('dept'), " ", request.POST.get('num'))
    s = request.user.student_set.all()[0]
    s.add_course(request.POST.get('dept'), request.POST.get('num'), request.POST.get('sec'), request.POST.get('sem'), request.POST.get('yr'), 'present')
    s.save()
    return HttpResponseRedirect("/home/course_search/")

def course_group(request):
    course_code = request.POST.get('course_code')
    (department, s, number) = course_code.partition(' ')
    course_detail = CourseDetail.objects.all()
    # This isn't finished


    
def settings(request):
    c = {}
    c.update(csrf(request))
    if request.user.student_set.all().count() == 0:
        return HttpResponseRedirect("/?error=1")
    student = request.user.student_set.all()[0]
    privacy_settings = student.privacysettings_set.all()[0]
    
    c["user"] = request.user
    c["student"] = student
    c["personal_form"] = StudentForm(request.POST or None, instance=student)
    c["privacy_form"] = PrivacySettingsForm(request.POST or None, instance=privacy_settings)
    return render_to_response("profile/settings.html", c, context_instance=RequestContext(request))
    
    
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


def edit_personal_info(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        s = request.user.student_set.all()[0]
        form = StudentForm(request.POST, instance=s)
        if form.is_valid():
            new_personal_info = form.save(commit=False)
            new_personal_info.save()
        else:
            logger.debug("invalid form in edit_personal_info")

    return HttpResponseRedirect("/home/settings/")
    
def edit_privacy_settings(request):
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        p = request.user.student_set.all()[0].privacysettings_set.all()[0]
        form = PrivacySettingsForm(request.POST, instance=p)
        if form.is_valid():
            new_privacy_settings = form.save(commit=False)
            new_privacy_settings.save()
    return HttpResponseRedirect("/home/settings/")
    
def profile_page(request):
    c = {}
    c.update(csrf(request))

    if (not request.user.is_authenticated()) or (request.user == None):
        return HttpResponseRedirect("/?error=11")

    c["user"] = request.user or None
    c["student"] = request.user.student_set.all()[0] or None
    return render_to_response("profile/profile_page.html", c)



