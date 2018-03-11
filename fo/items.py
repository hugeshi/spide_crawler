# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FoItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    pass


class QuestionItem(scrapy.Item):
    url = scrapy.Field()
    tag = scrapy.Field()
    title = scrapy.Field()
    question = scrapy.Field()
    answers = scrapy.Field()
    pass
