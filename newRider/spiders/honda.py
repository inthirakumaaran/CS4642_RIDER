# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import Item, Field
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import CrawlSpider, Rule

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class MyItem(Item):
    url = Field()
    description = Field()
    feature = Field()
    model = Field()
    brand = Field()
    specification = Field()


class HondaSpider(CrawlSpider):
    name = 'honda'
    allowed_domains = ['honda.lk']
    start_urls = ['http://honda.lk']
    rules = (Rule(LxmlLinkExtractor(allow=('bikes_ind')), callback='parse_page', follow=True),)

    def parse_page(self, response):
        page = response.url.split("/")[-1]
        # page = response.url
        print('-' * 30)
        print(page)
        print('-' * 30)

        item = MyItem()
        item['url'] = response.url
        item['brand'] = "Honda"
        para = self.remove(response.xpath('//*[@class="bike_detaicont"]').extract()[0])
        item['model'] = self.getname(para)
        item['description'] = para
        # # print(self.getname(self.remove(para)))

        spec = response.xpath('//*[@id="mainContent"]/div[2]/div[2]/div/div[2]/dl/dd[3]/div[1]').extract()
        if len(spec) > 0:
            spec = self.remove(spec[0])
            spec = self.clean(spec)
            item['specification'] = spec
        feature = response.xpath('//*[@id="mainContent"]/div[2]/div[2]/div/div[2]/dl/dd[3]/div[1]').extract()
        if len(feature) > 0:
            feature = self.remove(feature[0])
            feature = self.clean(feature)
            item['feature'] = feature
        yield item

    def remove(self, text):
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, ' ', text)
        text = re.sub('\s+', ' ', text)
        # text = " ".join(text.split())
        return text

    def getname(self, text):
        text = text.split(" ")
        if text[1].lower() == "the":
            answer = text[2] + " " + text[3]
        else:
            answer = text[1] + " " + text[2]
        return answer

    def clean(self, item):
        item = item.replace('</p>', '')
        item = item.replace('<p>', '')
        item = item.replace('<br>', '')
        item = item.replace('\n', '')
        item = re.sub(r' [^a-z0-9]+ ', ' ', item)
        item = item.replace('\r', '')
        item = " ".join(item.split())
        return item
