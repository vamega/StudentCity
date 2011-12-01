# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.forms import ModelForm

SEMESTER_CHOICES = (
    ('F', 'Fall'),
    ('S', 'Spring'),
    ('B', 'Summer')
)

RECOMMEND_COURSE_CHOICES = (
    ('Y', 'Yes'),
    ('N', 'No'),
)

RATINGS_CHOICES = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
)


class Course(models.Model):
    course_department = models.CharField(max_length=16)
    course_number = models.IntegerField()
    course_name = models.CharField(max_length=256)
    course_description = models.TextField()
    
    def course_code(self):
        return self.course_department + " " + str(self.course_number)

    def get_num_students(self, past_or_present):
        date_time = datetime.now()
        if date_time.month in (1, 2, 3, 4, 5, 6):
            sem = 'S'
        else:
            sem = 'F'
        yr = date_time.year
        count = 0
        if (past_or_present == 'present'):
            course_detail = self.coursedetail_set.filter(year__exact=yr, semester__exact=sem)
            for cd in course_detail:
                count += cd.current.count()
        elif (past_or_present == 'past'):
            course_detail = self.coursedetail_set.exclude(year__exact=yr, semester__exact=sem)
            for cd in course_detail:
                count += cd.taken.count()
        return count

    def __unicode__(self):
        return self.course_name


class CourseDetail(models.Model):
    course = models.ForeignKey(Course)
    year = models.CharField(max_length=4)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    section = models.IntegerField()
    professor = models.ManyToManyField('Teacher')
    crn = models.PositiveIntegerField(unique=True)

    def __unicode__(self):
        return self.course.course_name + " " + self.semester + " " + self.year + " " + str(self.section)
    
    def get_num_current_students(self):
        num = self.course.get_num_students(past_or_present='present')
        return num

    def get_num_past_students(self):
        num = self.course.get_num_students(past_or_present='past')
        return num

class Student(models.Model):
    user = models.ForeignKey(User, unique=True)
    rcs_id = models.CharField(max_length=128)
    rin = models.CharField(max_length=9)


    first_name = models.CharField(max_length=256, blank=True)
    middle_name = models.CharField(max_length=256, blank=True)
    last_name = models.CharField(max_length=256, blank=True)
    class_year = models.CharField(max_length=4, blank=True)
    interests = models.TextField(max_length=1280, blank=True)
    clubs = models.TextField(max_length=1280, blank=True)
    profile_picture_url = models.URLField(blank=True, default='http://localhost:8000/static/images/default_profile_picture.png')
    classes_current = models.ManyToManyField(CourseDetail, related_name='current')
    classes_taken = models.ManyToManyField(CourseDetail, related_name='taken')

    def add_course(self, dept, num, section, semester, year, present_or_past):
        course = Course.objects.get(course_number=num, course_department=dept)
        course_detail = CourseDetail.objects.get(course=course, semester=semester, year=year, section=section)
        if (present_or_past == 'present'):
            self.classes_current.add(course_detail)
        else:
            self.classes_taken.add(course_detail)

    def name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

    def __unicode__(self):
        return self.rcs_id

class Teacher(models.Model):
    rcs_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    courses_taught = models.ManyToManyField(CourseDetail)
    def name(self):
        return self.first_name + self.last_name
    def __unicode__(self):
        return self.rcs_id

class PrivacySettings(models.Model):
    student = models.ForeignKey(Student, unique=True)
    allow_others_to_view_profile_picture = models.BooleanField()
    allow_others_to_view_interests = models.BooleanField()
    allow_others_to_view_clubs = models.BooleanField()
    allow_others_to_send_me_messages = models.BooleanField()
    allow_others_to_send_me_email = models.BooleanField()
    allow_others_to_view_classes = models.BooleanField()

    
class PrivateMessage(models.Model):
    author = models.ForeignKey(Student, related_name='PM_author')
    recipients = models.ManyToManyField(Student, related_name='PM_recipients')
    subject = models.CharField(max_length=256)
    contents = models.TextField()
    read = models.BooleanField()
    previous_message = models.PositiveIntegerField(blank=True)
    timestamp = models.DateTimeField()
    
class GroupPost(models.Model):
    author = models.ForeignKey(User)
    group = models.ForeignKey(Course)
    contents = models.TextField()
    timestamp = models.TimeField()

class Ratings(models.Model):
    course = models.ForeignKey(CourseDetail)
    rater = models.ForeignKey(Student)
    easiness = models.IntegerField(choices=RATINGS_CHOICES)
    course_material = models.IntegerField(choices=RATINGS_CHOICES)
    course_subject_interest = models.IntegerField(choices=RATINGS_CHOICES)
    timestamp = models.DateTimeField(default=datetime.now)

class Recommendations(models.Model):
    course = models.ForeignKey(CourseDetail)
    recommender = models.ForeignKey(Student)
    would_recommend_course = models.CharField(max_length=1, choices=RECOMMEND_COURSE_CHOICES)
    comments = models.TextField(max_length=256, blank=True)
    timestamp = models.DateTimeField(default=datetime.now)

class StudyGroup(models.Model):
    course = models.ForeignKey(Course)
    members = models.ManyToManyField(Student)
    name = models.CharField(max_length=256)

