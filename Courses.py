import requests
from bs4 import BeautifulSoup
import pandas as pd
from rdflib.namespace import RDFS, RDF, FOAF, DC, DCTERMS
from rdflib import Graph, Namespace, Literal
import csv

graph = Graph()
graph.parse("Classes.rdf", format="application/rdf+xml")

def webPageScraping():
    page = requests.get("https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html#course-descriptions")
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soap)
    section = soup.find(id="content-main")
    course_desc = section.find_all(class_="wysiwyg parbase section")
    courses = course_desc[2].find_all("p")
    # print(courses)
    course_name = []
    course_subject = []
    course_number = []
    course_desc = []
    for i in range(2, len(courses)):
        courses_split = courses[i].find(class_="large-text").getText(strip=True).replace(u"\xa0", u" ").split(")", 2)
        # print (courses_split)
        cname_split = courses_split[0].split("(")[0]
        courses_split.pop(0)
        # print (courses_split)
        if len(courses_split)>1:
          x=courses_split[1]
        else:
          x=courses_split[0]
        course_desc.append(x)
        course_subject.append(cname_split.split(" ", 2)[0])
        course_number.append(cname_split.split(" ", 2)[1])
        course_name.append(cname_split.split(" ", 2)[2])

    '''print(course_subject)
    print(course_number)
    print(course_name)
    print(course_desc)'''

    df = pd.DataFrame(
        {'course_number': course_number,
         'course_name': course_name,
         'course_subject': course_subject,
         'course_desc':course_desc
        })
    df.to_csv('Courses.csv', index=False, sep='|')


def courseTripleGenerator(course_class):
    course_ns = Namespace("http://example.org/course/")
    course_graph = Graph()
    with open("Courses.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for course_list in file_reader:
            #print(course_list)
            course = course_ns[course_list[0]+"_"+course_list[2]]
            course_graph.add((course, RDF.type, course_class))
            course_graph.add((course, DC.identifier, Literal(course_list[0])))
            course_graph.add((course, DC.title, Literal(course_list[1])))
            course_graph.add((course, DC.subject, Literal(course_list[2])))
            course_graph.add((course, DC.description, Literal(course_list[3])))

    #print(course_graph.serialize(format='turtle'))

def universityTripleGenerator():
    university_graph = Graph()
    university =
    uni

webPageScraping()

subject = list(graph.subjects(RDF.type, RDFS.Class))
#print(subject)
for row in subject:
    if "#Courses" in row:
        course_class = row
    if "#University" in row:
        university_class = row

courseTripleGenerator(course_class)
universityTripleGenerator(university_class)