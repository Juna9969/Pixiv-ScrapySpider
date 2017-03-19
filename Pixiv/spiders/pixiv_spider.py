# -*- coding:UTF-8 -*-
import scrapy
from scrapy.http import Request
from Pixiv.items import PixivItem
from scrapy.conf import settings
class PixivSpider(scrapy.Spider):
	name = "pixiv"
	start_urls = ['http://www.pixiv.net/ranking.php?mode=male','http://www.pixiv.net/ranking.php?mode=male_r18']

	cookie = settings['COOKIE']
	headers = {
		'Connection':'keep-alive',
	}
	meta = {
		'dont_redirect':True,
		'handle_httpstatus_list':[301,302]
	}
#初始化
	def start_requests(self):
		yield Request(self.start_urls[1], callback=self.parse, cookies=self.cookie,
			headers=self.headers, meta=self.meta)

#进入排名页面
	def parse(self, response):
		for href in response.xpath('.//*[@id=@*]/div[@class="ranking-image-item"]/a/@href'):
			url = response.urljoin(href.extract())
			yield Request(url=url, cookies=self.cookie, callback=self.parse_dir_contents, headers=self.headers, meta=self.meta)
#子页面
	def parse_dir_contents(self, response):
		item = PixivItem()
		item['url'] = response.url
		item['image_urls'] = response.xpath('//*[@id="wrapper"]/div[2]/div/img/@data-src | @src').extract()
		if  not item['image_urls'] :
			for href in response.xpath('//*[@id="wrapper"]/div[1]/div[1]/div/div[6]/a/@href'):
				url = response.urljoin(href.extract())
				yield Request(url,cookies=self.cookie,headers=self.headers, meta=self.meta, callback=self.big_double)
		else:
			yield item

	def big_double(self,response):
		item = PixivItem()
		item['url'] = response.url
		for lis in response.xpath('//*[@id="main"]/section/div/a/@href'):
			url = response.urljoin(lis.extract())
			yield Request(url=url, cookies=self.cookie, callback=self.double_big_dir, headers=self.headers, meta=self.meta)

	def double_big_dir(self, response):
		item = PixivItem()
		item['url'] = response.url
		item['image_urls'] = response.xpath('/html/body/img/@src').extract()
		yield item