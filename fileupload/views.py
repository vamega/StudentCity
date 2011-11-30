from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext
from profile.models import *
from profile.forms import *
from django import forms
from fileupload.form import *
import logging

logger = logging.getLogger('testing')



# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file


def upload_file(request):
  
    c = {}
    c.update(csrf(request))
    
    if (not request.user.is_authenticated()) or (request.user == None):
      return HttpResponseRedirect("/?error=11")
    
    
    
        
##    search_options = {}
    
##    search_options['title'] = request.POST.get('title')
##    search_options['file'] = request.POST.get('file')
     
    
    if request.method == 'POST':
      #form = UploadFileForm(request.POST, request.FILES)
      form = c['UploadFileForm'] = UploadFileForm(request.POST, request.FILES, RequestContext(request))
      #if form.is_valid():
      if c['UploadFileForm'].is_valid():
        handle_uploaded_file(request.FILES['file'])
        return HttpResponseRedirect('fileupload/form')
        
    else:
        #form = UploadFileForm()
        form = c['UploadFileForm'] = UploadFileForm()
    return render_to_response('fileupload/upload.html', {'form': c['UploadFileForm']}, RequestContext(request))
    #return render_to_response('fileupload/upload.html', {'form': form})
##    return render_to_response('fileupload/upload.html', {'form': search_options}, c)


def handle_uploaded_file(f):
    destination = open('file.txt', 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
