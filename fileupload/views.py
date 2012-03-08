from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext
from profile.models import *
from profile.forms import *
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from fileupload.form import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import string
import random

import logging
logger = logging.getLogger('testing')



def upload_file(request):
    """ Get the course name, document title, and document location, returns a page redirect """
    c = {}
    c.update(csrf(request))
    
# Makes sure the user keeps their identity if they are not logged in redirect them to an error 11
    c['user'] = request.user
    c["student"] = request.user.student_set.all()[0]
    
    if (not request.user.is_authenticated()) or (request.user == None):
        return HttpResponseRedirect("/?error=11")
    
    
     
    # If the form has been submitted, Retrieve the inputes from form.html
    if request.method == 'POST':
        c['UploadFileForm'] = UploadFileForm(request.POST, request.FILES, RequestContext(request))

        # If the form was valid build the dictionary and send to function to handle file upload
        if c['UploadFileForm'].is_valid():
            c['title'] = request.POST['title']
            c['course'] = request.POST['course']
            handle_uploaded_file(request.FILES['file'], c)
            c['success'] = True
            
    # Else, Show the form for the user to enter data
    else:
        c['UploadFileForm'] = UploadFileForm()
        c['form'] = UploadFileForm()
    return render_to_response('fileupload/upload.html', c, RequestContext(request))



def handle_uploaded_file(f, c):
    """ Handles uploaded file, making the destination and uploading the file """   
    # Original way to name uploaded files  
    # location = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(16))

    # Builds location to save uploaded file under the course name then the title user inputed

    c['user'] = request.user
    location = 'static/userupload/'
    location += str(c['course'])
    location += '/'
    location += str(c['title'])
    destination = open(location, 'wb+')

    # Writes the file to the destination in chunks
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
