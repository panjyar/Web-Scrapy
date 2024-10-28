import pymongo
from .items import CitnewsItem
from .items import IITGnewsItem
from .items import NITSItems
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
        # Define the collection name based on the item's class name
        collection_name = item.__class__.__name__.lower()
        
        # Set up unique identifiers based on the item class to prevent duplicates
        if isinstance(item, CitnewsItem):
            query = {'newslink': item.get('newslink')} if item.get('newslink') else {'noticeUrl': item.get('noticeUrl')}
        elif isinstance(item, IITGnewsItem):
            query = {'newslink': item.get('newslink')}
        elif isinstance(item, NITSItems):
            query = {'latestNewsurlnits': item.get('latestNewsurlnits')}
        else:
            query = {}

        # Use upsert to insert the item if it does not exist, or update if it does
        self.db[collection_name].update_one(query, {'$set': dict(item)}, upsert=True)
        
        return item
