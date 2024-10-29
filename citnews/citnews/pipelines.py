import pymongo
from .items import CitnewsItem, IITGnewsItem, NITSItems  # Import all item classes

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # Create the pipeline with MongoDB URI and database name from settings
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'All_College')
        )

    def open_spider(self, spider):
     
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
       
        self.client.close()

    def process_item(self, item, spider):
        
        if item.get('news') and item.get('newslink'):
            collection_name = 'news'
            query = {'newslink': item.get('newslink')}
        
        elif item.get('noticeTitle') and item.get('noticeUrl'):
            collection_name = 'notices'
            query = {'noticeUrl': item.get('noticeUrl')}
        
        elif item.get('tenderTitle') and item.get('tenderUrl'):
            collection_name = 'tenders'
            query = {'tenderUrl': item.get('tenderUrl')}
        
        elif item.get('eventName') and item.get('eventInfo') and item.get('eventDate'):
            collection_name = 'upcoming_events'
            query = {'eventInfo': item.get('eventInfo')}

        else:
        
            collection_name = 'misc_data'
            query = {}

        # Use update_one with upsert=True to insert or update based on the unique identifier (query)
        self.db[collection_name].update_one(query, {'$set': dict(item)}, upsert=True)

        return item
