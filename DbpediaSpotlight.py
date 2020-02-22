import csv
import spotlight


topic_name = []
topic_url = []
with open("Courses.csv", "r") as course_file:
    file_reader = csv.reader(course_file, delimiter="|")
    next(file_reader)
    for row in file_reader:
        text = row[1]+" "+row[3]
        #print(text)
        if text != "":
            try:
                annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate', text=text, confidence=0.5)
                for data in annotations:
                    print(data)
                    topic_name = data['surfaceForm']
                    topic_url = data['URI']
            except:
                #to be completed
                None
        else:
            continue

#print(topic_name)

'''text = "President Obama on Monday will call for a new minimum tax rate for individuals making more than $1 million a year to ensure that they pay at least the same percentage of their earnings as other taxpayers, according to administration officials."
text1 = "Principles of distributed computing: scalability, transparency, concurrency, consistency, fault tolerance. Client-server interaction technologies: interprocess communication, sockets, group communication, remote procedure call, remote method invocation, object request broker, CORBA, web services. Distributed server design techniques: process replication, fault tolerance through passive replication, high availability through active replication, coordination and agreement transactions and concurrency control. Designing software fault-tolerant highly available distributed systems using process replication. Laboratory: two hours per week."
annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate',text=text1, confidence=0.5, support=20)
print(annotations)
for data in annotations:
    #data = annotations[1]
    print(data['URI'])
    print(data['surfaceForm'])'''

