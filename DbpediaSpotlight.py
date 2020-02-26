import csv
import spotlight
import pandas as pd

topic_name = []
topic_url = []
course_name = []
with open("Grad_courses.csv", "r") as course_file:
    file_reader = csv.reader(course_file, delimiter="|")
    next(file_reader)
    for row in file_reader:
        text = row[1]+" "+row[3]
        #print(text)
        if text != "":
          try:
            annotations = spotlight.annotate('https://api.dbpedia-spotlight.org/en/annotate', text=text, confidence=0.5, support=20)
            # file_annotations.append(annotations)
            for data in annotations:
                #print(data)
                #print (data['surfaceForm'])
                topic_name.append(data['surfaceForm'])
                topic_url.append(data['URI'])
                course_name.append(row[1])
          except:
            None


topicdf = pd.DataFrame(
    {'topic_name': topic_name,
     'topic_url': topic_url,
     'course_name': course_name
    })

final_topicdf = topicdf.drop_duplicates()
final_topicdf.to_csv('topic_new.csv', index=False , sep='|', encoding="utf8")




