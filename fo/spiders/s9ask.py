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


class S110com(scrapy.spiders.Spider):
    name = "9ask"
    allowed_domains = ["9ask.cn"]
    site_url = "http://www.9ask.cn"
    start_urls = [
        "http://www.9ask.cn/souask/list-wait-0-0-0-1.html"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Host": "9ask.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    def parse(self, response):
        selector = Selector(response)
        questions = selector.xpath('//ul[@class="clearfix"]/li')
        print len(questions)
        for question in questions:
            item = QuestionItem()
            url = question.xpath('a/@href').extract()[0]
            title = question.xpath('a/@title').extract()[0]
            item['parent'] = response.url
            item['url'] = url
            item['tag'] = question.xpath('span[@class="classItem"]/text()').extract()[0]
            item['title'] = title
            request = scrapy.Request(url, headers=self.headers,
                                     callback=self.parse_sub_page, dont_filter=True)
            request.meta['item'] = item
            yield request
        word = u'下一页'
        next_pages = selector.xpath('//a[text()="%s"]/@href' % word).extract()
        if next_pages:
            if len(next_pages[0]) > 0:
                next_page = next_pages[0]
                logger.info('parse next page============ %s', self.site_url+str(next_page))
                yield scrapy.Request(self.site_url+str(next_page), headers=self.headers,
                                        callback=self.parse, dont_filter=True)

    def parse_sub_page(self, response):
        item = response.meta['item']
        # parse response and populate item as required
        selector = Selector(response)
        question_text = selector.xpath('//div[@class="titnew"]/p/text()').extract()
        if question_text:
            text = question_text[0]
        soup = BeautifulSoup(text, 'lxml')
        question = ''.join(soup.find_all(text=True)).replace(' ', '').replace('\n', '')
        answers = selector.xpath('//div[@class="anss_con"]/p/text()').extract()
        answer_list = []
        for answer in answers:
            answer_list.append(answer)
            break
        item['question'] = question
        item['answers'] = '|'.join(answer_list).replace(' ', '').replace('\n', '')
        return item

