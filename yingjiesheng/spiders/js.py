# -*- coding: utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy import log
import time
from yingjiesheng.items import YingjieshengItem

today1 = time.strftime('%Y-%m-%d',time.localtime())
today2 = time.strftime('%Y年%m月%d日',time.localtime())

class JsSpider(CrawlSpider):
	name = "js"
	allowed_domains = ["yingjiesheng.com"]
	download_delay = 10
	start_urls = ['http://www.yingjiesheng.com/jiangsujob/']

	rules = (
	Rule(SgmlLinkExtractor(allow=(r'http://www.yingjiesheng.com/jiangsujob/list_\d.html'))),
	Rule(SgmlLinkExtractor(allow=(r'http://www.yingjiesheng.com/nanjing/'))),
	Rule(SgmlLinkExtractor(allow=(r'http://www.yingjiesheng.com/wuxijob/[\w]*'))),
	Rule(SgmlLinkExtractor(allow=(r'http://www.yingjiesheng.com/job-[\d-]+.html')),callback="parse_item"),
	Rule(SgmlLinkExtractor(allow=(r'http://my.yingjiesheng.com/job_[\d]+.html')),callback="parse_item2"),
)
	def parse_item2(self,response):

		itoday=response.xpath('//div[@class="job_list"]/ul/li/span/text()').re(today2.decode('utf-8'))
		if itoday == []:
			pass
		else:
			item = YingjieshengItem()
			company_name = response.xpath('//h1/a/text()').extract()
			company_link = str(response.url)
			company_tel = response.xpath('//div[@class="main"]').re(u'0[25][125][\d]?[)-]?[\u2014]?[\uff0d\u0020\u2014\uff09]?[0-9]{7,8}|1[358]\d-?\d{3,4}-?\d{4,5}')
			company_email = response.xpath('//div[@class="main"]').re('[A-Za-z0-9\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+')
	
			item['company_name']=''.join(company_name).encode('utf-8')
			item['company_link']=company_link.encode('utf-8')
			item['company_tel']=','.join(sorted(set(company_tel))[:5]).encode('utf-8')
			item['company_email']=','.join(sorted(set(company_email))[:5]).encode('utf-8')

			if item['company_email'] and item['company_name']:
				return item
			else:
				item['company_name']=''
				item['company_link']=''
				item['company_tel']=''
				item['company_email']=''
				return item

	def parse_item(self, response):

		itoday=response.xpath('//div[@class="info clearfix"]/ol/li/u/text()').re(today1.decode('utf-8'))
		if itoday == []:
			pass
		else:
			item = YingjieshengItem()

			company_name = response.xpath('//div[@class="mleft"]/h1/text()').extract()
			company_link = str(response.url)
			company_tel = response.xpath('//div[@class="mleft"]').re(u'0[25][125][\d]?[)-]?[\u2014]?[\uff0d\u0020\u2014\uff09]?[0-9]{7,8}|1[358]\d-?\d{3,4}-?\d{4,5}')
			company_email = response.xpath('//div[@class="mleft"]').re('[A-Za-z0-9\.-]+@(?:[A-Za-z0-9]+\.)+[A-Za-z]+')
			item['company_name']=''.join(company_name).encode('utf-8')
			item['company_link']=company_link.encode('utf-8')
			item['company_tel']=','.join(sorted(set(company_tel))[:5]).encode('utf-8')
			item['company_email']=','.join(sorted(set(company_email))[:5]).encode('utf-8')

			if item['company_email'] and item['company_name']:
				return item
			else:
				item['company_name']=''
				item['company_link']=''
				item['company_tel']=''
				item['company_email']=''
				return item
