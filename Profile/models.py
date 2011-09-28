from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    classes = models.ForeignKey(Course)
    rin = models.CharField(max_length=9)
    email = models.CharField(max_length=128)
    profile_picture_url = models.CharField(max_length=512)
    
    def name(self):
        return self.first_name + self.middle_name + self.last_name

class Course(models.Model):
    course_id = models.CharField(max_length=16)
    course_name = models.CharField(max_length=256)
    section = models.IntegerField()
    professor = models.CharField(max_length=256)
