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
