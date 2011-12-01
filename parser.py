from BeautifulSoup import BeautifulStoneSoup
from profile.models import *
import urllib2

def parseSemesterData(semesterData):
    desc = semesterData.split(' ')

    semester = None

    if desc[0] == 'Spring':
        semester = 'S'
    elif desc[0] == 'Fall':
        semester = 'F'
    else:
        semester = 'B'

    year = int(desc[1])

    return semester,year

def getCourseData(url):
    doc = urllib2.urlopen(url)
    soup = BeautifulStoneSoup(doc)

    root = soup.find('coursedb')
    semester, year = parseSemesterData(root['semesterdesc'])
    courses = soup.findAll('course')

    for currCourse in courses:
        course = Course()

        course.course_name = currCourse['name']
        course.course_number = currCourse['num']
        course.course_department = currCourse['dept']
        course.save()

        sections = currCourse.findAll('section')

        for currSection in sections:
            if currSection['seats'] == '0':
                continue

            professor_names = list()
            for period in currSection.findAll('period'):
                professor_names = period['instructor'].split("/")

            details = CourseDetail()
            details.course = course
            details.year = year
            details.semester = semester

            try:
                section = int(currSection['num'])
            except ValueError:
                section = -1

            details.section = section

            details.crn = currSection['crn']
            details.save()

            for professor_name in professor_names:
                professor = None
                try:
                    professor = Teacher.objects.get(last_name=professor_name)
                except Teacher.DoesNotExist:
                    professor = Teacher(last_name=professor_name)
                    professor.save()

                details.professor.add(professor)
            
            details.save()