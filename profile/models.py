# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

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
    SEMESTER_CHOICES = (
        ('F', 'Fall'),
        ('S', 'Spring'),
    )
    course = models.ForeignKey(Course)
    year = models.CharField(max_length=4)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    section = models.IntegerField()
    professor = models.CharField(max_length=64)
    crn = models.PositiveIntegerField(unique=True)

    def __unicode__(self):
        return self.course.course_name + " " + self.semester + " " + self.year + " " + str(self.section)

class Student(models.Model):
    rcs_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    class_year = models.CharField(max_length=4)
    rin = models.CharField(max_length=9)
    profile_picture_url = models.CharField(max_length=512)
    classes_current = models.ManyToManyField(CourseDetail, related_name='current')
    classes_taken = models.ManyToManyField(CourseDetail, related_name='taken')
    

    def add_class(self, num, dept, name, sem, yr, sec, present_or_past):
        class_taken, created = Course.objects.get_or_create(course_number=num, course_department=dept, course_name=name)
        class_section, created = CourseDetail.objects.get_or_create(course=class_taken, semester=sem, year=yr, section=sec)
        if (present_or_past == 'present'):
            self.classes_current.add(class_section)
        else:
            self.classes_taken.add(class_section)
    
    def name(self):
        return self.first_name + " " + self.middle_name + " " + self.last_name

    def __unicode__(self):
        return self.rcs_id

class Teacher(models.Model):
    rcs_id = models.CharField(max_length=128)
    first_name = models.CharField(max_length=256)
    middle_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    courses_taught = models.ManyToManyField(CourseDetail)
    
    def name(self):
        return self.first_name + self.middle_name + self.last_name

    def __unicode__(self):
        return self.rcs_id
