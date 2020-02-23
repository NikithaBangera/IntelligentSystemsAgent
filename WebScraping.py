import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def course_name_extract(courses, course_number, course_subject, course_name, course_desc):
    #print(courses)
    reg_pattern = re.compile(r'[A-Z]\d\d -')
    for i in courses[1:]:
        #print(i.find_all("b"))
        data = i.getText().replace(u"\xa0", u" ")
        #print(data)
        if "Note:" in data:
            continue
        if reg_pattern.search(data):
            continue
        else:
            #print(data)
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
    for item in courses:
        item_clean = item.getText().replace(u"\xa0", u" ")
        #print(item_clean)
        
        if "**)" in item_clean:
            item_split = item_clean.strip().split(")", 2)
        elif "credits" in item_clean or "Credits" in item_clean:
            item_split = item_clean.strip().split("redits)", 2)
        elif "credit" in item_clean or "Credit" in item_clean:
            item_split = item_clean.strip().split("redit)", 2)

        if "value" in item_clean:
            item_split = item_clean.split("value)", 2)
        elif "(****)" in item_clean:
            item_split = item_clean.split("redits)", 2)

        #print(item_split)
        name_split = item_split[0].split("(",1)[0]
        #print(name_split)
        #print()
        desc = item_split[1]
        if name_split.strip().split(" ",2)[2] in course_name:
            #print(name_split.strip().split(" ",2)[2])
            index1 = course_name.index(name_split.strip().split(" ",2)[2])
            course_desc[index1] = desc.strip()
        else:
            course_subject.append(name_split.strip().split(" ", 2)[0])
            course_number.append(name_split.strip().split(" ", 2)[1])
            course_name.append(name_split.strip().split(" ", 2)[2])
            course_desc.append(desc.strip())

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
        course_name_extract(courses, course_number, course_subject, course_name, course_desc)

    #for i in range(51, 55):
    for i in range(55,56):
        courses = course_details[i].find_all(class_="large-text")
        #print(courses)
        courses_with_desc(courses, course_number, course_subject, course_name, course_desc)

    print(course_number)
    print(course_subject)
    print(course_name)
    print(course_desc)




grad_page = "http://www.concordia.ca/academics/graduate/calendar/current/encs/engineering-courses.html#topic"
webPageScraping(grad_page)