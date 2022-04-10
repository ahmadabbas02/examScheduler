import requests
import time
from bs4 import BeautifulSoup

from course import Course

URL = "https://stdportal.emu.edu.tr/examlist.asp"
# Replace the course codes according to your own courses
courses_list = ["CMPE242", "CMSE222", "SCIE223", "MATH322", "MATH373"]
courses_object_list = []

if __name__ == "__main__":
    if len(courses_list) == 0:
        print("Courses list is empty!")
        raise SystemExit(0)
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, "lxml")

    header_table = soup.find("table").find_all("font")
    header_list = [element.string.replace("\xa0", "")
                   for element in header_table]

    tables = soup.find_all("table")[1::]

    for index, table in enumerate(tables):
        period = table.find_previous("font").string.replace("Period : ", "")

        rows = table.find_all("tr")
        for row in rows:
            fonts = row.find_all("font")
            cells = (font.string.strip() for font in fonts)
            for index, cell in enumerate(cells):
                if len(cell) > 0 and cell in courses_list:
                    date = time.strptime(header_list[index], "%d %B %Y")
                    time_period = time.strptime(period, "%H:%M")
                    course_object = Course(
                        name=cell, date=date, time=time_period)
                    courses_object_list.append(course_object)

    if len(courses_object_list) == 0:
        print("We failed to find information related to the courses specified.")
        raise SystemExit(0)

    courses_object_list.sort(key=lambda x: (x.date, x.time))

    with open('schedule.txt', 'w') as f:
        f.write("{:<8} {:<11} {:<10}\n".format('Course', 'Date', 'Time'))

        for course_object in courses_object_list:
            course = course_object.name
            date = course_object.date
            date_string = time.strftime("%d/%m/%Y", date)

            period = course_object.time
            time_string = time.strftime("%H:%M", period)

            f.write("{:<8} {:<11} {:<10}\n".format(
                course, date_string, time_string))
    f.close()
