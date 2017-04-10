from datetime import datetime
import operator
from time import strptime
from dateutil import parser
import pytz
import csv
utc=pytz.UTC
__author__ = 'roctbb'

import facebook
import requests

docNames = dict()
i=0

notFoundNames = []
nf = 0

with open('users.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        docNames[i]=dict()
        docNames[i]["surname"] = row[0]
        docNames[i]["name"] = row[1]
        docNames[i]["found"] = "no"
        i+=1
access_token = 'EAACEdEose0cBAOtdUQ6au8oxkBsnrfpr8PPhC7wk2sQZANZBZBd66P1J6nMsNjzbIkQ7ynAVDByjZCw37rrZALHoak5nZB8wmhQ70J7BuDP1j9m162pZCZCjkvQvGTBualFtTio2CYwRk7pKRrlkGW52HmfcUxcOzcRAMBDj6jHJQgZDZD'
graph = facebook.GraphAPI(access_token)
members = graph.get_connections(id='110103412708330', connection_name='members')


People = dict()
m=0
while (True):
    try:
        m+=len(members["data"])
        for member in members["data"]:
            data = str(member["name"]).lower().split(" ")
            #print(data)
            if len(data)>2:
                data = [data[0], data[2]]
            f = False
            for i in range(len(docNames)):
                #print(data[0].lower())
                #print(docNames[i]["name"].lower())
                if docNames[i]["name"].lower().find(data[0].lower()) == 0 and docNames[i]["surname"].lower().find(data[1].lower()) == 0:
                    docNames[i]["found"]="yes"
                    #print(data)
                    f=True
                    break
            if f==False:
                notFoundNames.append(data)


        members = requests.get(members['paging']['next']).json()
    except KeyError:
        break;

#print(m)
#for value in notFoundNames:
#    print(value[0]+" "+value[1])

#print(len(notFoundNames))

#c=0
for i in range(1,len(docNames)):
    print(docNames[i]["found"])

