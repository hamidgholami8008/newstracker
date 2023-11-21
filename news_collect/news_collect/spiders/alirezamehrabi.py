from typing import Iterable

import scrapy
from scrapy import Request


class AlirezamehrabiSpider(scrapy.Spider):
    name = "alirezamehrabi"
    allowed_domains = ["alirezamehrabi.com"]

    def start_requests(self):
        yield scrapy.Request(url="https://alirezamehrabi.com", callback=self.parse,
                             meta={
                                 'splash': {
                                     'endpoint': 'render.html',
                                     'args': {'wait': 0.1}
                                 }
                             })

    def parse(self, response):
        for title in response.xpath("//h3/text()"):
            yield {
                'title': title.get()
            }
