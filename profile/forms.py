from django import forms
from datetime import datetime
from django.forms import Form, ModelForm
from profile.models import *

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ("rcs_id", "first_name", "middle_name", "last_name", "class_year", "profile_picture_url", "interests", "clubs")


class PrivacySettingsForm(ModelForm):
    class Meta:
        model = PrivacySettings
        exclude = ('student')


class CourseSearchForm(Form):
    course_department = forms.CharField(max_length=16)
    course_number = forms.IntegerField(required=False)
    # TODO: Implement course_name search with substring comparison, etc.
    #course_name = forms.CharField()
    year = forms.CharField(max_length=4)
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES)

    section = forms.IntegerField()
    
class RatingsForm(ModelForm):
    course = forms.ModelChoiceField(queryset=CourseDetail.objects.all(),widget=forms.HiddenInput())
    rater = forms.ModelChoiceField(queryset=Student.objects.all(),widget=forms.HiddenInput())
    #timestamp = forms.DateTimeField(datetime.now,widget=forms.HiddenInput())

    class Meta:
        model = Ratings

class RecommendationForm(ModelForm):
    class Meta:
        model = Recommendations
        fields = ('would_recommend_course', 'comments')