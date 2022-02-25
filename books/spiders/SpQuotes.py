from scrapy.spiders import Spider

from scrapy_splash import SplashRequest

from books.items import QuotesItem


class SpquotesSpider(Spider):
    name = "spquotes"


    def start_requests(self):
        url = "http://quotes.toscrape.com/js/"
        yield SplashRequest(url=url, callback=self.parse)


    def parse(self, response):

        for quote in response.xpath('//div[@class="quote"]'):

            yield QuotesItem(
                quote = quote.xpath('.//span[@class="text"]/text()').get(),
                author = quote.xpath('.//small[@class="author"]/text()').get(),
                tags = quote.xpath('.//a[@class="tag"]/text()').getall()
            )

        next_page = response.xpath('//li[@class="next"]/a/@href').get()

        if next_page is not None:

            yield SplashRequest(
                response.urljoin(next_page),
                callback=self.parse,
            )
