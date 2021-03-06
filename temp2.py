#!/usr/bin/python
import pysftp as sftp
import urllib2
from urllib2 import urlopen
from cookielib import CookieJar
import time
import urllib
from bs4 import BeautifulSoup
import wikipedia
#import scrapy
#from scrapy import *
from collections import defaultdict

# graph is a dictionary whith list as its value for implementing the data structure graph
# each graph variable stores revelent categories of thier respective query upto given level



# making connection with given category to its revelant categories

def addEdge(graph,u,v):
    graph[u].append(v)

# inserting edge information in a lift from dictionary

def generate_edges(graph):
    edges = []
    for node in graph:
        for neighbour in graph[node]:
            edges.append((node, neighbour))
    return edges
# displaying all values for a key in the graph

def show_edges(graph):
    edges=generate_edges(graph)
    for n in edges:
     print (n)

# shortest path between two noedes via dijkstra algorithm

def find_shortest_path(graph, start, end, path =[]):
        path = path + [start]
        if start == end:
            return path
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest


# Creating cookie jar object to extract the image tags

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

#login_data = urllib.parse.urlencode({'login' : 'admin', 'pass' : '123'})

opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17')]

#eachthing = wikipedia.page(city_tags[0]['value']).categories
#print(eachthing)

# for scraping informatin from wikipedia

wikipedia.set_lang("en")

def my_f(query):    #extracting wikipedia tags from a query

 #wikiterm = wikipedia.search(query)
 dx = 0
 # To eleminate exceptions in wikipedia categories
 try:
    page = wikipedia.page(query)
 except wikipedia.exceptions.DisambiguationError as e:
  dx=10
 except wikipedia.exceptions.PageError as e:
  #print e
  dx=10
 if dx == 0:
  if urllib.urlopen(wikipedia.page(query).url).getcode() == 200 :
   content = opener.open(wikipedia.page(query).url).read()
   soup2 = BeautifulSoup(content,'html.parser')
   cat1 = soup2.find_all("div",{'class':'mw-normal-catlinks'})
   cat2 = cat1[0].find_all('a')
   d=0
   list=[]
   for i in cat2:
    if d != 0:
     list.append(str(i.text.encode('utf8')))
    d=d+1
 else:
     return 0
 return list

# Adding scraped data to graph
def create_graph(query,lvl,graph):
 lvl = lvl + 1
 templist=[]
 a=0
 if query not in graph :
    templist = my_f(query)
 else:
    for var in graph[query]:
        templist.append(var)
        a=1

 if templist != 0 and len(templist) != 0 :
  if a!=1:
   print(query," ",templist)
   print("\n")
  for i in templist:
   if (a!=1):
    addEdge(graph,query, i)
  for j in templist:
   #print(j)
   if lvl<7:
    if j !=query :
     create_graph(j,lvl,graph)
   else:
    return 0
 else:
    return 0

# File Handling

# Adding data to file
def add_to_file(graph,name):
    open("created_graph/"+name+".txt", 'w').close()
    fout = open("created_graph/"+name+".txt","w")
    for node in graph:
        fout.write(node)
        fout.write("\n")
        for neighbour in graph[node]:
            fout.write(neighbour)
            fout.write("\n")
        fout.write("-1\n")
    fout.write("-2\n")

def output_file(query,gname,path):
    fout = open("output5.txt","a")
    fout.write(query)
    fout.write("\n")
    fout.write(gname)
    fout.write("\n")
    #for node in path:
     #   fout.write(node)
      #  fout.write("\n")

    fout.write(str(len(path)))
    fout.write("\n")
    fout.write("-1\n")

# Reading data from file
def read_from_file(graph,name):

    try:
        fin = open("created_graph/"+name+".txt")
    except :
        return 0
    query=fin.readline()
    query=query.replace("\n","")
    while(query and query!="-2"):
        val=fin.readline()
        val=val.replace("\n","")
        while(val and val!="-1"):
            addEdge(graph,query,val)
            val=fin.readline()
            val=val.replace("\n","")
        query=fin.readline()
        query=query.replace("\n","")
    return 1

graph = defaultdict(list)

#query = "supermarket"
#read_from_file(graph,query)
#create_graph(query,0,graph)
#add_to_file(graph,query)
#show_edges(graph)
#print("\n")

#query = "Machine Learning"
#read_from_file(graph2,query)
#create_graph(query,3,graph2)
#add_to_file(graph2,query)
#show_edges(graph2)


xl=["waterfall model","flow - oriented design","data coupling","function cohesion",
    "life cycle model","requirement specification ( srs )","actual time","available time",
    "earliest start time","event or milestone","network diagram","putnam estimation model",
    "computer assisted software system engineering ( cas )","min calculate unadjusted function points",
    "engineering environment","reverse engineering","belady and lehman model","boehm ' s model",
    "full reuse model","taute ' s maintenance model","Iterative enhancement model","yau and collofello ' s model",
    "cost of software maintenance","quality assurance ( sqa )","capability maturity model ( cmm )",
    "basic execution time model","calendar time",    "execution time","halstead ' s software science metrics",
    "human engineering","boehm ' s software quality model","mccabe ' s cyclomatic comple mccall ' s model",
    "Egineering quality","public domain software"
    ]

distance_from="mobile device"
read_from_file(graph,distance_from)
ans=[]
for query in xl :
    del ans [:]
    ans=[]
    graph2 = defaultdict(list)
    x=read_from_file(graph2,query)
    if x:
        print (query)
        print("\n")
        for key in graph2:
            path=[]
            del path [:]
            path=find_shortest_path(graph,distance_from,key)
            if ( path and (len(path) < len(ans) or not ans)):
                ans=path
                print(ans)
            for value in graph[key]:
                if value not in graph:
                    path=find_shortest_path(graph,distance_from,key)
                    if ( path and (len(path) < len(ans) or not ans)):
                        ans=path
                        print(ans)
        if ans:
            output_file(distance_from,query,ans)

