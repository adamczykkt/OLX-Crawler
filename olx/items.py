# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Compose, Identity


class OfferItem(Item):
    title = Field() #string
    price = Field() #float
    offerID = Field() #string
    addDate = Field() #Datetime
    location = Field() #string
    offerType = Field() #string
    level = Field() #string
    bulidingType = Field() #string
    area = Field() #float
    roomCount = Field() #string
    additionalCost = Field() #float
    url = Field() #string

class OfferItemLoader(ItemLoader):
    pass
