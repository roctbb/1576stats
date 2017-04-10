from datetime import datetime
import operator
from time import strptime
from dateutil import parser
import pytz

utc=pytz.UTC
__author__ = 'roctbb'

import facebook
import requests

access_token = 'EAACEdEose0cBAOIyDhWd2DPluDKOqEtwCZBYjyipqK41JfphblwQNWNFiQFBr37F9IW0jdcz0mqyNuKbrvJreOZBWvJV5uCEns6bh6qgnNRhZB1QpUW6fGfxArjE95V7eKPdErVL0gZCHMNXEDZBaToZBZBDl4mvlZBVBvarnsj7zG1EzS0Mlhk3DFqeK4d9sQQZD'
graph = facebook.GraphAPI(access_token)
members = graph.get_connections(id='110103412708330', connection_name='members')


People = dict()

while (True):
    try:
        for member in members["data"]:
            People[member["name"]] = dict();
            People[member["name"]]["likes"]=0;
            People[member["name"]]["comments"]=0;
            People[member["name"]]["posts"]=0;
        members = requests.get(members['paging']['next']).json()
    except KeyError:
        break;

posts = graph.get_connections(id='110103412708330', connection_name='feed')

while (True):
    try:
        break_time = False;
        posts_data = posts['data']
        for post in posts_data:
            try:
                if (parser.parse(post["created_time"])>utc.localize(datetime(2017, 1, 1))):
                    continue
                if (parser.parse(post["created_time"])<utc.localize(datetime(2016, 12, 1))):
                    break_time = True
                    continue
                else:
                    break_time = False
                if "likes" in post.keys():
                    for like in post["likes"]["data"]:
                        People[like["name"]]["likes"]+=1
                if "comments" in post.keys():
                    for comment in post["comments"]["data"]:
                        People[comment["from"]["name"]]["comments"]+=1
                if "from" in post.keys():
                    if "name" in post["from"].keys():
                        People[post["from"]["name"]]["posts"]+=1
            except KeyError:
                continue;

        if break_time==True:
                break;
        posts = requests.get(posts['paging']['next']).json()
    except KeyError:
        break;

print("likes:");
for man in sorted(People.keys()):
    likes = 0;
    if "likes" in People[man].keys():
        likes = People[man]["likes"]
    posts = 0;
    if "posts" in People[man].keys():
        posts = People[man]["posts"]
    comments = 0;
    if "comments" in People[man].keys():
        comments = People[man]["comments"]
    print(str(man)+";"+str(posts)+";"+str(comments)+";"+str(likes))


