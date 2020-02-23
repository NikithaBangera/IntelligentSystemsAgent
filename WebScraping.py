import requests
from bs4 import BeautifulSoup
import pandas as pd


def course_name_extract(courses, course_number, course_subject, course_name, course_desc):
    #print(courses)
    for i in courses[1:]:
        #print(i.find_all("b"))
        data = i.getText().replace(u"\xa0", u" ")
        #print(data.strip())
        if "Note:" in data:
            continue
        else:
            if "\n" in data:
                #print(data)
                data_split = data.split("\n")
                #print(data_split)
                for l in data_split:
                    split_data = l.split("(",1)[0]
                    course_subject.append(split_data.strip().split(" ", 2)[0])
                    course_number.append(split_data.strip().split(" ", 2)[1])
                    course_name.append(split_data.strip().split(" ", 2)[2])
                    course_desc.append("")
            else:
                split_dt = data.split("(",1)[0]
                course_subject.append(split_dt.strip().split(" ", 2)[0])
                course_number.append(split_dt.strip().split(" ", 2)[1])
                course_name.append(split_dt.strip().split(" ", 2)[2])
                course_desc.append("")


def courses_with_desc(courses, course_number, course_subject, course_name, course_desc):
    '''a = courses[1].getText(strip=True).replace(u"\xa0", u" ")
    if "credits" in a:
        print(a.split("credits)", 2))'''
    for item in courses:
        print(item)
        item_clean = item.getText(strip=True).replace(u"\xa0", u" ")
        if "**)" in item_clean:
            item_split = item_clean.split(")", 2)
        elif "credits" in item_clean:
            item_split = item_clean.split("credits)", 2)
        elif "credit" in item_clean:
            item_split = item_clean.split("credit)", 2)

        name_split = item_split[0].split("(",1)[0]
        #print(name_split)
        #print(item_split[1])
        #if name_split.strip().split(" ",2)[0] in course_subject and name_split.strip().split(" ",2)[1] in course_number:
        '''if name_split.strip().split(" ",2)[2] in course_name:
            #print(name_split.strip().split(" ",2)[2])
            index1 = course_name.index(name_split.strip().split(" ",2)[2])
            course_desc[index1] = item_split[1]
        else:
            course_subject.append(name_split.strip().split(" ", 2)[0])
            course_number.append(name_split.strip().split(" ", 2)[1])
            course_name.append(name_split.strip().split(" ", 2)[2])
            course_desc.append(item_split[1])'''

def webPageScraping(grad_page):
    course_name = []
    course_subject = []
    course_number = []
    course_desc = []
    page = requests.get(grad_page)
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soap)
    section = soup.find(id="content-main")
    course_details = section.find_all(class_="wysiwyg parbase section")
    #course_details = course_details.find_all(class_="large-text")
    for i in range(3, 46):
        courses = course_details[i].find_all(class_="large-text")
        #print(courses)
        course_name_extract(courses, course_number, course_subject, course_name, course_desc)

    #for i in range(51, 52):
    for i in range(52,53):
        courses = course_details[i].find_all(class_="large-text")
        #print(courses)
        courses_with_desc(courses, course_number, course_subject, course_name, course_desc)

    '''print(course_number)
    print(course_subject)
    print(course_name)
    print(course_desc)'''




grad_page = "http://www.concordia.ca/academics/graduate/calendar/current/encs/engineering-courses.html#topic"
webPageScraping(grad_page)