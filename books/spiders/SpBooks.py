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

        title = response.xpath("//a[@title]/@title").getall()
        detail_page_url = response.xpath("//a[@title]//@href").getall()
        img_url = response.xpath('//img[@class="thumbnail"]/@src').getall()
        price = response.xpath('//p[@class="price_color"]//text()').getall()

        next_page = response.xpath('//li[@class="next"]/a//@href').get()

        results = zip(title, detail_page_url, img_url, price)
        for r in results:
            yield BooksItem(
                title=r[0],
                detail_page_url=response.urljoin(r[1]),
                img_url=response.urljoin(r[2]),
                price=r[3],
            )

        if next_page is not None:
            print(response.urljoin(next_page))
            yield Request(
                response.urljoin(next_page),
                callback=self.parse_item,
            )
