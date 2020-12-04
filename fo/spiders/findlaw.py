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
    name = "findlaw"
    allowed_domains = ["findlaw.cn"]
    site_url = "http://china.findlaw.cn"
    start_urls = [
        "http://china.findlaw.cn/ask/d200401_t01",
        "http://china.findlaw.cn/ask/d200402_t01",
        "http://china.findlaw.cn/ask/d200403_t01",
        "http://china.findlaw.cn/ask/d200404_t01",
        "http://china.findlaw.cn/ask/d200405_t01",
        "http://china.findlaw.cn/ask/d200406_t01",
        "http://china.findlaw.cn/ask/d200407_t01",
        "http://china.findlaw.cn/ask/d200408_t01",
        "http://china.findlaw.cn/ask/d200409_t01",
        "http://china.findlaw.cn/ask/d200410_t01",
        "http://china.findlaw.cn/ask/d200411_t01",
        "http://china.findlaw.cn/ask/d200412_t01",
        "http://china.findlaw.cn/ask/d200501_t01",
        "http://china.findlaw.cn/ask/d200502_t01",
        "http://china.findlaw.cn/ask/d200503_t01",
        "http://china.findlaw.cn/ask/d200504_t01",
        "http://china.findlaw.cn/ask/d200505_t01",
        "http://china.findlaw.cn/ask/d200506_t01",
        "http://china.findlaw.cn/ask/d200507_t01",
        "http://china.findlaw.cn/ask/d200508_t01",
        "http://china.findlaw.cn/ask/d200509_t01",
        "http://china.findlaw.cn/ask/d200510_t01",
        "http://china.findlaw.cn/ask/d200511_t01",
        "http://china.findlaw.cn/ask/d200512_t01",
        "http://china.findlaw.cn/ask/d200601_t01",
        "http://china.findlaw.cn/ask/d200602_t01",
        "http://china.findlaw.cn/ask/d200603_t01",
        "http://china.findlaw.cn/ask/d200604_t01",
        "http://china.findlaw.cn/ask/d200605_t01",
        "http://china.findlaw.cn/ask/d200606_t01",
        "http://china.findlaw.cn/ask/d200607_t01",
        "http://china.findlaw.cn/ask/d200608_t01",
        "http://china.findlaw.cn/ask/d200609_t01",
        "http://china.findlaw.cn/ask/d200610_t01",
        "http://china.findlaw.cn/ask/d200611_t01",
        "http://china.findlaw.cn/ask/d200612_t01",
        "http://china.findlaw.cn/ask/d200701_t01",
        "http://china.findlaw.cn/ask/d200702_t01",
        "http://china.findlaw.cn/ask/d200703_t01",
        "http://china.findlaw.cn/ask/d200704_t01",
        "http://china.findlaw.cn/ask/d200705_t01",
        "http://china.findlaw.cn/ask/d200706_t01",
        "http://china.findlaw.cn/ask/d200707_t01",
        "http://china.findlaw.cn/ask/d200708_t01",
        "http://china.findlaw.cn/ask/d200709_t01",
        "http://china.findlaw.cn/ask/d200710_t01",
        "http://china.findlaw.cn/ask/d200711_t01",
        "http://china.findlaw.cn/ask/d200712_t01",
        "http://china.findlaw.cn/ask/d200801_t01",
        "http://china.findlaw.cn/ask/d200802_t01",
        "http://china.findlaw.cn/ask/d200803_t01",
        "http://china.findlaw.cn/ask/d200804_t01",
        "http://china.findlaw.cn/ask/d200805_t01",
        "http://china.findlaw.cn/ask/d200806_t01",
        "http://china.findlaw.cn/ask/d200807_t01",
        "http://china.findlaw.cn/ask/d200808_t01",
        "http://china.findlaw.cn/ask/d200809_t01",
        "http://china.findlaw.cn/ask/d200810_t01",
        "http://china.findlaw.cn/ask/d200811_t01",
        "http://china.findlaw.cn/ask/d200812_t01",
        "http://china.findlaw.cn/ask/d200901_t01",
        "http://china.findlaw.cn/ask/d200902_t01",
        "http://china.findlaw.cn/ask/d200903_t01",
        "http://china.findlaw.cn/ask/d200904_t01",
        "http://china.findlaw.cn/ask/d200905_t01",
        "http://china.findlaw.cn/ask/d200906_t01",
        "http://china.findlaw.cn/ask/d200907_t01",
        "http://china.findlaw.cn/ask/d200908_t01",
        "http://china.findlaw.cn/ask/d200909_t01",
        "http://china.findlaw.cn/ask/d200910_t01",
        "http://china.findlaw.cn/ask/d200911_t01",
        "http://china.findlaw.cn/ask/d200912_t01",
        "http://china.findlaw.cn/ask/d201001_t01",
        "http://china.findlaw.cn/ask/d201002_t01",
        "http://china.findlaw.cn/ask/d201003_t01",
        "http://china.findlaw.cn/ask/d201004_t01",
        "http://china.findlaw.cn/ask/d201005_t01",
        "http://china.findlaw.cn/ask/d201006_t01",
        "http://china.findlaw.cn/ask/d201007_t01",
        "http://china.findlaw.cn/ask/d201008_t01",
        "http://china.findlaw.cn/ask/d201009_t01",
        "http://china.findlaw.cn/ask/d201010_t01",
        "http://china.findlaw.cn/ask/d201011_t01",
        "http://china.findlaw.cn/ask/d201012_t01",
        "http://china.findlaw.cn/ask/d201101_t01",
        "http://china.findlaw.cn/ask/d201102_t01",
        "http://china.findlaw.cn/ask/d201103_t01",
        "http://china.findlaw.cn/ask/d201104_t01",
        "http://china.findlaw.cn/ask/d201105_t01",
        "http://china.findlaw.cn/ask/d201106_t01",
        "http://china.findlaw.cn/ask/d201107_t01",
        "http://china.findlaw.cn/ask/d201108_t01",
        "http://china.findlaw.cn/ask/d201109_t01",
        "http://china.findlaw.cn/ask/d201110_t01",
        "http://china.findlaw.cn/ask/d201111_t01",
        "http://china.findlaw.cn/ask/d201112_t01",
        "http://china.findlaw.cn/ask/d201201_t01",
        "http://china.findlaw.cn/ask/d201202_t01",
        "http://china.findlaw.cn/ask/d201203_t01",
        "http://china.findlaw.cn/ask/d201204_t01",
        "http://china.findlaw.cn/ask/d201205_t01",
        "http://china.findlaw.cn/ask/d201206_t01",
        "http://china.findlaw.cn/ask/d201207_t01",
        "http://china.findlaw.cn/ask/d201208_t01",
        "http://china.findlaw.cn/ask/d201209_t01",
        "http://china.findlaw.cn/ask/d201210_t01",
        "http://china.findlaw.cn/ask/d201211_t01",
        "http://china.findlaw.cn/ask/d201212_t01",
        "http://china.findlaw.cn/ask/d201301_t01",
        "http://china.findlaw.cn/ask/d201302_t01",
        "http://china.findlaw.cn/ask/d201303_t01",
        "http://china.findlaw.cn/ask/d201304_t01",
        "http://china.findlaw.cn/ask/d201305_t01",
        "http://china.findlaw.cn/ask/d201306_t01",
        "http://china.findlaw.cn/ask/d201307_t01",
        "http://china.findlaw.cn/ask/d201308_t01",
        "http://china.findlaw.cn/ask/d201309_t01",
        "http://china.findlaw.cn/ask/d201310_t01",
        "http://china.findlaw.cn/ask/d201311_t01",
        "http://china.findlaw.cn/ask/d201312_t01",
        "http://china.findlaw.cn/ask/d201401_t01",
        "http://china.findlaw.cn/ask/d201402_t01",
        "http://china.findlaw.cn/ask/d201403_t01",
        "http://china.findlaw.cn/ask/d201404_t01",
        "http://china.findlaw.cn/ask/d201405_t01",
        "http://china.findlaw.cn/ask/d201406_t01",
        "http://china.findlaw.cn/ask/d201407_t01",
        "http://china.findlaw.cn/ask/d201408_t01",
        "http://china.findlaw.cn/ask/d201409_t01",
        "http://china.findlaw.cn/ask/d201410_t01",
        "http://china.findlaw.cn/ask/d201411_t01",
        "http://china.findlaw.cn/ask/d201412_t01",
        "http://china.findlaw.cn/ask/d201501_t01",
        "http://china.findlaw.cn/ask/d201502_t01",
        "http://china.findlaw.cn/ask/d201503_t01",
        "http://china.findlaw.cn/ask/d201504_t01",
        "http://china.findlaw.cn/ask/d201505_t01",
        "http://china.findlaw.cn/ask/d201506_t01",
        "http://china.findlaw.cn/ask/d201507_t01",
        "http://china.findlaw.cn/ask/d201508_t01",
        "http://china.findlaw.cn/ask/d201509_t01",
        "http://china.findlaw.cn/ask/d201510_t01",
        "http://china.findlaw.cn/ask/d201511_t01",
        "http://china.findlaw.cn/ask/d201512_t01",
        "http://china.findlaw.cn/ask/d201601_t01",
        "http://china.findlaw.cn/ask/d201602_t01",
        "http://china.findlaw.cn/ask/d201603_t01",
        "http://china.findlaw.cn/ask/d201604_t01",
        "http://china.findlaw.cn/ask/d201605_t01",
        "http://china.findlaw.cn/ask/d201606_t01",
        "http://china.findlaw.cn/ask/d201607_t01",
        "http://china.findlaw.cn/ask/d201608_t01",
        "http://china.findlaw.cn/ask/d201609_t01",
        "http://china.findlaw.cn/ask/d201610_t01",
        "http://china.findlaw.cn/ask/d201611_t01",
        "http://china.findlaw.cn/ask/d201612_t01",
        "http://china.findlaw.cn/ask/d201701_t01",
        "http://china.findlaw.cn/ask/d201702_t01",
        "http://china.findlaw.cn/ask/d201703_t01",
        "http://china.findlaw.cn/ask/d201704_t01",
        "http://china.findlaw.cn/ask/d201705_t01",
        "http://china.findlaw.cn/ask/d201706_t01",
        "http://china.findlaw.cn/ask/d201707_t01",
        "http://china.findlaw.cn/ask/d201708_t01",
        "http://china.findlaw.cn/ask/d201709_t01",
        "http://china.findlaw.cn/ask/d201710_t01",
        "http://china.findlaw.cn/ask/d201711_t01",
        "http://china.findlaw.cn/ask/d201712_t01",
        "http://china.findlaw.cn/ask/d201801_t01",
        "http://china.findlaw.cn/ask/d201802_t01",
        "http://china.findlaw.cn/ask/d201803_t01",
        "http://china.findlaw.cn/ask/d201804_t01",
        "http://china.findlaw.cn/ask/d201805_t01",
        "http://china.findlaw.cn/ask/d201806_t01",
        "http://china.findlaw.cn/ask/d201807_t01",
        "http://china.findlaw.cn/ask/d201808_t01",
        "http://china.findlaw.cn/ask/d201809_t01",
        "http://china.findlaw.cn/ask/d201810_t01",
        "http://china.findlaw.cn/ask/d201811_t01",
        "http://china.findlaw.cn/ask/d201812_t01"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Host": "china.findlaw.cn",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    def parse(self, response):
        selector = Selector(response)
        questions = selector.xpath('//ul[@class="result-list"]/li[@class="list-item"]')
        print len(questions)
        for question in questions:
            item_num = question.xpath('div/span[@class="rli-item item-num"]/text()').extract()[0]
            if item_num and "0个" == item_num:
                continue
            item = QuestionItem()
            url = question.xpath('div/a[@class="rli-item item-link"]/@href').extract()[0]
            title = question.xpath('div/a[@class="rli-item item-link"]/@title').extract()[0]
            item['parent'] = response.url
            item['url'] = url
            item['tag'] = question.xpath('div/span[@class="rli-item item-classify"]/text()').extract()[0]
            item['title'] = title
            request = scrapy.Request(url, headers=self.headers,
                                     callback=self.parse_sub_page, dont_filter=True)
            request.meta['item'] = item
            yield request
        word = u'下页'
        next_pages = selector.xpath('//a[text()="%s"]/@href' % word).extract()
        if next_pages:
            if len(next_pages[0]) > 0:
                next_page = next_pages[0]
                logger.info('parse next page============ %s', str(next_page))
                yield scrapy.Request(str(next_page), headers=self.headers,
                                        callback=self.parse, dont_filter=True)

    def parse_sub_page(self, response):
        item = response.meta['item']
        # parse response and populate item as required
        selector = Selector(response)
        question_text = selector.xpath('//p[@class="question-text"]/text()').extract()
        if question_text:
            text = question_text[0]
            print text
        else:
            text = selector.xpath('//div[@class ="wl_13"]/p/text()').extract()[0]
            print text
        soup = BeautifulSoup(text, 'lxml')
        question = ''.join(soup.find_all(text=True)).replace(' ', '').replace('\n', '')
        answers = selector.xpath('//div[@class="answer-text"]/text()').extract()
        if not answers:
            answers = selector.xpath('//p[@class="wla_22"]/text()').extract()
        answer_list = []
        for answer in answers:
            answer_list.append(answer)
            break
        item['question'] = question
        item['answers'] = '|'.join(answer_list).replace(' ', '').replace('\n', '')
        return item

