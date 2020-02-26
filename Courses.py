import requests
from bs4 import BeautifulSoup
import pandas as pd
from rdflib.namespace import RDFS, RDF, FOAF, DC, OWL, URIRef
from rdflib import Graph, Namespace, Literal
import csv

graph = Graph()
graph.parse("Classes.rdf", format="application/rdf+xml")
comp_grad_page = "https://www.concordia.ca/academics/graduate/calendar/current/encs/computer-science-courses.html#course-descriptions"
grad_page = "https://www.concordia.ca/academics/graduate/calendar/current/encs/engineering-courses.html#topicsinengineering"

def universityTripleGenerator(university_class):
    university_ns = Namespace("http://example.org/university/")
    #university_graph = Graph()
    university_list = ["Concordia_University"]
    university = university_ns[university_list[0]]
    graph.add((university, RDF.type, university_class))
    graph.add((university, FOAF.name, Literal("Concordia University")))
    graph.add((university, RDFS.seeAlso, Literal("http://dbpedia.org/resource/Concordia_University")))
    #print(graph.serialize(format='turtle'))
    graph.serialize(format='turtle')
    return university


def courseTripleGenerator(course_class, comp_grad_page, grad_page, is_offered_by, university):
    course_ns = Namespace("http://example.org/course/")
    #course_graph = Graph()
    with open("Courses.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for course_list in file_reader:
            #print(course_list)
            course = course_ns[course_list[2]+"_"+course_list[0]]
            graph.add((course, RDF.type, course_class))
            graph.add((course, DC.identifier, Literal(course_list[0])))
            graph.add((course, DC.title, Literal(course_list[1])))
            graph.add((course, DC.subject, Literal(course_list[2])))
            graph.add((course, DC.description, Literal(course_list[3])))
            graph.add((course, is_offered_by, Literal(university)))
            if course_list[2] == 'COMP' or course_list[2] == 'SOEN':
                graph.add((course, RDFS.seeAlso, Literal(comp_grad_page)))
            else:
                graph.add((course, RDFS.seeAlso, Literal(grad_page)))

    #print(course_graph.serialize(format='turtle'))
    graph.serialize(format='turtle')


def topicsTripleGenerator(topic_class):
    topic_ns = Namespace("http://example.org/topics/")
    #topic_graph = Graph()
    with open("topic.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for topic_list in file_reader:
            if " " in topic_list[0]:
                topic_name = topic_list[0].split(" ")[0] + "_" + topic_list[0].split(" ")[1]
            else:
                topic_name = topic_list[0]
            topic = topic_ns[topic_name]
            graph.add((topic, RDF.type, topic_class))
            graph.add((topic, DC.title, Literal(topic_list[0])))
            graph.add((topic, RDFS.seeAlso, Literal(topic_list[1])))
            graph.add((topic, FOAF.isPrimaryTopicOf, Literal(topic_list[2])))

    #print(topic_graph.serialize(format='turtle'))
    graph.serialize(format='turtle')


def studentTripleGenerator(student_class, enrolled_property, takes_course_property, is_awarded, university, has_transcript):
    student_ns = Namespace("http://example.org/people/")
    #student_graph = Graph()
    with open("StudentsRecord.csv", 'r') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|")
        next(file_reader)
        for student_list in file_reader:
            #print(student_list)
            student = student_ns[student_list[0]]
            graph.add((student, RDF.type, student_class))
            graph.add((student, FOAF.studentId, Literal(student_list[0])))
            graph.add((student, FOAF.givenName, Literal(student_list[1])))
            graph.add((student, FOAF.familyName, Literal(student_list[2])))
            graph.add((student, FOAF.mbox, Literal(student_list[3])))
            graph.add((student, enrolled_property, university))
            row_length = len(student_list)
            counter = 1
            for i in range(4,row_length):
                transcript_identifier = "T" + str(counter) + "S" + student_list[0]
                transcript_record = transcriptTripleGenerator(transcript_identifier, student_list[i], student_list[0], takes_course_property, is_awarded)
                graph.add((student, has_transcript, transcript_record))
                counter = counter + 1

    #print(student_graph.serialize(format='turtle'))
    graph.serialize(destination='FinalKnowledgeGraph.ttl', format='turtle')

def transcriptTripleGenerator(transcript_identifier, student_subject_list, student_id, takes_course_property, is_awarded):
    transcript_ns = Namespace("http://example.org/transcript/")
    #transcript_graph = Graph()
    split_subject_list = student_subject_list.split("-",3)
    #print(split_subject_list)
    transcript = transcript_ns[transcript_identifier]
    graph.add((transcript, RDF.type, transcript_class))
    graph.add((transcript, DC.identifier, Literal(student_id)))
    graph.add((transcript, takes_course_property, Literal(split_subject_list[0])))
    graph.add((transcript, is_awarded, Literal(split_subject_list[1])))
    graph.add((transcript, DC.PeriodOfTime, Literal(split_subject_list[2])))

    graph.serialize(format='turtle')
    return transcript


def sparql_query_1(query_graph):

    query1 = query_graph.query(
        """SELECT (count(*) AS ?Triples) 
        WHERE{
            ?sub ?p ?o .
    }"""
    )

    for row in query1:
        print("Total number of Triples:%s" % row)

    query2 = query_graph.query(
        """SELECT ?studentCount ?courseCount ?topicCount {
         {
            SELECT (count(DISTINCT ?firstName) AS ?studentCount) 
                WHERE{
                    ?studentSub a focu:Student .
                    ?studentSub foaf:givenName ?firstName .}
         }
         {
            SELECT (count(?courseTitle) AS ?courseCount)
                WHERE{   
                    ?courseSub a focu:Courses .
                    ?courseSub ns1:title ?courseTitle .}
         }
         {
            SELECT (count(?topicTitle) AS ?topicCount)
                WHERE{   
                    ?topicSub a focu:Topics .
                    ?topicSub ns1:title ?topicTitle .}
         }
        }"""
    )

    for row in query2:
        print("Total number of students:%s, total number of courses:%s and total number of topics:%s" % row)


def sparql_query_course(query_graph, question):
    query3 = query_graph.query(f"SELECT ?topicTitle ?topicUri WHERE{{ ?topicSub foaf:isPrimaryTopicOf '{question}' . ?topicSub ns1:title ?topicTitle . ?topicSub rdfs:seeAlso ?topicUri}}")

    for row in query3:
        print("Topic title:%s and Topic URI:%s" % row)


def sparql_query_student(query_graph, studentName):
    query4 = query_graph.query(f"SELECT ?courseName ?grade WHERE{{ ?transcriptSub a focu:Transcript . ?transcriptSub ns1:identifier ?studentId . {{SELECT ?studentId WHERE {{ ?studentSub foaf:givenName '{studentName}' . ?studentSub foaf:studentId ?studentId}} }} ?transcriptSub focu:takesCourse ?courseName . ?transcriptSub focu:isAwarded ?grade .}}")

    for row in query4:
        print(studentName, "has completed the Course %s with the Grade:%s" % row)

def sparql_query_studentAndTopic(query_graph, question):
    query5 = query_graph.query(f"SELECT ?studentId WHERE {{ ?transcriptSub a focu:Transcript . ?transcriptSub ns1:title ?courseName . {{SELECT ?courseName WHERE{{ ?topicSub ns1:title '{question}' . ?topicSub foaf:isPrimaryTopicOf ?courseName .}}}} . ?transcriptSub ns1:identifier ?studentId .}}")

    for row in query5:
        print("Student name:%s" % row)

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
courseTripleGenerator(course_class, comp_grad_page, grad_page, is_offered_by, university)
topicsTripleGenerator(topic_class)
studentTripleGenerator(student_class, enrolled_property, takes_course_property, is_awarded, university, has_transcript)
query_graph = Graph()
query_graph.parse("FinalKnowledgeGraph.ttl", format="ttl")
sparql_query_1(query_graph)
question = input("Hello, I am your smart university agent. How can I help you?")
#sparql_query_course(query_graph, question)
sparql_query_student(query_graph, question)
#sparql_query_studentAndTopic(query_graph, question)