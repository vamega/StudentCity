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

    class Meta:
        model = Ratings
        exclude = ("timestamp")

class RecommendationsForm(ModelForm):
    course = forms.ModelChoiceField(queryset=CourseDetail.objects.all(),widget=forms.HiddenInput())
    recommender = forms.ModelChoiceField(queryset=Student.objects.all(),widget=forms.HiddenInput())

    class Meta:
        model = Recommendations
        exclude = ("timestamp")

class MessageForm(ModelForm):
    author = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput())
    previous_message = forms.IntegerField(widget=forms.HiddenInput())
    recipients = forms.ModelMultipleChoiceField(queryset=Student.objects.filter(privacysettings__allow_others_to_send_me_messages__exact=True))

    class Meta:
        model = PrivateMessage
        exclude = ("timestamp", "read")