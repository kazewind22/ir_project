# -*- coding: utf-8 -*-
import re
import urllib2
import xlrd
import sys
import time
import traceback
from HTMLParser import HTMLParser

class MyHTMLParser(HTMLParser):
	def init(self, filename):
		self.flag = False
		self.fo = open(sys.argv[2]+'/'+filename, "w");

	def handle_endtag(self, tag):
		if tag == 'tr':
			if self.flag == True:
				self.flag = False
				self.fo.write("</>\n");

	def handle_data(self, data):
		checklist = ['課程名稱', '開課學期', '授課對象', '授課教師', '課號', '課程識別碼', '班次', '學分', '全/半年', '必/選修', '上課時間', '上課地點', '課程概述', '課程目標', '課程要求']
		if self.flag is True:
			data = data.decode('cp950').encode("utf-8").strip()
			if data:	
				self.fo.write(data+'\n')
		for item in checklist:
			if item in data:
				self.fo.write('<'+data.decode('big5').encode('utf-8')+'>\n')
				self.flag = True
if len(sys.argv) < 3:
	print "usage: python course.py *.xls dir\n"
	sys.exit(1)
book = xlrd.open_workbook(sys.argv[1])
sh = book.sheet_by_index(0)
parser = MyHTMLParser()
i = 1
while i < sh.nrows:
	course_id = str(sh.cell_value(rowx=i, colx=4).split()[0])+'%20'+str(sh.cell_value(rowx=i, colx=4).split()[1])
	class_id = str(sh.cell_value(rowx=i, colx=5))
	dpt_code = str(sh.cell_value(rowx=i, colx=2))
	ser_no = str(sh.cell_value(rowx=i, colx=0))
	skiplist = [u'\u670d\u52d9\u5b78\u7fd2', u'\u5c08\u984c\u7814\u7a76',
	  u'\u8ad6\u6587', u'\u5916\u6587\u9818\u57df', u'\u570b\u6587\u9818\u57df', u'\u8ecd\u8a13']
	#skiplist = [u'服務學習', u'專題研究', u'論文', u'外文領域', u'國文領域', u'軍訓']
	flag = False
	for tmp in skiplist:
		if tmp in sh.cell_value(rowx=i, colx=10):
			flag = True
			break
	if(flag):
		i += 1
		continue
	filename = str(sh.cell_value(rowx=i, colx=4).split()[0])+'_'+str(sh.cell_value(rowx=i, colx=4).split()[1])
	if class_id:
		filename += '_'+class_id
#	print str(i) + " " + filename
	parser.init(filename)
#	maybe some skip rule ex credit ==0 , chinese, english?

	url = 'http://nol.ntu.edu.tw/nol/coursesearch/print_table.php?' + 'course_id=' + course_id +'&class=' + class_id + '&dpt_code=' + dpt_code + '&ser_no=' + ser_no + '&semester=103-2'
	try:	
		parser.feed(urllib2.urlopen(url).read())
	except urllib2.HTTPError, e:
		i -= 1
		print url
		print 'HTTPError = ' + str(e.code)
	except urllib2.URLError, e:
		i -= 1
		print url
		print 'URLError = ' + str(e.code)
	except Exception:
		i -= 1
		print url
		print 'generic exception: ' + traceback.format_exc()
	i += 1
