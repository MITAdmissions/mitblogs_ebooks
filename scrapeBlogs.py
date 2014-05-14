##scrapes entry text from all mitadmissions.org blogs and writes to text file
##horrible code can be blamed on petey@mit.edu

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
import re
import unicodedata

#https://pypi.python.org/pypi/PyMarkovChain/1.7.5

##get list of best of the blogs links 
#define a base URL & page variable to increment 
baseURL = "http://mitadmissions.org/blogs/P"
p = 0 
html = ""

#loop through & download last 4600 (p<=4600 for production as of 5/14/2014) blog listings into a single stupidly huge document  
while p <= 20: 
	doc = urllib2.urlopen(baseURL + str(p))
	html = html + doc.read()
	p = p + 20

#load stupidly huge document into stupidly disgusting soup 
soup = BeautifulSoup(html)

#get entry links and write to list 
links = []
linkSoup = soup.find_all("h3")
for link in linkSoup:
	thisLink = link.a['href']
	fixedLink = str(thisLink)
	links.append(fixedLink)

##visit each link for each entry, scrape text, write to file 

#loop through all extracted links
for i in links:
	#create a separate soup for each linked entry
	html2 = ""
	doc2 = urllib2.urlopen(i)
	html2 = html2 + doc2.read()
	soup2 = BeautifulSoup(html2, "lxml")

	#get entry text 
	#first, scrape the soup for all <p> that have no id nor class (which for some reason is just sentences)
	lines = soup2.find_all('p', id='', class_='')

	#remove the 'see complete archives' outlier which always comes first 
	lines.pop(0)

	#then, iterate through this list of strings, get and clean the text, and write line to text file 
	for l in lines:
		thisLine = l.getText()
		cleanLine = unicodedata.normalize('NFKD', thisLine).encode('ascii', 'ignore')
		cleanerLine = cleanLine.replace('\n','').replace('\\','')
		with open('blogtext.txt', 'a') as out_file:
			out_file.write(' ' + cleanerLine)
