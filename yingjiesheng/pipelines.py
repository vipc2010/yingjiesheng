# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem
from scrapy.contrib.pipeline.images import ImagesPipeline
import time
import MySQLdb
import MySQLdb.cursors

import sys

if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

countadd=0
class YingjieshengPipeline(object):

	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb',db='customer',user = 'root',passwd = 'vipc2010',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)

	def process_item(self, item, spider):

		query = self.dbpool.runInteraction(self._conditional_insert,item)

		query.addErrback(self.handle_error)
		return item

	def _conditional_insert(self,tx,item):
	
#	print '\n\n---------------------\n',item['company_name'],'\n------------\n\n'

		tx.execute("select * from yingjiesheng_jiangsu where company_name = %s", (item['company_name'],))
		result = tx.fetchone()
		if result or item['company_name']=='':
			log.msg("\n\n\n\n\n\nItem already stored in db: %s" % item, level=log.DEBUG)
		else:
			tx.execute(\
			"insert into yingjiesheng_jiangsu (company_name,company_tel,company_email,company_link) values (%s, %s, %s,%s)",(item['company_name'], item['company_tel'], item['company_email'], item['company_link']))
			log.msg("\n\n\n\n\n\nItem stored in db: %s" % item, level=log.DEBUG)

	def handle_error(self,e):
		log.err(e)
