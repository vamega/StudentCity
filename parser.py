from django.conf import settings
from BeautifulSoup import BeautifulStoneSoup
from profile.models import *
import urllib2
import sys
import os
import re

def parse_semester_data(semester_data):
    """Parse the semester and year from the semesterDesc attribute of the CourseDB tag in the XML.

    semester_data is the contents of the semesterDesc attribute

    This function returns a tuple of the semester and year of the related CourseDB
    """

    description = semester_data.split(' ')

    semester = None

    if description[0] == 'Spring':
        semester = 'S'
    elif description[0] == 'Fall':
        semester = 'F'
    else:
        semester = 'B'

    year = int(description[1])

    return semester,year

def get_course_data(url):
    """Parse a CourseDB from SIS' course data XML file.

    url is a url to a CourseDB XML file.

    This function modified the database to include add courses, courseDetails and professors that are described in the xml file.
    """
    doc = open(url)
    # print doc.read()
    soup = BeautifulStoneSoup(doc)

    root = soup.find('coursedb')
    semester, year = parse_semester_data(root['semesterdesc'])
    courses = soup.findAll('course')

    for current_course in courses:
        course = None

        try:
            course = Course.objects.get(course_department=current_course['dept'], course_number=current_course['num'])
        except Course.DoesNotExist:
            course = Course()
            name = re.sub('[^a-zA-Z0-9 ]', '', current_course['name'])
            course.course_name = name
            course.course_number = current_course['num']
            course.course_department = current_course['dept']
            course.save()
            
            try:
                os.mkdir( os.path.join(settings.USER_UPLOAD_DIR, name) )
            except:
                pass

        sections = current_course.findAll('section')

        for current_section in sections:
            if current_section['seats'] == '0':
                continue

            professor_names = list()
            for period in current_section.findAll('period'):
                professor_names = period['instructor'].split("/")

            details = CourseDetail()
            details.course = course
            details.year = year
            details.semester = semester

            try:
                section = int(current_section['num'])
            except ValueError:
                section = -1

            details.section = section

            details.crn = current_section['crn']
            
            try:
                details.save()
            except:
                continue

            for professor_name in professor_names:
                professor = None
                try:
                    professor = Teacher.objects.get(last_name=professor_name)
                except Teacher.DoesNotExist:
                    professor = Teacher(last_name=professor_name)
                    professor.save()

                details.professor.add(professor)
            
            details.save()


if __name__ == "__main__":
    url = None
    if(len(sys.argv) == 1):
        print "No URL supplied. Running on test URL."
        url = 'http://50.115.160.86/static/testCourseData.xml'
        print "Test URL - %s"%url
    else:
        url = sys.argv[1]
    
    print url
    get_course_data(url)
