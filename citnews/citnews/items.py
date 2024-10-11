# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CitnewsItem(scrapy.Item):
    # define the fields for your item here like:
    news = scrapy.Field()
    newslink = scrapy.Field()
    noticeUrl = scrapy.Field()
    noticeTitle = scrapy.Field()
    tenderUrl = scrapy.Field()
    tenderTitle = scrapy.Field()
    eventDate = scrapy.Field()
    eventInfo = scrapy.Field()
    eventName = scrapy.Field()

class IITGnewsItem(scrapy.Item):
    # define the fields for your item here like:
    latestNewstitle = scrapy.Field()
    latestNewsurl = scrapy.Field()
    eventName = scrapy.Field()
    eventDate = scrapy.Field()
    eventInfo = scrapy.Field()
    # tenderTitle = scrapy.Field()
    eventName = scrapy.Field()
    eventDate = scrapy.Field()
    eventInfo = scrapy.Field()
    

class NITSItems(scrapy.Item):
    latestNews = scrapy.Field()
    latestNewsUrl = scrapy.Field()
    latestNewstitlenits = scrapy.Field()
    latestNewsurlnits = scrapy.Field()

    pass