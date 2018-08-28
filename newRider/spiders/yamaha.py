# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import Item, Field
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
import lxml.etree as et
from lxml.etree import HTMLParser


try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class MyItem(Item):
    url = Field()
    body = Field()
    color = Field()
    model = Field()
    brand = Field()
    engine= Field()


class YamahaSpider(CrawlSpider):
    name = 'yamaha'
    allowed_domains = ['yamaha.lk']
    start_urls = ['http://yamaha.lk/']

    rules = (Rule(LxmlLinkExtractor(), callback='parse_page', follow=True),)

    def parse_page(self, response):
        page = response.url.split("/")[-1]
        print('-' * 30)
        print(page)
        print('-' * 30)

        item = MyItem()
        item['url'] = response.url
        eng = response.xpath('//*[@id="tabs1-Features"]/p[2]').extract()
        if len(eng)>0:
            engine = eng[0]
            item['engine'] = self.clean(engine)
            item['brand'] = "yamaha"
            item['model'] = response.url.split("/")[-1].split(".")[0]
            colours= response.xpath('//*[@id="tabs1-Colours"]/div/*/p/text()').extract()
            self.log(colours)
            self.log(response.xpath('//*[@id="tabs1-Colours"]/div/*/p/text()').extract()[0])
            color=''
            for colour in colours:
                color += colour
            if color:
                item['color']=self.clean(color)
        yield item

    def clean(self,item):
        item = item.replace('</p>', '')
        item = item.replace('<p>', '')
        item = item.replace('<br>', '')
        item = item.replace('\n', '')
        item = re.sub(r' [^a-z0-9]+ ', ' ', item)
        item = item.replace('\r', '')
        item = item.replace('\u2019', '')
        return item.strip()
