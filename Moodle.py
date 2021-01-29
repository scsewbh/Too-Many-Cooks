import requests
from bs4 import BeautifulSoup as bs
import os

data_keys = {"qazi": "32127", "tina": "32126", "arafat": "32123"}
moodle_url = 'https://lms.manhattan.edu/my/'
login_page = os.environ.get("LOGIN-URL")
course_base_link = 'https://lms.manhattan.edu/course/view.php?id='  # append course codes at end of url to get course page (5-digits code) (data-keys)


class Moodle:
    def __init__(self):
        self.session = requests.Session()
        self.session.get(moodle_url)
        r = self.session.get(login_page)
        if r.status_code == 200:
            print("Successful Login")
        else:
            print("Failed Login")

    def findCourse(self, course):
        # for key in data_keys:
        #    course_url = course_base_link+key
        # request

        testlink = course_base_link + data_keys[course]
        courseUnparsed = self.session.get(testlink)
        return courseUnparsed

    def parsingCourseData(self, dataUnparsed):
        soup = bs(dataUnparsed.text, 'html.parser')
        # for all activity instances check title name for File
        activityInstances = soup.findAll('div', {'class': 'activityinstance'})
        titleNameList = []
        hrefInstanceList = []
        for ai in activityInstances:   #Can change into a dictionary to match title to href instead of two separate arrays
            hrefInstance = ai.find('a', href=True).get('href')
            titleName = ai.find('span', {'class': 'instancename'}).text
            titleNameList.append(titleName)
            hrefInstanceList.append(hrefInstance)
        return titleNameList, hrefInstanceList
        # Forum, File (ppt,pdf,etc.), if none just a link, Assignment (HW), Page (Intructions)
        # Resources - ppt and docs and pdfs
        # Assignments/Project/Quiz

    def assignments(self, dataUnparsed):
        homeworks = {}
        assign = 'assignment'
        soup = bs(dataUnparsed.text, 'html.parser')
        # for all activity instances check title name for File
        activityInstances = soup.findAll('div', {'class': 'activityinstance'})
        for ai in activityInstances:
            titleName = ai.find('span', {'class': 'instancename'}).text
            if assign in titleName.lower(): #or hw in titleName.lower():
                hrefInstance = ai.find('a', href=True).get('href') #30 DAYs after due date dont include
                hwUnparsed = self.session.get(hrefInstance)
                soup = bs(hwUnparsed.text, 'html.parser')
                statusTable = soup.find('table', {'class': 'generaltable'})
                dueDate = statusTable.find('th', text='Due date')
                if dueDate is not None:
                    dd = dueDate.parent
                    due = dd.find('td').text
                    homeworks[titleName] = due, hrefInstance
                else:
                    homeworks[titleName] = "Friday, October 16, 2025, 11:00 PM", hrefInstance
        return homeworks

'''
instant = Moodle()
courseData = instant.findCourse('qazi')
instant.parsingCourseData(courseData)
instant.assignments(courseData)
'''
