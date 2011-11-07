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
    c['course_search_form'] = CourseSearchForm(request.GET or None)
    if request.GET.get("course_department") != u'':
        # TO DO: Implement legitimate search functionality here.
        # The following is simply a "proof-of-concept" of sorts allowing for demonstration.
        c['search_results'] = []
        if request.GET.get("course_department") == u'CSCI':
            c['num_results'] = 8
            for course in Course.objects.filter(course_department = u'CSCI'):
                for course_detail in course.coursedetail_set.all():
                    c['search_results'].append(course_detail)
            
    c['user'] = request.user
    c['student'] = request.user.student_set.all()[0]
    return render_to_response("profile/add_course.html", c, context_instance=RequestContext(request))

def add_course(request):
    c = {}
    c.update(csrf(request))
    if request.GET.get('dept') == u'' or request.GET.get('num') == u'':
        return HttpResponseRedirect("/home/course_search")
    logger.debug(request.GET.get('dept'), " ", request.GET.get('num'))
    s = request.user.student_set.all()[0]
    s.add_course(request.GET.get('dept'), request.GET.get('num'), request.GET.get('sec'), request.GET.get('sem'), request.GET.get('yr'), 'present')
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
