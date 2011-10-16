from django.db import models

class Course(models.Model):
    course_department = models.CharField(max_length=16)
    course_number = models.IntegerField()
    course_name = models.CharField(max_length=256)
    course_description = models.TextField()
    
    def course_code(self):
        return course_department + " " + str(course_number)

class CourseDetail(models.Model):
    SEMESTER_CHOICES = (
        ('F', 'Fall'),
        ('S', 'Spring'),
    )
    course = models.ForeignKey(Course)
    year = models.CharField(max_length=4)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    section = models.IntegerField()

class Student(models.Model):
    rcs_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    class_year = models.CharField(max_length=4)
    rin = models.CharField(max_length=9)
    profile_picture_url = models.CharField(max_length=512)
    classes_current = models.ManyToManyField(Course)
    classes_taken = models.ManyToManyField(CourseDetail)
    
    def name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

class Teacher(models.Model):
    rcs_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    courses_taught = models.ManyToManyField(CourseDetail)
    def name(self):
        return self.first_name + self.middle_name + self.last_name
