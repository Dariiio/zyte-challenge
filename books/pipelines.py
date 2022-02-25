import json

from itemadapter import ItemAdapter

class BooksPipeline:

    def open_spider(self, spider):
        self.file = open('scraped_items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
