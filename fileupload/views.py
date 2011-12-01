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
  
    c = {}
    c.update(csrf(request))
    c['user'] = request.user
    
    if (not request.user.is_authenticated()) or (request.user == None):
      return HttpResponseRedirect("/?error=11")
    
    
     
    
    if request.method == 'POST':
      form = c['UploadFileForm'] = UploadFileForm(request.POST, request.FILES, RequestContext(request))

# If the form was valid build the dictionary and send to function to handle file upload
      if c['UploadFileForm'].is_valid():
	c['title'] = request.POST['title']
	c['course'] = request.POST['course']
        handle_uploaded_file(request.FILES['file'], c)
        return HttpResponseRedirect('fileupload/success.html')
        
    else:
        form = c['UploadFileForm'] = UploadFileForm()
    return render_to_response('fileupload/upload.html', {'form': c['UploadFileForm']}, RequestContext(request))



def handle_uploaded_file(f, c):
# location = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(16))

# Builds location to save uploaded file under the course number then title user inputed
    c['user'] = request.user
    location = 'static/userupload/'
    location += str(c['course'])
    location += '/'
    location += str(c['title'])
    destination = open(location, 'wb+')

    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
 
