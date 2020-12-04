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
    name = "110com"
    allowed_domains = ["110.com"]
    site_url = "http://www.110.com"
    start_urls = [
        "http://www.110.com/ask/browse-s2c0r0.html"
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
        selector = Selector(response)
        questions = selector.xpath('//div[@class="tit07"]')
        for question in questions:
            item = QuestionItem()
            texts = question.xpath('.//a[@class="hui"]/text()').extract()
            if texts:
                if len(texts) == 2:
                    tag = texts[1]
                elif len(texts) == 1:
                    tag = texts[0]
            title = question.xpath('.//a[contains(@href,"/ask/question-")]/text()').extract()[0]
            url = question.xpath('.//a[contains(@href,"/ask/question-")]/@href').extract()[0]
            full_url = self.site_url + str(url)
            item['parent'] = response.url
            item['url'] = full_url
            item['tag'] = tag
            item['title'] = title
            request = scrapy.Request(full_url, headers=self.headers,
                                     callback=self.parse_sub_page, dont_filter=True)
            request.meta['item'] = item
            yield request
        word = u'下一页'
        next_pages = selector.xpath('//a[text()="%s"]/@href' % word).extract()
        if next_pages:
            next_page = next_pages[0]
            logger.info('parse next page============ %s', self.site_url + str(next_page))
            yield scrapy.Request(self.site_url + str(next_page), headers=self.headers,
                                    callback=self.parse, dont_filter=True)

    def parse_sub_page(self, response):
        item = response.meta['item']
        # parse response and populate item as required
        selector = Selector(response)
        text = selector.xpath('//div[@class="xwz"]').extract()[0]
        soup = BeautifulSoup(text, 'lxml')
        question = ''.join(soup.find_all(text=True)).replace(' ', '').replace('\n', '')
        answers = selector.xpath('//div[@class="zjdanr"]/text()').extract()
        answer_list = []
        for answer in answers:
            answer_list.append(answer)
            break
        item['question'] = question
        item['answers'] = '|'.join(answer_list).replace(' ', '').replace('\n', '')
        return item

