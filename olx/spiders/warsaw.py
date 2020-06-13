# -*- coding: utf-8 -*-
import scrapy


class WarsawSpider(scrapy.Spider):
    name = 'warsaw'
    allowed_domains = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa']
    start_urls = ['http://https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/']

    def parse(self, response):
        pass
