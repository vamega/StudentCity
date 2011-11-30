from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.forms import * 
from django.template import RequestContext
from django import forms

class UploadFileForm(forms.Form):
    
    title = forms.CharField(max_length=50)
    file  = forms.FileField()
