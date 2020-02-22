from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, FOAF,RDFS
import csv

student_ns = Namespace("http://example.org/people/")
student_graph = Graph()
with open("StudentsRecord.csv", 'r') as csv_file:
    file_reader = csv.reader(csv_file, delimiter= "|")
    next(file_reader)
    for student_list in file_reader:
        print(student_list)
        student = student_ns[student_list[0]]
        student_graph.add((student, RDF.type, FOAF.Student))
        student_graph.add((student, FOAF.studentId, Literal(student_list[0])))
        student_graph.add((student, FOAF.givenName, Literal(student_list[1])))
        student_graph.add((student, FOAF.familyName, Literal(student_list[2])))
        student_graph.add((student, FOAF.mbox, Literal(student_list[3])))
        #course triple to be added

print(student_graph.serialize(format='turtle'))



