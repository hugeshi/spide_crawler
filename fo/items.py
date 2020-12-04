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
    title = scrapy.Field()
    subject = scrapy.Field()
    replies = scrapy.Field()
    views = scrapy.Field()
    question = scrapy.Field()
    labels = scrapy.Field()
    tags = scrapy.Field()
    problems_ratings = scrapy.Field()
    answers = scrapy.Field(serialize=lambda x: u'\007'.join(x))
    pass
