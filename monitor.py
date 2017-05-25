import urllib
import urllib2
import json
import time
import MySQLdb

db=MySQLdb.connect(host='',port=,user='',passwd='',db='',charset="utf8")
cursor = db.cursor()
def monitor():
	global db
	global cursor
	try:
		sql = 'select small from douban_status'
		cursor.execute(sql)
		small0 = cursor.fetchall()[0][0]
		# query cache
		cursor.execute("COMMIT")
		time.sleep(600)

		if db == None:
			db=MySQLdb.connect(host='',port=,user='',passwd='',db='',charset="utf8")
			cursor = db.cursor()
		else:
			db.ping(True)
		cursor.execute(sql)
		small1 = cursor.fetchall()[0][0]

		if small0 == small1:
			print 'rerun... from %s'%small1
			small = long(small1)+4
			sql = 'update douban_status set small=%s'%small
			cursor.execute(sql)
			cursor.execute("COMMIT")

			key = small-1
			url = 'http://127.0.0.1:8080/?id=%s'%key

			request = urllib2.Request(url)
			response = urllib2.urlopen(request)
	except urllib2.URLError, e:
	    if hasattr(e,"code"):
	        print e.code
	    else:
	    	print str(e)
	except Exception, e:
		print str(e)
	cursor.close()
	db.close()

if __name__ == "__main__":
    monitor()