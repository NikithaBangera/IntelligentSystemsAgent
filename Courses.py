import requests
from bs4 import BeautifulSoup
import pandas as pd
from rdflib.namespace import RDFS, RDF, FOAF, DC, OWL
from rdflib import Graph, Namespace, Literal
import csv

graph = Graph()
graph.parse("Classes.rdf", format="application/rdf+xml")


def webPageScraping(comp_grad_page):
    page = requests.get(comp_grad_page)
    soup = BeautifulSoup(page.content, "html.parser")
    #print(soap)
    section = soup.find(id="content-main")
    course_details = section.find_all(class_="wysiwyg parbase section")
    courses = course_details[2].find_all("p")
    course_name_list = course_details[0].find_all(class_="large-text")
    #print(course_name_list)

    course_name = []
    course_subject = []
    course_number = []
    course_desc = []
    for i in range(2, len(courses)):
        courses_split = courses[i].find(class_="large-text").getText(strip=True).replace(u"\xa0", u" ").split(")", 2)
        # print (courses_split)
        cname_split = courses_split[0].split("(")[0]
        courses_split.pop(0)
        #print(courses_split)
        if len(courses_split)>1:
          x=courses_split[1]
        else:
          x=courses_split[0]
        course_desc.append(x)
        course_subject.append(cname_split.split(" ", 2)[0])
        course_number.append(cname_split.split(" ", 2)[1])
        course_name.append(cname_split.split(" ", 2)[2])

    courses_list = []
    for j in range(1, len(course_name_list), 2):
        courses = course_name_list[j].find_all("b")
        #print(courses)
        for k in courses:
            data = k.getText().replace(u"\xa0", u" ").strip()
            if "\n" in data:
                data_split = data.split("\n")
                for l in data_split:
                    courses_list.append(l)
            else:
                courses_list.append(data)

    #print(courses_list)
    for items in courses_list:
        item_spl = items.split("(",1)
        items_split = item_spl[0].split(" ", 2)
        #print(items_split[2])
        #if items_split[0] in course_subject and items_split[1] in course_number:
        if items_split[2] in course_name:
            #print("yes")
            continue
        else:
            course_desc.append("")
            course_subject.append(items_split[0])
            course_number.append(items_split[1])
            course_name.append(items_split[2])

    '''print(course_subject)
    print(course_number)
    print(course_name)
    print(course_desc)'''

    df = pd.DataFrame(
        {'course_number': course_number,
         'course_name': course_name,
         'course_subject': course_subject,
         'course_desc': course_desc
        })
    df.to_csv('Courses.csv', index=False, sep='|')


def universityTripleGenerator(university_class):
    university_ns = Namespace("http://example.org/university/")
    university_graph = Graph()
    university_list = ["Concordia_University"]
    university = university_ns[university_list[0]]
    university_graph.add((university, RDF.type, university_class))
    university_graph.add((university, FOAF.name, Literal("Concordia University")))
    university_graph.add((university, RDFS.seeAlso, Literal("http://dbpedia.org/resource/Concordia_University")))
    # print(university_graph.serialize(format='turtle'))
    return university


def courseTripleGenerator(course_class, comp_grad_page, is_offered_by, university):
    course_ns = Namespace("http://example.org/course/")
    course_graph = Graph()
    with open("Courses.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for course_list in file_reader:
            #print(course_list)
            course = course_ns[course_list[2]+"_"+course_list[0]]
            course_graph.add((course, RDF.type, course_class))
            course_graph.add((course, DC.identifier, Literal(course_list[0])))
            course_graph.add((course, DC.title, Literal(course_list[1])))
            course_graph.add((course, DC.subject, Literal(course_list[2])))
            course_graph.add((course, DC.description, Literal(course_list[3])))
            course_graph.add((course, RDFS.seeAlso, Literal(comp_grad_page)))
            course_graph.add((course, is_offered_by, Literal(university)))


    #print(course_graph.serialize(format='turtle'))


def topicsTripleGenerator(topic_class):
    topic_ns = Namespace("http://example.org/topics/")
    topic_graph = Graph()
    with open("topic.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for topic_list in file_reader:
            if " " in topic_list[0]:
                topic_name = topic_list[0].split(" ")[0] + "_" + topic_list[0].split(" ")[1]
            else:
                topic_name = topic_list[0]
            topic = topic_ns[topic_name]
            topic_graph.add((topic, RDF.type, topic_class))
            topic_graph.add((topic, DC.title, Literal(topic_list[0])))
            topic_graph.add((topic, RDFS.seeAlso, Literal(topic_list[1])))
            topic_graph.add((topic, FOAF.isPrimaryTopicOf, Literal(topic_list[2])))

    #print(topic_graph.serialize(format='turtle'))


def studentTripleGenerator(student_class, enrolled_property, takes_course_property, is_awarded, university, has_transcript, transcript):
    student_ns = Namespace("http://example.org/people/")
    student_graph = Graph()
    with open("StudentsRecord.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for student_list in file_reader:
            #print(student_list)
            student = student_ns[student_list[0]]
            student_graph.add((student, RDF.type, student_class))
            student_graph.add((student, FOAF.studentId, Literal(student_list[0])))
            student_graph.add((student, FOAF.givenName, Literal(student_list[1])))
            student_graph.add((student, FOAF.familyName, Literal(student_list[2])))
            student_graph.add((student, FOAF.mbox, Literal(student_list[3])))
            student_graph.add((student, takes_course_property, Literal(student_list[4])))
            student_graph.add((student, is_awarded, Literal(student_list[5])))
            student_graph.add((student, enrolled_property, university))
            student_graph.add((student, has_transcript, transcript))

    #print(student_graph.serialize(format='turtle'))


def transcriptTripleGenerator(transcript_class):
    transcript_ns = Namespace("http://example.org/transcript/")
    transcript_graph = Graph()
    with open("transcript.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for transcript_list in file_reader:
            # print(student_list)
            transcript = transcript_ns[transcript_list[0]]
            transcript_graph.add((transcript, RDF.type, transcript_class))
            transcript_graph.add((transcript, DC.identifier, Literal(transcript_list[0])))
            transcript_graph.add((transcript, DC.title, Literal(transcript_list[1])))
            transcript_graph.add((transcript, OWL.hasValue, Literal(transcript_list[2])))
            transcript_graph.add((transcript, DC.PeriodOfTime, Literal(transcript_list[3])))

    print(transcript_graph.serialize(format='turtle'))
    return transcript

comp_grad_page = "https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html#course-descriptions"
webPageScraping(comp_grad_page)

subject = list(graph.subjects(RDF.type, RDFS.Class))
#print(subject)
for row in subject:
    if "#Courses" in row:
        course_class = row
    if "#University" in row:
        university_class = row
    if "#Student" in row:
        student_class = row
    if "#Topics" in row:
        topic_class = row
    if "#Transcript" in row:
        transcript_class = row

properties = list(graph.subjects(RDF.type, RDF.Property))
#print(properties)
for row in properties:
    if "#isEnrolledAt" in row:
        enrolled_property = row
    if "#takesCourse" in row:
        takes_course_property = row
    if "#isAwarded" in row:
        is_awarded = row
    if "#isofferedBy" in row:
        is_offered_by = row
    if "#hasTranscript" in row:
        has_transcript = row

university = universityTripleGenerator(university_class)
#print(university)
courseTripleGenerator(course_class, comp_grad_page, is_offered_by, university)
topicsTripleGenerator(topic_class)
transcript = transcriptTripleGenerator(transcript_class)
studentTripleGenerator(student_class, enrolled_property, takes_course_property, is_awarded, university, has_transcript, transcript)
