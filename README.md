
# Welcome! 😀

## Solution 1 🕸

[Zyte Dashboard](https://app.zyte.com/p/584545/jobs)

[Download CSV](book_data.csv)

~~~~python
from scrapy.http import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from books.items import BooksItem


class SpbooksSpider(CrawlSpider):
    name = "spbooks"
    start_urls = ["http://books.toscrape.com/"]

    rules = [
        Rule(
            LinkExtractor(restrict_xpaths="//ul/li/ul/li/a"),
            callback="parse_item",
            follow=True,
        ),
    ]

    def parse_item(self, response):


        for book in response.xpath('//article[@class="product_pod"]'):
            yield BooksItem(
                title = book.xpath(".//a[@title]/@title").get(),
                detail_page_url = response.urljoin(
                    book.xpath(".//a[@title]//@href").get(),
                ),
                img_url = response.urljoin(
                    book.xpath('.//img[@class="thumbnail"]/@src').get(),
                ),
                price = book.xpath('.//p[@class="price_color"]//text()').get()
            )

        next_page = response.xpath('//li[@class="next"]/a//@href').get()

        if next_page is not None:
            yield Request(
                response.urljoin(next_page),
                callback=self.parse_item,
            )

~~~~


## Solution 2 🕷

[Download CSV](quote_data.csv)


~~~~python
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

~~~~