# -*- coding: utf-8 -*-
import re
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy import Item, Field
from scrapy.spiders import CrawlSpider, Rule

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class MyItem(Item):
    url = Field()
    feature = Field()
    model = Field()
    brand = Field()
    cc = Field()
    power = Field()
    torque = Field()
    engine = Field()


class BajajSpider(CrawlSpider):
    name = 'bajaj'
    allowed_domains = ['globalbajaj.com']
    start_urls = ['http://globalbajaj.com/sri-lanka/english/']

    rules = (Rule(LxmlLinkExtractor(allow=('sri-lanka'), deny=('events', 'wallpapers', 'about-us', 'contact-us')),
                  callback='parse_page', follow=False),)

    def parse_page(self, response):
        page = response.url.split("/")[-1]
        # page = response.url
        print('-' * 30)
        print(page)
        print('-' * 30)

        item = MyItem()
        item['url'] = response.url
        item['brand'] = "Bajaj"
        model = response.xpath('//*[@class="h1mar dis-head"]/text()').extract()
        if len(model) > 0:
            item['model'] = model[0]
            details = response.xpath(
                '//*[@class="body_content_ineside"]//*[@class="caption_variant"]/h3/text()').extract()
            item['cc'] = details[0]
            item['power'] = details[1]
            item['torque'] = details[2]
            item['engine'] = details[3]
            feature = response.xpath('//*[@class="technology_content f-left"]').extract()
            if len(feature) > 0:
                item['feature'] = self.remove(feature[0])

        yield item

    def remove(self, text):
        cleanr = re.compile('<.*?>')
        text = re.sub(cleanr, ' ', text)
        text = re.sub('\s+', ' ', text)
        text = " ".join(text.split())
        return text
