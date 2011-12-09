from django.utils import unittest
from profile.models import *
import parser

class MyFuncTestCase(django.test.TestCase):
    
    def testgetCourseData(self):
        oldNum = len(Course.objects.all)
        parser.getCourseData("http://50.115.160.86/static/testCourseData.xml")
        newNum = len(Course.objects.all)

        self.assertNotEqual(oldNum, newNum)