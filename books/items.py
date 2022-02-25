from scrapy.item import Item, Field
from itemloaders.processors import Join, MapCompose


class BooksItem(Item):

    title = Field()
    price = Field()
    img_url = Field()
    detail_page_url = Field()


class QuotesItem(Item):
    quote = Field()
    author = Field()
    tags = Field()