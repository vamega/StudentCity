from django import template


register = template.Library()

@register.filter
def strip_spaces(string): 
    return string.replace(' ', '')