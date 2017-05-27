import urllib
import urllib2
import json
import time
import os
import helper
from random import choice

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

host = os.getenv('MANAGE_HOST')
sleepTimes = [0.7,0.1,0.2,0.3,0.4,0.5,0.6]
headers = { 'User-Agent' : 'Baiduspider' }
bids = helper.gen_bids()
def fetch(id=''):
	key = long(id)
	while True:
		if not crawl(key):
			print 'stop:%s'%key
			break
		key = key - 1
	print 'finish:%s'%key

def crawl(key=None):
	try:
		url = 'https://api.douban.com/v2/book/%s?alt=json&apikey=08f332d3675ca9d71ad9987a3615fd85'%key

		request_status = urllib2.Request('http://%s/fetch-api1/status?id=%s'%(host,key))
		response_status = urllib2.urlopen(request_status)
		result_status = json.loads(response_status.read())
		if not result_status['result']:
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
				record_url = 'http://%s/fetch-api1/douban'%host
				record_values = {'id':id,'title':title,'author':','.join(author),'isbn':isbn,'publisher':publisher,'pubdate':pubdate,'tags':','.join(tagStrs),'image':image,'summary':summary,'price':price,'average':average}
				record_data = urllib.urlencode(record_values)
				response_record = urllib.urlopen('%s?%s'%(record_url,record_data))
		else:
			print 'msg:%s\n'%(msg)
	except urllib2.URLError, e:
	    if hasattr(e,"code"):
	        print e.code
	    else:
	    	raise e
	time.sleep(choice(sleepTimes))
	return True
