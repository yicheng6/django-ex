import urllib
import urllib2
import json
import time
import MySQLdb
import helper
from random import choice

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

db=MySQLdb.connect(host='',port=,user='',passwd='',db='',charset="utf8")
cursor = db.cursor()
sleepTimes = [0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6]
headers = { 'User-Agent' : 'Baiduspider' }
bids = helper.gen_bids()
def fetch(id=''):
	global db
	global cursor
	key = long(id)
	while True:
		if not crawl(key):
			print 'stop:%s'%key
			break
		key = key - 1
	print 'finish:%s'%key
	cursor.close()
	db.close()
	cursor = None
	db = None

def crawl(key=None):
	global db
	global cursor
	if db == None:
		db=MySQLdb.connect(host='',port=,user='',passwd='',db='',charset="utf8")
		cursor = db.cursor()
	else:
		db.ping(True)
	try:
		url = 'https://api.douban.com/v2/book/%s?alt=json&apikey=08f332d3675ca9d71ad9987a3615fd85'%key

		sql0 = 'update douban_status set small=%s where small>min'%key   
		n = cursor.execute(sql0)
		cursor.execute("COMMIT")
		if n != 1:
			return False

		headers["Cookie"] = 'bid="%s"' % choice(bids)
		request = urllib2.Request(url,headers = headers)
		response = urllib2.urlopen(request)
		result = json.loads(response.read())
		msg = result.get('msg')
		if msg == None:
			average = result['rating']['average']
			id = result['id']
			title = result['title']
			isbn = result.get('isbn13')
			author = result['author']
			pubdate = result['pubdate']
			tags = result['tags']
			image = result['images']['large']
			publisher = result['publisher']
			summary = result['summary']
			price = result['price']
			if average == '0.0':
				print 'msg:%s average is 0.0'%id
			elif len(author) == 0:
				print 'msg:%s author not exists'%id
			elif len(tags) == 0:
				print 'msg:%s tags not exists'%id
			elif isbn == None:
				print 'msg:%s isbn13 not exists'%id
			else:
				tagStrs = []
				for tag in tags:
					tagStrs.append(tag['name'])
				print '%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n'%(id,title,','.join(author),isbn,publisher,pubdate,','.join(tagStrs),image,summary,price,average)
				sql = "insert ignore into douban_book(id,title,author,isbn,publisher,pubdate,tags,image,summary,price,average) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"   
				param = (id,title,','.join(author),isbn,publisher,pubdate,','.join(tagStrs),image,summary,price,average)    
				n = cursor.execute(sql,param)
				cursor.execute("COMMIT")
		else:
			print 'msg:%s\n'%(msg)
	except urllib2.URLError, e:
	    if hasattr(e,"code"):
	        print e.code
	    else:
	    	print str(e)
	    	time.sleep(900)
	except Exception, e:
		print str(e)
		time.sleep(900)
	time.sleep(choice(sleepTimes))
	return True
