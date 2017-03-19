# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.h
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem

class PixivPipeline(object):
    def process_item(self, item, spider):
        return item
class PixivImagesPipeline(ImagesPipeline):

    """抽取ITEM中的图片地址，并下载"""

    def file_path(self, request, response=None, info=None):
        image_guid = request.url.split('/')[-1]
        return '{0}'.format(image_guid)

    def get_media_requests(self, item, info):
        try:
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url,
                headers={'Referer': item['url'],  #添加Referer，否则会返回403错误
                         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'})
        except KeyError:
            raise DropItem("Item contains no images")

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item