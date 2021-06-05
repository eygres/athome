import scrapy
import pandas as pd
from ..items import AthomeItem


class AthomeDirSpider(scrapy.Spider):
    name = 'athome-dir'
    allowed_domains = ['athome.lu']
    
    # url filter
    start_urls = ['https://www.athome.lu/en/srp/?tr=rent&bedrooms_max=1&price_min=800&price_max=1200&q=faee1a4a&loc=L2-luxembourg&ptypes=flat,4,7,5,6,42,32,41']

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
            yield scrapy.Request(next_page, callback=self.parse)