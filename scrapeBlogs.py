##scrapes entry text from all mitadmissions.org blogs and writes to text file
##horrible code can be blamed on petey@mit.edu

from bs4 import BeautifulSoup
import os
import csv
import string
import urllib
import urllib2
import re
import unicodedata

##get list of best of the blogs links 
#define a base URL & page variable to increment 
baseURL = "http://mitadmissions.org/blogs/P"
p = 0 
#html = ""

headers = { 'User-Agent' : 'PeteyBlogBot' }

#loop through & download last 80 (p<=4600 for production as of 5/14/2014) blog listings into a single stupidly huge document  
while p <= 4600:
	html = "" 
	#doc = urllib2.urlopen(baseURL + str(p))
	doc = urllib2.urlopen(urllib2.Request((baseURL + str(p)), None, headers))
	html = doc.read()
	soup = BeautifulSoup(html)
	print str(p)

	#get entry links and write to list 
	links = []
	linkSoup = soup.find_all("h3")
	for link in linkSoup:
		thisLink = link.a['href']
		fixedLink = str(thisLink)
		links.append(fixedLink)

		##eventually, should add some stuff to pull entry authors, links, dates, etc, and store in dict w/ entry text)

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
			if "Comments have been closed." in thisLine:
				break
			if "No comments yet!" in thisLine:
				break 
			cleanLine = unicodedata.normalize('NFKD', thisLine).encode('ascii', 'ignore')
			cleanerLine = cleanLine.replace('\n','').replace('\\','')
			with open('blogtext.txt', 'a') as out_file:
				out_file.write(' ' + cleanerLine)

	#begin loop anew 
	p = p + 20