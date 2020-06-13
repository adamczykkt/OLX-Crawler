# -*- coding: utf-8 -*-
import scrapy
import re


class WarsawSpider(scrapy.Spider):
    name = 'warsaw'
    allowed_domains = ['olx.pl', 'otodom.pl']
    start_urls = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/warszawa/']

    def parse(self, response):
        # offers = response.xpath('//table[@id="offers_table"]/tbody/tr[@class="wrap"]/td/div/table/tbody/tr[1]')
        # for offer in offers:
            # yield {
            #     'title' : offer.xpath('./td[contains(@class, "title-cell")]/div/h3/a/strong/text()').get(),
            #     'price' : offer.xpath('./td[contains(@class, "td-price")]/div/p/strong/text()').get()
            # }
        offersLinks = response.xpath('//table[@id="offers_table"]/tbody/tr[@class="wrap"]/td/div/table/tbody/tr[1]/td[contains(@class, "title-cell")]/div/h3/a/@href')
        for href in offersLinks:
            if 'olx.pl' in href.get(): 
                yield response.follow(href, callback=self.parse_offer_page_olx)
            elif 'otodom.pl' in href.get():
                yield response.follow(href, callback=self.parse_offer_page_otodom)

    def parse_offer_page_olx(self, response):
        # Get full offer details
        offer = response.xpath('//*[@id="offerdescription"]')

        # Get title and price separately
        title = offer.xpath('./div[1]/h1/text()').get().strip()
        price = offer.xpath('./div/div/div[@class="pricelabel"]/strong/text()').get()
        # try:
        #     price = int(re.sub(r'z\u0142|\s', '', price))
        # except:
        #     price = None
        price = re.sub(r'z\u0142|\s', '', price)

        offerData = {
            'title' : title,
            'price' : price
        }

        # Loop through remaining details
        details = offer.xpath('./div/ul[@class="offer-details"]/li/*[contains(@class, "offer-details__param")]')
        for detail in details:
            name = detail.xpath('./span/text()').get()
            value = detail.xpath('./strong/text()').get()
            offerData[name] = value

        # Get ID and link (canonical)
        offerData['id'] = response.xpath('//*[@id="offerbottombar"]/ul/li[3]/strong').get()
        offerData['url'] = response.xpath('/html/head/link[@rel="canonical"]/@href').get()
        offerData['add_date'] = response.xpath('//*[@id="offerbottombar"]/ul/li[1]/em/strong/text()').get()
        offerData['address'] = response.xpath('//*[@id="offeractions"]/div/div/div[@class="offer-user__address"]/address/p/text()').get()

        return offerData

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
