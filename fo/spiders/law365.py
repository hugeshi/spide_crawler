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

logger = logging.getLogger('Slaw365logger')


class Slaw365(scrapy.spiders.Spider):
    name = "law365"
    allowed_domains = ["law365.legaldaily.com.cn"]
    site_url = "http://law365.legaldaily.com.cn"
    start_urls = [
        "http://law365.legaldaily.com.cn/ecard/search/query_select?q_lock=1&"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Host": "law365.legaldaily.com.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    def parse(self, response):
        selector = Selector(response)
        questions = selector.xpath('//tr[td[@class="f14 yh"]]')
        for question in questions:
            item = QuestionItem()
            tag = question.xpath('td[1]/text()').extract()[0]
            title = question.xpath('td[2]/a/text()').extract()[0]
            url = question.xpath('td[2]/a/@href').extract()[0]
            item['parent'] = response.url
            item['url'] = str(url)
            item['tag'] = tag
            item['title'] = title
            request = scrapy.Request(str(url), headers=self.headers,
                                     callback=self.parse_sub_page, dont_filter=True)
            request.meta['item'] = item
            yield request
        word = u'下一页'
        next_pages = selector.xpath('//a[text()="%s"]/@href' % word).extract()
        if next_pages:
            next_page = next_pages[0]
            logger.info('parse next page============ %s', str(next_page))
            yield scrapy.Request(str(next_page), headers=self.headers,
                                 callback=self.parse, dont_filter=True)

    def parse_sub_page(self, response):
        item = response.meta['item']
        # parse response and populate item as required
        selector = Selector(response)
        text = selector.xpath('//div[@class="show_content"]/span').extract()[0]
        soup = BeautifulSoup(text, 'lxml')
        question = ''.join(soup.find_all(text=True)).replace(' ', '').replace('\n', '')
        answers = selector.xpath('//div[@class="org_box"]/div/p').extract()
        answer_list = []
        for answer in answers:
            soup_answer = BeautifulSoup(answer, 'lxml')
            answer = ''.join(soup_answer.find_all(text=True))
            answer_list.append(answer)
        item['question'] = question
        item['answers'] = '|'.join(answer_list).replace(' ', '').replace('\n', '')
        return item

