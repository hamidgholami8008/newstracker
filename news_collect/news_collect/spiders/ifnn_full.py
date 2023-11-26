import scrapy
from scrapy import Request
import requests


class IfnnFullSpider(scrapy.Spider):
    name = "ifnn_full"

    next_page_number = 2

    def start_requests(self):
        yield scrapy.Request(url="https://ifnn.ir/category/%d8%a7%d8%ae%d8%a8%d8%a7%d8%b1/", callback=self.parse)

    def parse(self, response):

        for article_link in response.xpath("//article"):
            yield scrapy.Request(url=article_link.xpath('.//div/h2/a/@href').get(), callback=self.parse_content)

        new_url = str(f"https://ifnn.ir/category/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/page/{self.next_page_number}/")
        next_page = requests.get(new_url)
        self.next_page_number += 1

        if next_page.status_code == 200:

            yield scrapy.Request(url=new_url, callback=self.parse)

    def parse_content(self, response):

        list_of_sentences = []
        for item in response.xpath('//div[@class="single"]'):
            for text in item.xpath('.//div[@class="contentsingle"]/p/text()'):
                list_of_sentences.append(text.get())
            yield {
                'title': item.xpath(".//h1/a/text()").get(),
                'link': response.request.url,
                'sentence': ''.join(list_of_sentences)
            }
            list_of_sentences = []

