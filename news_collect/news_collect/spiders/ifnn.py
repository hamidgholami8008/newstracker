import requests
import scrapy
from scrapy_selenium import SeleniumRequest


class IfnnSpider(scrapy.Spider):
    name = "ifnn"


    next_page_number = 2

    def start_requests(self):
        yield SeleniumRequest(url="https://ifnn.ir/category/%d8%a7%d8%ae%d8%a8%d8%a7%d8%b1/",
                              wait_time=1,
                              callback=self.parse)

    def parse(self, response):

        for article in response.xpath("//article[@class='article item']"):
            yield {
                'title' : article.xpath(".//a/@title").get(),
                'link' : article.xpath(".//a/@href").get(),
                'summary' : article.xpath(".//div/div[@class='body']/text()").get()
            }

        new_url = str(f"https://ifnn.ir/category/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1/page/{self.next_page_number}/")
        next_page = requests.get(new_url)
        self.next_page_number += 1

        if next_page.status_code == 200:

            yield SeleniumRequest(url=new_url,
                                  wait_time=0.1,
                                  callback=self.parse)

