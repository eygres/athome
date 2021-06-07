import scrapy
from ..items import AthomeItem
from random import randrange
from time import sleep

class AthomeDirSpider(scrapy.Spider):
    name = 'athome-dir'
    allowed_domains = ['athome.lu']
    
    request_header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Content-Type": "application/x-www-form-urlencoded",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-GPC": "1"
             }
    
    # url filter
    start_url = 'https://www.athome.lu/en/srp/?tr=rent&bedrooms_max=1&price_min=800&price_max=1200&q=faee1a4a&loc=L2-luxembourg&ptypes=flat,4,7,5,6,42,32,41'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse, headers=self.request_header) #, meta={"proxy": "http://192.168.44.137:8080"})
        
    def parse(self, response):
        item = AthomeItem()
         
        for appart in response.xpath('/html/body/div[1]/div/div/section/div[1]/div/div/article/div'): #/h3/a
            item['href'] = response.urljoin(appart.css('a::attr(href)').get())
            item['title'] = appart.css('a::attr(title)').get()
            item['price'] = appart.xpath('ul[1]/li/span/text()').get()
            item['m2'] = appart.xpath('ul[2]/li/text()').get()

    # /html/body/div[1]/div/div/section/div[1]/div/div[25]/article/div/ul[1]/li/span        
    #        self.log(item)
            yield item
            
        next_page = response.css('a.nextPage::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            sleep(randrange(5))
            yield scrapy.Request(next_page, callback=self.parse, headers = self.request_header)