import re
import json


from scrapy.selector import Selector
try:
    from scrapy.spider import Spider
except:
    from scrapy.spider import BaseSpider as Spider
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as lxmle
from scrapy.loader import ItemLoader

from itzhaopin.items import  *
from itzhaopin.misc.log import *


class TencentSpider(CrawlSpider):
    name = "tencent"
    allowed_domains = ["tencent.com"]
    start_urls = [
        "http://hr.tencent.com/position.php"
    ]
	#for next page
    rules = [
        Rule(sle(allow=("/position.php\?&start=\d{,4}#a")), follow=True, callback='parse_item')
    ]

    def parse_item(self, response):
        items = []
        sel = Selector(response)
        base_url = get_base_url(response)
        sites_even = sel.css('table.tablelist tr.even')
        for site in sites_even:
            item = TencentItem()
            item['name'] = site.css('.l.square a').xpath('text()').extract()[0]
            relative_url = site.css('.l.square a').xpath('@href').extract()[0]
            item['detailLink'] = urljoin_rfc(base_url, relative_url)
            item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()
            item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()[0]
            item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()[0]
            item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()[0]
            items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'

        sites_odd = sel.css('table.tablelist tr.odd')
        for site in sites_odd:
            item = TencentItem()
            item['name'] = site.css('.l.square a').xpath('text()').extract()[0]
            relative_url = site.css('.l.square a').xpath('@href').extract()[0]
            item['detailLink'] = urljoin_rfc(base_url, relative_url)
            item['catalog'] = site.css('tr > td:nth-child(2)::text').extract()
            item['workLocation'] = site.css('tr > td:nth-child(4)::text').extract()[0]
            item['recruitNumber'] = site.css('tr > td:nth-child(3)::text').extract()[0]
            item['publishTime'] = site.css('tr > td:nth-child(5)::text').extract()[0]
            items.append(item)
            #print repr(item).decode("unicode-escape") + '\n'

        info('parsed ' + str(response))
        return items


    def _process_request(self, request):
        info('process ' + str(request))
        return request


class LavaJobs(CrawlSpider):
	name = "lavajobs"
	allowed_domains = ["10.0.70.55"]
	start_urls = [
		"http://10.0.70.55/scheduler/alljobs",
	]

	rules = [
		Rule(lxmle(allow=(u"page=\d{,4}#table")), follow=True, callback='parse_item')
	]

	def parse_item(self, response):
		items = []
		sel = Selector(response)
		base_url = get_base_url(response)
		sites_even = sel.css('table.display tr.even')
		for site in sites_even:
			item = LavaJobsItem()
			item['ID'] = site.css('tr > td.id a::text').extract()[0]
			relative_url = site.css('tr > td.id a::attr(href)').extract()[0]
			item['jobdetailLink'] = urljoin_rfc(base_url, relative_url)
			item['status'] = site.css('tr > td.status::text').extract()[0]
			item['priority'] = site.css('tr > td.priority::text').extract()[0]
			item['device'] = site.css("tr > td[class='device'] *::text").extract()[0]
			items.append(item)

		sites_odd = sel.css('table.display tr.odd')
		for site in sites_odd:
			item = LavaJobsItem()
			item['ID'] = site.css('tr > td.id a::text').extract()[0]
			relative_url = site.css('tr > td.id a::attr(href)').extract()[0]
			item['jobdetailLink'] = urljoin_rfc(base_url, relative_url)
			item['status'] = site.css('tr > td.status::text').extract()[0]
			item['priority'] = site.css('tr > td.priority::text').extract()[0]
			item['device'] = site.css("tr > td[class='device'] *::text").extract()[0]
			items.append(item)

		info('parse ' + str(response))
		return items

	def _process_request(self, request):
		info('process ' + str(request))
		return request

class SinaCaijing(CrawlSpider):
	name = 'sinacaijing'
	allow_domains = ["finance.sina.com.cn"]
	start_urls = [
		"http://finance.sina.com.cn/",
	]
	rules = [
		Rule(lxmle(allow=(u"http://finance.sina.com.cn/roll/\d{4}-\d{2}-\d{2}/doc-\w*.shtml")), follow=True, callback='parse_item'),
	]

	def parse_item(self, response):
		items = []
		sel = Selector(response)
		#important_news = sel.css("div[id='directAd_huaxia']").css("div[class='m-p-middle fleft']")
		#for news in important_news:
		info(get_base_url(response))
		if True:
			il = ItemLoader(item=SinaRollDocItem(), selector=sel)
			il.add_css('title', 'h1.main-title::text')
			il.add_css('content', 'div[class="article-content-left"] p::text')
			return il.load_item()
		else:
			item = SinaRollDocItem()
			item['title'] = sel.css('h1.main-title::text').extract()
			item['content'] = sel.css('div[class="article-content-left"] p::text').extract()
			return item

