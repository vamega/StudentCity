import django.forms
from django.forms import Form, ModelForm
from profile.models import *


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ('first_name', 'middle_name', 'last_name', 'rcs_id', 'class_year', 'profile_picture_url')
        
class PrivacySettingsForm(ModelForm):
    class Meta:
        model = PrivacySettings
        exclude = ('student')


class CourseSearchForm(Form):
    course_department = forms.CharField()
    course_number = forms.IntegerField(required=False)
    # TODO: Implement course_name search with substring comparison, etc.
    #course_name = forms.CharField()
    