from django.forms import ModelForm
from profile.models import Student

class StudentForm(ModelForm):
    class Meta:
        model = Student