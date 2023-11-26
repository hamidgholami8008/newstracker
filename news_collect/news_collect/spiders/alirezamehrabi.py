from typing import Iterable

import scrapy
from scrapy import Request


class AlirezamehrabiSpider(scrapy.Spider):
    name = "alirezamehrabi"
    allowed_domains = ["alirezamehrabi.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://alirezamehrabi.com/news/bourse", callback=self.parse)

    def parse(self, response):

        for the_link in response.xpath("//div[@data-aos]/a"):
            yield scrapy.Request(url=the_link.xpath(".//@href").get(), callback=self.parse_text)

    def parse_text(self, response):

        list_of_sentences = []
        for detail in response.xpath("//div[@class='blog-details-desc']"):
            for text in detail.xpath(".//div[2]/p/text()"):
                list_of_sentences.append(text.get())
            yield {
                'title': detail.xpath(".//div/div/span/h5/text()").get(),
                'link': response.request.url,
                'sentence': ''.join(list_of_sentences)
            }
            list_of_sentences = []
