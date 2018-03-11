# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class FoPipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        tag = item['tag']
        tag = item['url']
        question = item['question']
        answers = item['answers']
        print "结果========================="
        print len(answers)
        print question
        return item

