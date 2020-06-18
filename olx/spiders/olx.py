# -*- coding: utf-8 -*-
import scrapy
import re
from olx.items import OfferItemLoader, OfferItem


DETAILS_MAPPING = {
    'Oferta od' : 'offerType',
    'Poziom' : 'level',
    'Rodzaj zabudowy' : 'bulidingType',
    'Powierzchnia' : 'area',
    'Liczba pokoi' : 'roomCount',
    'Czynsz (dodatkowo)' : 'additionalCost'
}

class OLXSpider(scrapy.Spider):
    name = 'olx'
    allowed_domains = ['olx.pl', 'otodom.pl']
    start_urls = ['https://olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/']

    def parse(self, response):
        offersLinks = response.xpath('//table[@id="offers_table"]/tbody' \
            '/tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[contains(@class, "title-cell")]' \
            '/div/h3/a/@href').getall()
        for href in offersLinks:
            if 'olx.pl' in href:#.get(): 
                yield response.follow(href, callback=self.parse_offer_page_olx)
            # elif 'otodom.pl' in href:#.get():
            #     yield response.follow(href, callback=self.parse_offer_page_otodom)

    def parse_offer_page_olx(self, response):
        loader = OfferItemLoader(item=OfferItem(), response=response)
        descriptionLoader = loader.nested_xpath('//*[@id="offerdescription"]')
        descriptionLoader.add_xpath('title', './div[1]/h1/text()')
        descriptionLoader.add_css('price', '.pricelabel__value::text')

        details = response.xpath('//*[@id="offerdescription"]/div[2]/ul/li/*')
        for detail in details:
            name = detail.xpath('./span/text()').get()
            value = detail.xpath('./strong/text()').get()
            fieldName = DETAILS_MAPPING.get(name, None)
            if fieldName:
                loader.add_value(fieldName, value)
        
        loader.add_xpath('url', '/html/head/link[@rel="canonical"]/@href')
        loader.add_xpath('location', '//*[@id="offeractions"]/div[3]/div[2]/div[1]/address/p/text()')
        
        bottomLoader = loader.nested_xpath('//*[@id="offerbottombar"]/ul')
        bottomLoader.add_xpath('offerID', './li[3]/strong/text()')
        bottomLoader.add_xpath('addDate', './li[1]/em/strong/text()')        
        return loader.load_item()

    def parse_offer_page_otodom(self, response):
        # Get title and price separately
        title = response.xpath('//*[@id="root"]/article/header/div[1]/div/div/h1/text()').get()
        price = response.xpath('//*[@id="root"]/article/header/div[2]/div[1]/div[2]/text()').get()
        price = re.sub(r'z\u0142|\s', '', price)
        offerData = {
            'title' : title,
            'price' : price
        }

        # Loop through remaining details
        details = response.xpath('//*[@id="root"]/article/div[3]/div[1]/section[@class="section-overview"]/div/ul/li')
        for detail in details:
            name = detail.xpath('./text()').get()
            value = detail.xpath('./strong/text()').get()
            offerData[name] = value


        offerData['type'] = response.xpath('//*[@id="root"]/article/section[2]/div[2]/div[1]/text()').get()
        offerData['address'] = response.xpath('//*[@id="root"]/article/header/div[1]/div/div/div/a/text()').get()
        offerID = response.xpath('//*[@id="root"]/article/div[3]/div[1]/div[3]/div/div[1]/text()').get()
        offerID = offerID.split(':')[-1].strip()
        offerData['id'] = offerID
        offerData['add_time'] = response.xpath('//*[@id="root"]/article/div[3]/div[1]/div[3]/div/div[2]/text()').get()
        offerData['url'] = response.xpath('/html/head/link[@rel="canonical"]/@href').get()

        return offerData
