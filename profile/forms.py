from django import forms
from datetime import datetime
from django.forms import Form, ModelForm
from profile.models import *

"""
    These are the custom forms we developed to go along with our models.
"""

class StudentForm(ModelForm):
    """Generate a form used for saving personal data into the Student model."""
    class Meta:
        model = Student
        fields = ("rcs_id", "first_name", "middle_name", "last_name", "class_year", "profile_picture_url", "interests", "clubs")


class PrivacySettingsForm(ModelForm):
    """Generate a form used for saving student privacy settings into the PrivacySettings object."""
    class Meta:
        model = PrivacySettings
        exclude = ('student')


class CourseSearchForm(Form):
    """Generate a form used for searching the CourseDetail and Course model tables in the SQL database."""
    course_department = forms.CharField(max_length=16)
    course_number = forms.IntegerField(required=False)
    # TODO: Implement course_name search with substring comparison, etc.
    #course_name = forms.CharField()
    year = forms.CharField(max_length=4)
    semester = forms.ChoiceField(choices=SEMESTER_CHOICES)

    section = forms.IntegerField()

class RatingsForm(ModelForm):
    """Generate a form used for saving ratings data into the Ratings model."""
    course = forms.ModelChoiceField(queryset=CourseDetail.objects.all(),widget=forms.HiddenInput())
    rater = forms.ModelChoiceField(queryset=Student.objects.all(),widget=forms.HiddenInput())

    class Meta:
        model = Ratings
        exclude = ("timestamp")

class RecommendationsForm(ModelForm):
    """Generate a form used for saving recommendations data into the Recommendations model."""
    course = forms.ModelChoiceField(queryset=CourseDetail.objects.all(),widget=forms.HiddenInput())
    recommender = forms.ModelChoiceField(queryset=Student.objects.all(),widget=forms.HiddenInput())

    class Meta:
        model = Recommendations
        exclude = ("timestamp")

class MessageForm(ModelForm):
    """Generate a form used for sending a message and saving it in the Message model."""
    author = forms.ModelChoiceField(queryset=Student.objects.all(), widget=forms.HiddenInput())
    previous_message = forms.IntegerField(widget=forms.HiddenInput())
    recipients = forms.ModelMultipleChoiceField(queryset=Student.objects.filter(privacysettings__allow_others_to_send_me_messages__exact=True))

    class Meta:
        model = PrivateMessage
        exclude = ("timestamp", "read")

