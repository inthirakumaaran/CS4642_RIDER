# -*- coding: utf-8 -*-
import json

import scrapy
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
    price = Field()
    model = Field()
    brand = Field()
    cc = Field()


class SlbikesSpider(CrawlSpider):
    name = 'SLBikes'
    allowed_domains = ['srilankabikes.com']
    start_urls = ['http://www.srilankabikes.com/']

    rules = (Rule(LxmlLinkExtractor(canonicalize=True, unique=True), callback='parse_url', follow=True),)

    def parse_url(self, response):
        page = response.url.split("/")[-2]
        print('-' * 30)
        print(page)
        print('-' * 30)
        parser = HTMLParser(encoding='utf-8', recover=True)
        tree = et.parse(StringIO(response.body), parser)
        for element in tree.xpath('.//*[@id="view-video"]'):
            element.getparent().remove(element)
        filename = '/home/kumar/7thsemi/IR/newRider/corpus_SLBikes/SLBikes-%s.JSON' % page
        item = MyItem()
        item['url'] = response.url
        price = response.xpath('//*[@id="view-price"]/text()').extract()
        # newPrice =price.map(self.getPrice,price)
        # item['price'] = newPrice[0]
        if len(price) > 0:
            newprice = response.xpath('//*[@id="view-price"]/text()').extract()[0].split(":")[1]
            if newprice != " Rs./-":
                item['price'] = newprice
        urll = response.url.split("/")[-2].split("-")
        if urll[1] == "price":
            item['model'] = urll[0]
        else:
            item['model'] = urll[0] + "-" + urll[1]
        item['brand'] = response.url.split("/")[-3].split("-")[0]
        # item['cc'] = response.xpath('//*[@id="view-details"]/table/tbody/tr[3]/td[2]').extract()
        cc = response.xpath('//*[@id="view-details"]/table/tbody/tr[3]/td[2]').extract()
        # newPrice =price.map(self.getPrice,price)
        # item['price'] = newPrice[0]
        if len(cc) > 0 :
            cc = response.xpath('//*[@id="view-details"]/table/tbody/tr[3]/td[2]').extract()[0].replace('</td>', '')
            cc= cc.replace('<td>', '')
            if len(cc)>1:
                item['cc'] = cc
        # self.log('srilankaBikes %s' % filename)
        # with open(filename, 'wb') as f:
        #     f.write(item)
        # f.close()
        # self.log('srilankaBikes %s' % filename)

        # line = json.dumps(
        #     dict(item),
        #     sort_keys=True,
        #     indent=4,
        #     separators=(',', ': ')
        # ) + ",\n"
        #
        # self.file.write(line)
        yield item

    def getPrice(n):
        return n.extract()[0].split(":")[1]
