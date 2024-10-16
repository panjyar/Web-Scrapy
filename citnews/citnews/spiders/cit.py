import scrapy
import datetime
from datetime import datetime
from ..items import CitnewsItem
from ..items import IITGnewsItem
from ..items import NITSItems
class CitSpider(scrapy.Spider):
    name = "cit"
    allowed_domains = ["cit.ac.in" , "iitg.ac.in" , "nits.ac.in"]
    start_urls = ["https://cit.ac.in" , "https://iitg.ac.in" , "http://www.nits.ac.in/"]


    def parse(self, response):
        # Uncomment and adjust if you want to scrape the CIT website
        if "cit.ac.in" in response.url:
            self.logger.info('------------------------SCRAPPING CIT WEBSITE-----------------------------')
            yield from self.parse_cit(response)

        elif "iitg.ac.in" in response.url:
            self.logger.info('--------------------------------SCRAPPING IITG WEBSITE-------------------------------------------')
            yield from self.parse_iitg(response)

        elif "nits.ac.in" in response.url:
            self.logger.info('------------------------------SCRAPPING NITS WEBSITE---------------------------------')
            yield from self.parse_nits(response)
    
    def parse_nits(self, response):
        self.logger.info('-------------------------------------------  SCRAPPING LATEST NEWS OF NITS----------------------------------------------------')
        
       
        for news_item in response.css('marquee a'):
            latestNewsitems = NITSItems()
            
            latestNews = news_item.css('::text').get()
            latestNewsUrl = news_item.css('::attr(href)').get()  

            latestNewsitems['latestNews'] = latestNews.strip() if latestNews else None
            latestNewsitems['latestNewsUrl'] = response.urljoin(latestNewsUrl) if latestNewsUrl else None

            yield latestNewsitems

        self.logger.info('---------Scrapping Latest News of NITS ---------')
        for news_item in response.css('div.newsupdatesmargin b'):
            latestNewsitems = NITSItems()
            latestNewstitlenits = news_item.css('a::text').get()
            latestNewsurlnits = news_item.css('a::attr(href)').get()

            latestNewsitems['latestNewstitlenits'] = latestNewstitlenits.strip() if latestNewstitlenits else None
            latestNewsitems['latestNewsurlnits'] = response.urljoin(latestNewsurlnits)
            yield latestNewsitems 
        if response.url != 'http://www.nits.ac.in/newsupdates.php':
                yield response.follow('http://www.nits.ac.in/newsupdates.php', self.newsUpdatesnits)
    
    def newsUpdatesnits(self, response):
        self.logger.info('----------------Scrapping Latest News of NITS (All Page)--------------- ')
        for news_item in response.css('div.panel-border  b a'):
            latestNewsitems = NITSItems()
            latestNewstitlenits = news_item.css('::text').get()
            latestNewsurlnits = news_item.css('::attr(href)').get()

            latestNewsitems['latestNewstitlenits'] = latestNewstitlenits.strip() if latestNewstitlenits else None
            latestNewsitems['latestNewsurlnits'] = response.urljoin(latestNewsurlnits)
            yield latestNewsitems
        
        self.logger.info('----------------Scrapping Notice--------------- ')
    
        for notice in response.css('div#tab1 a'):
            latestNewsitems = NITSItems()
            latestNewstitlenits = news_item.css('a::text').get()
            latestNewsurlnits = news_item.css('a::attr(href)').get()

            latestNewsitems['latestNewstitlenits'] = latestNewstitlenits.strip() if latestNewstitlenits else None
            latestNewsitems['latestNewsurlnits'] = response.urljoin(latestNewsurlnits)
            yield latestNewsitems

        
        if response.url != 'http://www.nits.ac.in/newsupdates.php':
            yield response.follow('http://www.nits.ac.in/newsupdates.php', self.newsUpdatesnits)

    def parse_iitg(self, response):
        self.logger.info('---------Scrapping Latest News of IITG ---------')
        for news_item in response.css('div#bn7 a'):
            latestNewsitems = IITGnewsItem()
            latestNewstitle = news_item.css('::text').get()
            latestNewsurl = news_item.css('::attr(href)').get()

            latestNewsitems['latestNewstitle'] = latestNewstitle.strip() if latestNewstitle else None
            latestNewsitems['latestNewsurl'] = response.urljoin(latestNewsurl)
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
                    date_str = eventDate.strip().replace('Date: ', '')
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

        if response.url != 'https://iitg.ac.in/iitg_events_all':
            yield response.follow('https://iitg.ac.in/iitg_events_all', self.parse_upcommingEventOfIITG)

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

        
        if response.url != 'https://www.cit.ac.in/pages-notices-all':
            yield response.follow('https://www.cit.ac.in/pages-notices-all', self.parse_notices)

        self.logger.info('----------------Scrapping Tender--------------- ')
        for tender in response.css('div#tab1 a'):
            tenderitems = CitnewsItem()
            tenderTitle = tender.css('::text').get()
            tenderUrl = tender.css('::attr(href)').get()

            tenderitems['tenderTitle'] = tenderTitle.strip() if tenderTitle else None
            tenderitems['tenderUrl'] = response.urljoin(tenderUrl)
            yield tenderitems
        if response.url != 'https://www.cit.ac.in/pages-tenders-all':
            yield response.follow('https://www.cit.ac.in/pages-tenders-all', self.parse_tender)
        
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
