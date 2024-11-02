import scrapy
import datetime
from datetime import datetime
from ..items import CitnewsItem
from ..items import IITGnewsItem
from ..items import NITSItems
from ..items import NITAItems
from ..items import IITDItems
class CitSpider(scrapy.Spider):
    name = "cit"
    allowed_domains = ["cit.ac.in" , "iitg.ac.in" , "nits.ac.in" , "nita.ac.in" , "home.iitd.ac.in/"]
    start_urls = ["https://cit.ac.in" , "https://iitg.ac.in" , "http://www.nits.ac.in/" , "https://www.nita.ac.in/" , "https://home.iitd.ac.in/"]


    def parse(self, response):
        
        if "iitd.ac.in" in response.url:
            self.logger.info('------------------------------SCRAPPING IIT Delhi  WEBSITE---------------------------------')
            yield from self.parse_iitd(response)
        
        elif "nita.ac.in" in response.url:
            self.logger.info('------------------------------SCRAPPING NITS WEBSITE---------------------------------')
            yield from self.parse_nita(response)
        
        elif "cit.ac.in" in response.url:
            self.logger.info('------------------------SCRAPPING CIT WEBSITE-----------------------------')
            yield from self.parse_cit(response)

        elif "iitg.ac.in" in response.url:
            self.logger.info('--------------------------------SCRAPPING IITG WEBSITE-------------------------------------------')
            yield from self.parse_iitg(response)

        elif "nits.ac.in" in response.url:
            self.logger.info('------------------------------SCRAPPING NITS WEBSITE---------------------------------')
            yield from self.parse_nits(response)
        
    def parse_iitd(self, response):
        self.logger.info('-------------------------------------------  SCRAPPING LATEST NEWS OF IIT Delhi----------------------------------------------------')
        
       
        def extract_news_items(news_item):
            """ Helper function to extract news and news link from a news item. """
            latestNewsitems = IITDItems()
            news = news_item.css('::text').get()
            newslink = news_item.css('::attr(href)').get()  

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink) if newslink else None

            yield latestNewsitems
            print("Extracted News for IIT Delhi:", news)
            print("Extracted IIT Delhi Link:", newslink)

        
        for news_item in response.css('#courses div.row a'):
            yield from extract_news_items(news_item)
        # Startups News
        for news_item in response.css('#startups h4 a'): 
            yield from extract_news_items(news_item)
        # Latest News
        for news_item in response.css('#news .col-md-8 h4 a'): 
            yield from extract_news_items(news_item)
        # Research
        for news_item in response.css('#research .col-md-8 h4 a'): 
            yield from extract_news_items(news_item)
        self.logger.info('----------------------Scrapping Upcoming event of  IIT Delhi ----------------------------')

        for event in response.css('div.info p '):
            eventitems = IITDItems()

            eventName = event.css('a::text').get()
            eventDate = event.css(' li::text').get()
            eventInfo = event.css('a::attr(href)').get()

            # Extract date from eventDate and convert to datetime object
            if eventDate:
                try:
                    # Extract just the date part from the string
                    date_str = eventDate.strip().replace('')
                    event_date_obj = datetime.strptime(date_str, '%b %d, %Y')  # Format: Nov 25, 2015
                    current_date = datetime.now()
                    end_date = datetime(2025, 12, 31)

                    # Check if the event date is within the specified range
                    if current_date <= event_date_obj <= end_date:
                        eventitems['eventName'] = eventName.strip() if eventName else None
                        eventitems['eventDate'] = eventDate.strip()
                        eventitems['eventInfo'] = response.urljoin(eventInfo) if eventInfo else None
                        yield eventitems
                except ValueError:
                    self.logger.warning(f"Could not parse event date: {eventDate.strip()}")

    def parse_nita(self, response):
        self.logger.info('-------------------------------------------  SCRAPPING LATEST NEWS OF NIT AGARTALA----------------------------------------------------')
        
       
        for news_item in response.css('div.news_card'): 
            latestNewsitems = NITAItems()
            
            news = news_item.css('a::text').get()
            newslink = news_item.css('a::attr(href)').get()  

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink) if newslink else None

            yield latestNewsitems
            print("Extracted News for NIT Agartala" , news)
            print("Extracted Linkn:" , newslink)

        self.logger.info('----------------------Scrapping Upcoming event of  NIT AGARTALA  ----------------------------')

        for event in response.css('div.event_box'):
            eventitems = NITAItems()

            day = event.css('div.d-flex > p.mb-0::text').get().strip()
            month = event.css('div.d-flex > p.mb-0 > span::text').get().strip()
            year = event.css('div.d-flex > p.mb-0::text').re_first(r'\d{4}')
            eventName = event.css('div.event_box > a::text').get()
            eventInfo = event.css('div.event_box > a::attr(href)').get()

            eventDate = f"{month} {day}, {year}" if day and month and year else None
        
            eventitems['eventDate'] = eventDate  
            eventitems['eventName'] = eventName
            eventitems['eventInfo'] = response.urljoin(eventInfo) if eventInfo else None
            
            yield eventitems
            print("Extracted Event Date:", eventDate)
            print("Extracted Event Title:", eventName)
            print("Event Link:", eventInfo)
    
    def parse_nits(self, response):
        self.logger.info('-------------------------------------------  SCRAPPING LATEST NEWS OF NITS----------------------------------------------------')
        
       
        for news_item in response.css('marquee a'):
            latestNewsitems = NITSItems()
            
            news = news_item.css('::text').get()
            newslink = news_item.css('::attr(href)').get()  

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink) if newslink else None

            yield latestNewsitems

        self.logger.info('---------Scrapping Latest News of NITS ---------')
        for news_item in response.css('div.newsupdatesmargin b'):
            latestNewsitems = NITSItems()
            news = news_item.css('a::text').get()
            newslink = news_item.css('a::attr(href)').get()

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink)
            yield latestNewsitems 
        # if response.url != 'http://www.nits.ac.in/newsupdates.php':
        #         yield response.follow('http://www.nits.ac.in/newsupdates.php', self.newsUpdatesnits)
    
    def newsUpdatesnits(self, response):
        self.logger.info('----------------Scrapping Latest News of NITS (All Page)--------------- ')
        for news_item in response.css('div.panel-border  b a'):
            latestNewsitems = NITSItems()
            news = news_item.css('::text').get()
            newslink = news_item.css('::attr(href)').get()

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink)
            yield latestNewsitems
        
        self.logger.info('----------------Scrapping Notice--------------- ')
    
        for notice in response.css('div#tab1 a'):
            latestNewsitems = NITSItems()
            news = news_item.css('a::text').get()
            newslink = news_item.css('a::attr(href)').get()

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink)
            yield latestNewsitems

        
        # if response.url != 'http://www.nits.ac.in/newsupdates.php':
        #     yield response.follow('http://www.nits.ac.in/newsupdates.php', self.newsUpdatesnits)

    def parse_iitg(self, response):
        self.logger.info('---------Scrapping Latest News of IITG ---------')
        for news_item in response.css('div#bn7 a'):
            latestNewsitems = IITGnewsItem()
            news = news_item.css('::text').get()
            newslink = news_item.css('::attr(href)').get()

            latestNewsitems['news'] = news.strip() if news else None
            latestNewsitems['newslink'] = response.urljoin(newslink)
            yield latestNewsitems

        self.logger.info('----------------------Scrapping Upcoming event of IITG  ----------------------------')

        for event in response.css('div.mb-15.bg-white'):
            eventitems = IITGnewsItem()

            eventName = event.css('div.testimonial a::text').get()
            eventDate = event.css('ul.text-white li::text').get()
            eventInfo = event.css('div.testimonial a::attr(href)').get()

            # Extract date from eventDate and convert to datetime object
            if eventDate:
                try:
                    # Extract just the date part from the string
                    date_str = eventDate.strip().replace('')
                    event_date_obj = datetime.strptime(date_str, '%b %d, %Y')  # Format: Nov 25, 2015
                    current_date = datetime.now()
                    end_date = datetime(2025, 12, 31)

                    # Check if the event date is within the specified range
                    if current_date <= event_date_obj <= end_date:
                        eventitems['eventName'] = eventName.strip() if eventName else None
                        eventitems['eventDate'] = eventDate.strip()
                        eventitems['eventInfo'] = response.urljoin(eventInfo) if eventInfo else None
                        yield eventitems
                except ValueError:
                    self.logger.warning(f"Could not parse event date: {eventDate.strip()}")

        # if response.url != 'https://iitg.ac.in/iitg_events_all':
        #     yield response.follow('https://iitg.ac.in/iitg_events_all', self.parse_upcommingEventOfIITG)

    def parse_upcommingEventOfIITG(self, response):
        self.logger.info('----------------------Scrapping Upcoming event of IITG (All PAGE) ----------------------------')
        for row in response.css('table tbody tr'):
            upcommingitems = IITGnewsItem()
            eventName = row.css('td a::text').get()
            eventDate = row.css('td p::text').get()
            eventInfo = row.css('td a::attr(href)').get()

            # Extract date from eventDate and convert to datetime object
            if eventDate:
                try:
                    # Extract just the date part from the string
                    date_str = eventDate.strip().replace('Date: ', '')
                    event_date_obj = datetime.strptime(date_str, '%b %d, %Y')  # Format: Nov 25, 2015
                    current_date = datetime.now()
                    end_date = datetime(2025, 12, 31)

                    # Check if the event date is within the specified range
                    if current_date <= event_date_obj <= end_date:
                        upcommingitems['eventName'] = eventName.strip() if eventName else None
                        upcommingitems['eventDate'] = eventDate.strip()
                        upcommingitems['eventInfo'] = response.urljoin(eventInfo) if eventInfo else None
                        yield upcommingitems
                except ValueError:
                    self.logger.warning(f"Could not parse event date: {eventDate.strip()}")

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_upcommingEventOfIITG)  

    def parse_cit(self, response):
        self.logger.info('----------------Scrapping Latest News--------------- ')
        for news_item in response.css('div#bn7 a'):
            latestNewsitems = CitnewsItem()
            title = news_item.css('::text').get()
            url = news_item.css('::attr(href)').get()

            latestNewsitems['news'] = title.strip() if title else None
            latestNewsitems['newslink'] = response.urljoin(url)
            yield latestNewsitems
        
        self.logger.info('----------------Scrapping Notice--------------- ')
    
        for notice in response.css('div#tab1 a'):
            noticeitems = CitnewsItem()
            noticeTitle = notice.css('::text').get()
            noticeUrl = notice.css('::attr(href)').get()

            noticeitems['noticeTitle'] = noticeTitle.strip() if noticeTitle else None
            noticeitems['noticeUrl'] = response.urljoin(noticeUrl)
            yield noticeitems

        
        # if response.url != 'https://www.cit.ac.in/pages-notices-all':
        #     yield response.follow('https://www.cit.ac.in/pages-notices-all', self.parse_notices)

        self.logger.info('----------------Scrapping Tender--------------- ')
        for tender in response.css('div#tab2 > ul li a'):
            tenderitems = CitnewsItem()
            tenderTitle = tender.css('::text').get()
            tenderUrl = tender.css('::attr(href)').get()

            tenderitems['tenderTitle'] = tenderTitle.strip() if tenderTitle else None
            tenderitems['tenderUrl'] = response.urljoin(tenderUrl)
            yield tenderitems
        # if response.url != 'https://www.cit.ac.in/pages-tenders-all':
        #     yield response.follow('https://www.cit.ac.in/pages-tenders-all', self.parse_tender)
        
        self.logger.info('-----------------------------------Upcoming Events------------------------------------------------------')
        for event in response.css('div.mb-15.bg-white'):
            eventitems = CitnewsItem()
            
            eventDate = event.css('ul.text-white li::text').get()
            eventName = event.css('div.testimonial a::text').get()
            eventInfo = event.css('div.testimonial a::attr(href)').get()
            
            eventitems['eventDate'] = eventDate.strip() if eventDate else None
            eventitems['eventName'] = eventName.strip() if eventName else None
            eventitems['eventInfo'] = response.urljoin(eventInfo) if eventInfo else None
            self.logger.info(f"Extracted event: {eventName}, date: {eventDate}, info link: {eventInfo}")

            yield eventitems

        
    def parse_notices(self, response):
        self.logger.info('---------Scrapping Notices from Notices Page---------')
        for row in response.css('table tbody tr'):
            noticeitems = CitnewsItem()
            noticeTitle = row.css('td a::text').get()
            noticeUrl = row.css('td a::attr(href)').get()

            if noticeTitle and noticeUrl:
                noticeitems['noticeTitle'] = noticeTitle.strip()
                noticeitems['noticeUrl'] = response.urljoin(noticeUrl)
                yield noticeitems

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_notices)
    
    def parse_tender(self, response):
        self.logger.info('---------Scrapping Notices from Notices Page---------')

        for row in response.css('table tbody tr'):
            tenderitems = CitnewsItem()
            tenderTitle = row.css('td a::text').get()
            tenderUrl = row.css('td a::attr(href)').get()

            if tenderTitle and tenderUrl:
                tenderitems['tenderTitle'] = tenderTitle.strip()
                tenderitems['tenderUrl'] = response.urljoin(tenderUrl)
                yield tenderitems

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_notices)
