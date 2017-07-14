import requests
requests.packages.urllib3.disable_warnings() #turn off HTTPS warnings
import re 
import lxml.html as LH
import random
import datetime 
import time
import sys 
import json
import urllib2 as urllib2 
import urllib
from twitter import * 


#data source
URL='https://microbewiki.kenyon.edu/index.php/Microbial_Biorealm'


#returns python requests object
def webRequest( url ):
	return requests.get(url, verify=False)

#returns python lxhtml root object
def webRoot( req): 
	return LH.fromstring(req.content)

#returns python array containing relevant links
def webLinks( root ):
	return root.xpath('.//div[@id="mw-content-text"]//a/@href')

#returns python integer
def getRandomIndex( f, c):
	return int(round(random.uniform(f,c)))

#returns relevant link
def getPostLink( linx, idx):
	return linx[idx]

#returns python string
def makeLabelFromLink( str ):
	return re.sub('.*\/(.+)', r'\1', str)

def prettifyLink( str ):
	return "https://microbewiki.kenyon.edu" + str

def getTwitterHandle(consumer_key, consumer_secret, access_key, access_secret):
	twitter = Twitter(auth=OAuth(access_key, access_secret, consumer_key, consumer_secret))
	return twitter


#quick check on args
if len(sys.argv) != 6:
	print "Generate Your Keys! https://apps.twitter.com/"
	print "usage: facts_bot_simple.py <accessKey> <accessSecret> <consumerKey> <consumerSecret> <intervalSeconds>"
	sys.exit(1)
else:
	consumerKey=sys.argv[1]
	consumerSecret=sys.argv[2]
	accessKey=sys.argv[3]
	accessSecret=sys.argv[4]
	intSec=float(sys.argv[5])




while True:
	twitter = getTwitterHandle(accessKey, accessSecret, consumerKey, consumerSecret)
	req = webRequest(URL)
	wRoot = webRoot(req)
	linx = webLinks(wRoot)
	ix = getRandomIndex(22, int(len(linx)))
	postLink = getPostLink(linx, ix)
	postLabel = makeLabelFromLink(postLink)
	prettyLink = prettifyLink(postLink)
	postText = "Learn about: " + postLabel + " here \n" + prettyLink + "\n" + "^_^" + "\n" + "BacterialBot"
	print postText
	twitter.statuses.update(status=postText)
	time.sleep(intSec)



