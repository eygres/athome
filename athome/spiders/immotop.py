import scrapy
import time
from unicodedata import normalize
from ..items import AthomeItem
from random import randrange
from time import sleep
import math

class ImmotopSpider(scrapy.Spider):
    name = 'immotop'
    allowed_domains = ['immotop.lu']
    start_urls = ['https://www.immotop.lu/']
    cur_page = 1
    
    request_header = {
        "Host": "www.immotop.lu",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-GB,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.immotop.lu",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://www.immotop.lu",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-GPC": "1",
        }
        
    def start_requests(self):
        # load home page to mimic human behavior
        url = 'https://www.immotop.lu/'
        
        # add debugging proxy if needed, meta={"proxy": "http://192.168.44.137:8080"}
        yield scrapy.Request(url=url, callback=self.parse, headers=self.request_header)
    
    def parse(self, response):

        params = {
            'f[days]':'',
            'f[geodata][0][c_label]':'Luxembourg',
            'f[geodata][0][country]':'luxembourg',
            'f[geodata][0][label]':'Country',
            'f[geodata][0][level]':'country',
            'f[geodata][0][name]':'Luxembourg',
            'f[hidden]':'',
            'f[is_new]':'',           
            'f[Kind_ID][]':['201','203','204','205','206','207','208'],
            'f[price][from]':'800',
            'f[price][to]':'1200',
            'f[radius_new]':'',
            'f[rooms][from]':'1 Rooms',           
            'f[smode]':'L',
            'f[sort_field]':'ts',
            'f[sort_type]':'desc',
            'f[surface][from]':'',
            'f[text_search]':'',
            'f[Type]': 'rent',
            'f[year_buid]':'',            
            'form':'main_search_form',
            'form':'simple_search',
            'sort_field': 'ts',           
            'sort_type': 'desc'           
            }
        # add debugging proxy if needed, meta={"proxy": "http://192.168.44.137:8080"}        
        yield scrapy.FormRequest('https://www.immotop.lu/en/search/', callback=self.parse2,
                                 method='POST', formdata=params, headers=self.request_header)
   
    def parse2(self, response):
        item = AthomeItem()
        
        #from scrapy.shell import inspect_response
        #inspect_response(response, self)
        
        total_items = int(response.css('h2').css('span::text').get())
        self.log(f"Total items={total_items}")
        
        total_pages = math.ceil(total_items/15) # 15 items per page (const?)
        self.log(f"Total pages={total_pages}")
        
        for appart in response.css('div.search-agency-item-information'): 
            item['href'] = appart.css('a::attr(href)').get()
            item['title'] = appart.css('a::text').get()
            item['price'] = appart.css('div.price').css('nobr::text').get()
            item['m2'] = appart.css('div[title="Surface"]').css('nobr::text').get()
            yield item
        
        self.request_header['Referer'] = response.url
        
        if(self.cur_page < total_pages):
            self.cur_page+=1
            next_page = f"https://www.immotop.lu/en/search/index{self.cur_page}.html"
            if next_page is not None:
                sleep(randrange(20)) # be nice to the web site
                # add debugging proxy if needed, meta={"proxy": "http://192.168.44.137:8080"}
                yield scrapy.Request(next_page, callback=self.parse2, headers = self.request_header)   
    