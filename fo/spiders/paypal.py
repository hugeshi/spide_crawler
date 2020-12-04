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

logger = logging.getLogger('PaypalCommunitylogger')


class PaypalCommunity(scrapy.spiders.Spider):
    name = "paypal"
    allowed_domains = ["paypal-community.com"]
    site_url = "https://www.paypal-community.com"
    start_urls = [
        "https://www.paypal-community.com/t5/PayPal-Basics/bd-p/1",
        "https://www.paypal-community.com/t5/Payments/bd-p/2",
        "https://www.paypal-community.com/t5/My-Money/bd-p/3",
        "https://www.paypal-community.com/t5/My-Account/bd-p/4",
        "https://www.paypal-community.com/t5/Disputes-and-Limitations/bd-p/5",
        "https://www.paypal-community.com/t5/Products-and-Services/bd-p/6",
        "https://www.paypal-community.com/t5/PayPal-Credit/bd-p/7"
    ]

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh-TW;q=0.7,zh;q=0.6",
        "Connection": "keep-alive",
        "Host": "www.paypal-community.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

    def parse(self, response):
        selector = Selector(response)
        questions = selector.xpath('//div[@id="messageList"]//tr[contains(@class,"lia-list-row")]')
        print len(questions)
        for question in questions:
            replies_num = question.xpath(
                './/div[@class="lia-component-messages-column-message-replies-count"]/span/text()').extract()[0]
            if replies_num is None or int(str(replies_num).strip()) == 0:
                continue
            item = QuestionItem()
            item['replies'] = str(replies_num).strip()

            views_num = \
            question.xpath('.//div[@class="lia-component-messages-column-message-views-count"]/span/text()').extract()[
                0]
            item['views'] = str(views_num).strip()
            url = question.xpath('.//a[@class="page-link lia-link-navigation lia-custom-event"]/@href').extract()[0]
            if url:
                item['subject'] = str(url).split('/')[2]
            title = question.xpath('.//a[@class="page-link lia-link-navigation lia-custom-event"]/text()').extract()[0]
            item['title'] = title.replace('\t', '').replace('\n', '').replace(u'\xa0', ' ')
            item['answers'] = []
            request = scrapy.Request(self.site_url + str(url), headers=self.headers,
                                     callback=self.parse_sub_page, dont_filter=True)
            request.meta['item'] = item
            yield request
        word = u'next'
        next_pages = selector.xpath('//link[@rel="%s"]/@href' % word).extract()
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
        if not item.get('question', None):
            question_text = selector.xpath('//div[@class="lia-message-body-content"]').extract()
            question = ""
            if question_text:
                text = question_text[0]
                soup = BeautifulSoup(text, 'lxml')
                question = ' '.join(soup.find_all(text=True)).replace('\t', '').replace('\n', '').replace(u'\xa0', ' ')

            item['question'] = question

            tags = selector.xpath('//li[contains(@class,"lia-tag-list-item")]/a/text()').extract()
            tags_result = ""
            if tags:
                tags_result = '|'.join(tags)
            item['tags'] = tags_result

            labels = selector.xpath('//a[@class="label-link lia-link-navigation lia-custom-event"]/text()').extract()
            labels_result = ""
            if labels:
                labels_result = '|'.join(labels)
            item['labels'] = labels_result

            problems_ratings = selector.xpath('//a[@class="lia-link-navigation lia-rating-value-summary"]/text()').extract()
            problems_ratings_result = ""
            if problems_ratings:
                problems_ratings_result = str(problems_ratings[0]).strip()
            item['problems_ratings'] = problems_ratings_result

        answers = selector.xpath(
            '//div[@class="lia-component-reply-list"]/div/div[@class="lia-linear-display-message-view"]')
        print len(answers)
        if answers:
            for answer in answers:
                accepted = "0"
                resolved = answer.xpath(
                    './/div[@class="MessageView lia-message-view-forum-message lia-message-view-display lia-row-standard-unread lia-thread-reply lia-list-row-thread-solved lia-accepted-solution"]').extract()
                if resolved:
                    accepted = "1"
                kudos = answer.xpath(
                    './/span[@class="MessageKudosCount lia-component-kudos-widget-message-kudos-count"]/text()').extract()
                if kudos:
                    kudo_num = str(kudos[0]).strip()
                accept_answer = answer.xpath('.//div[@class="lia-message-body-content"]').extract()
                if accept_answer:
                    answer_soup = BeautifulSoup(accept_answer[0], 'lxml')
                    answer_text = ' '.join(answer_soup.find_all(text=True)).replace('\t', '').replace('\n', '').replace(
                        u'\xa0', ' ')
                item['answers'].append('|'.join([answer_text, kudo_num, accepted]))
        word = u'Next Page'
        next_pages = selector.xpath('//a[@aria-label="%s"]/@href' % word).extract()
        if next_pages:
            if len(next_pages[0]) > 0:
                next_page = next_pages[0]
                logger.info('parse sub next page============ %s', str(next_page))
                sub_request = scrapy.Request(str(next_page), headers=self.headers,
                                             callback=self.parse_sub_page, dont_filter=True)
                sub_request.meta['item'] = item
                yield sub_request
        else:
            yield item
