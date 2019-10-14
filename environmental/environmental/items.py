# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EnvironmentalItem(scrapy.Item):
    title = scrapy.Field()
    publication_date = scrapy.Field()
    journal = scrapy.Field()
    article_type = scrapy.Field()
    abstract = scrapy.Field()
    