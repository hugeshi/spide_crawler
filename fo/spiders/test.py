#!/usr/bin/env python
# -*- coding:utf-8 -*-
import scrapy
from fo.items import QuestionItem
import logging
from scrapy.selector import Selector
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

logger = logging.getLogger('S110comlogger')


class TestSpider(scrapy.spiders.Spider):
    name = "test"
    allowed_domains = ["110.com"]
    site_url = "http://www.110.com"
    start_urls = [
        "http://www.110.com/ask/question-12203649.html"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Host": "www.110.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    def parse(self, response):
        # parse response and populate item as required
        item = QuestionItem()
        selector = Selector(response)
        text = selector.xpath('//div[@class="xwz"]').extract()[0]
        soup = BeautifulSoup(text, 'lxml')
        question = ''.join(soup.find_all(text=True)).replace(' ', '').replace('\n', '')
        answers = selector.xpath('//div[@class="zjdanr"]/text()').extract()
        answer_list = []
        item['parent'] = response.url
        item['url'] = response.url
        item['tag'] = "test"
        item['title'] = "test"
        for answer in answers:
            answer_list.append(answer)
            print answer
        item['question'] = question
        item['answers'] = '|'.join(answer_list).replace(' ', '').replace('\n', '')
        return item

