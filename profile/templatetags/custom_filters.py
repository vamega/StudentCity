from django import template
import os


register = template.Library()

@register.filter
def strip_spaces(string): 
    return string.replace(' ', '')
    
@register.filter
def get_resources(string):
   return os.listdir('static/userupload/' + str(string))