import scrapy


class PolimalinewsSpider(scrapy.Spider):
    name = "tejaratnews"
    allowed_domains = ["tejaratnews.com"]

    page_number = 2
    substring = "آبان"


    def start_requests(self):
        yield scrapy.Request(url="https://tejaratnews.com/tags/%D8%A8%D8%A7%D8%B2%D8%A7%D8%B1_%D8%B3%D9%87%D8%A7%D9%85/?page=1",
                              callback=self.parse)

    def parse(self, response):
        for content in response.xpath("//div[@class='content']"):

            title_text: str = content.xpath(".//a/@title").get()

            if self.substring not in title_text:
                yield {
                    'title': title_text
                }
            else:
                title_text = ''.join(filter(lambda x: not x.isdigit(), title_text))
                yield {
                    'title': title_text.replace(self.substring, '')
                }

        next_url = str(f"https://tejaratnews.com/tags/%D8%A8%D8%A7%D8%B2%D8%A7%D8%B1_%D8%B3%D9%87%D8%A7%D9%85/?page={self.page_number}")
        self.page_number += 1

        yield scrapy.Request(url=next_url, callback=self.parse)
