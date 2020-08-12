from scrapy.exceptions import DropItem
from pymongo import MongoClient


class ValidationPipeline(object):

    def process_item(self, item, spider):
        if not item['title']:
            raise DropItem('Title missing')

        return item


class MongoPipeline(object):
    """ Save an item into MongoDB """

    def open_spider(self, spider):
        """ Connect to the MongoDB when Spider initiates """

        self.client = MongoClient('localhost', 27017)
        self.db = self.client['scraping-book']
        self.collection = self.db['items']

    def close_spider(self, spider):
        """ Close connection to the Mongo at the end of Spider """

        self.client.close()

    def process_item(self, item, spider):
        """ Add an item into the collection """

        self.collection.insert_one(dict(item))
        return item