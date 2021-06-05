# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AthomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    href = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    m2 = scrapy.Field()
    price_m2 = scrapy.Field()
    timestamp = scrapy.Field()
    status = scrapy.Field()
    place = scrapy.Field()
    
