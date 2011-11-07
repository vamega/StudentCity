from django.forms import ModelForm
from profile.models import Student, PrivacySettings

class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ("rcs_id", "first_name", "middle_name", "last_name", "class_year", "rin")
        
class PrivacySettingsForm(ModelForm):
    class Meta:
        model = PrivacySettings