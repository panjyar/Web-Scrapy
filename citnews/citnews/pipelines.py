# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter


# class CitnewsPipeline:
#     def process_item(self, item, spider):
#         return item

import pymongo

class MongoDBPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create the pipeline
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'cit_scrapy')
        )

    def open_spider(self, spider):
        # Initialize MongoDB connection when the spider is opened
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # Close the MongoDB connection when the spider is closed
        self.client.close()

    def process_item(self, item, spider):
        # Insert the item into the MongoDB collection
        collection_name = item.__class__.__name__.lower()
        self.db[collection_name].insert_one(dict(item))
        return item
