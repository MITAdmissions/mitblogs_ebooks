##scrapes the last 100 blog posts from mitadmissions & computes blogger stats 

from bs4 import BeautifulSoup
from collections import Counter
from pprint import pprint
import os
import csv
import string
import urllib
import urllib2
import time
from datetime import datetime
from datetime import timedelta

##Open & store current student bloggers (based on blog entry code)
students = urllib2.urlopen('http://mitadmissions.org/blogs/group/students')

bloggersHTML = students.read()
bloggersSoup = BeautifulSoup(bloggersHTML)

bloggers = []
bloggersSoup = bloggersSoup.find_all("h5")
for blogger in bloggersSoup:
	thisBlogger = blogger.string
	fixedBlogger = thisBlogger.encode('ascii','ignore')
	bloggers.append(str(fixedBlogger))

#define a base URL & page variable to increment 
baseURL = "http://mitadmissions.org/blogs/P"
p = 0 
html = ""

#loop through & download last 100 blog posts into soup  
while p <= 80: 
	doc = urllib2.urlopen(baseURL + str(p))
	html = html + doc.read()
	p = p + 20

#load to soup 
soup = BeautifulSoup(html)

##get blogger names 
names = []
nameSoup = soup.find_all("p", "byline")
for name in nameSoup: 
	thisName = name.string
	fixedName = thisName.encode('ascii', 'ignore')
	names.append(str(fixedName))

##find delinquent bloggers
delinquents = []
for blogger in bloggers:
	if blogger not in names:
		delinquents.append(blogger)

##now put them into a list of dicts for later 
ghosts = []
z = 0
for d in delinquents:
	ghouls = {
			  'author': delinquents[z],
			  'delta': "OUTSIDE OF TIME, OUTSIDE OF MIND",
			  }
	ghosts.append(ghouls)
	z = z + 1

##get blog title
titles = []
titleSoup = soup.find_all("h3")
for title in titleSoup:
	thisTitle = title.string
	fixedTitle = thisTitle.encode('ascii', 'ignore')
	titles.append(str(fixedTitle))

##get blog link 
links = []
linkSoup = soup.find_all("h3")
for link in linkSoup:
	thisLink = link.a['href']
	fixedLink = str(thisLink)
	links.append(fixedLink)

##get blog dates
dates = []
dateSoup = soup.find_all("p", "meta")
for date in dateSoup:
	thisDate = str(date.contents[0])
	fixedDate = thisDate[:-3]
	dates.append(fixedDate)

##parse date to a day/time structure and add to list
stamps = []
for date in dates:
	localTime = time.strptime(date, "%b %d %Y")
	timeStamp = time.mktime(localTime)
	stamps.append(timeStamp)

##compute days since last blogged
today = datetime.now()
deltas = []
for stamp in stamps: 
	dateStamp = datetime.fromtimestamp(stamp)
	thisDelta = today.date() - dateStamp.date()
	deltas.append(thisDelta.days)

##create a list of dicts containing blog info 
entries = [] 
e = 0 
for d in dates:
	entry = {
	'date': dates[e],
	'author': names[e],
	'title': titles[e],
	'url': links[e],
	'stamp': stamps[e],
	'delta': deltas[e]
	}
	entries.append(entry)
	e = e + 1 

##clean non-students out of dict
#the [:] makes a copy of the list so we're not simultaneously iterating & mutating as per http://goo.gl/dIusCp
for n in entries[:]:
	if n['author'] not in bloggers:
		entries.remove(n)

#iterate through the dict looking for deltas of authors and 
#putting them into a list of active or inactive bloggers and slackers
active = []
inactive = []

for en in entries:
	if en['delta'] <= 30:
		active.append(en)

#a gross loop to figure out if they're on the active list or not 
for tr in entries:
	hasBlogs = False
	for a in active:
		if tr['author'] == a['author']:
			hasBlogs = True
	if hasBlogs == False:
		inactive.append(tr) 

slackers = inactive + ghosts

##print output
print "***BLOGGER ANALYTICS***"

# ##count blogs by blogger and print to terminal
# print " "
# print " " 
# print "THE LAST 100 ENTRIES - BY VOLUME"
# print "(# of last 100 blog posts by current blogger)"
# for m in names[:]:
# 	if m not in bloggers:
# 		names.remove(m)
# pprint(Counter(names).most_common())

##count blogs by blogger and print to terminal
print " "
print " " 
print "THE LAST 30 DAYS - BY VOLUME"
print "(# of posts over last 30 days by current bloggers)"
mostBlogs = []

#add authors to list 
for a in active: 
	mostBlogs.append(a['author'])

#print a count of the recent blogs
for k, v in Counter(mostBlogs).most_common():
	num = str(v)
	print k + "\t \t" + num + " pearl(s) of insight" 

##count blog by most recent blog date and print to terminal
print " "
print " " 
print "THE LAST 30 DAYS - BY RECENCY"
print "(most recent blog post by current bloggers)"
mostRecent = []
for v in active:
	if v['author'] not in mostRecent:
		day = str(v['delta'])
		print v['author'] + "\t \t" + day + " day(s) since last posted"
		mostRecent.append(v['author'])

print " "
print " "
print "SLACKER BLOGGERS, FULL OF PUNT, THY GUILT IS WITH THEE"
print "(no blog posts in 30 days by (ostensibly) current bloggers)"
yesSlack = []
for s in slackers:
	if s['author'] not in yesSlack:
		day = str(s["delta"])
		print s['author'] + "\t \t" + day + " days since last blog"
		yesSlack.append(s['author'])

##write to csv and save to directory 
keys = ['date', 'author', 'title', 'url', 'stamp', 'delta']
f = open ('guiltTrip.csv','wb')
DW = csv.DictWriter(f,keys)
DW.writer.writerow(keys)
DW.writerows(entries)













