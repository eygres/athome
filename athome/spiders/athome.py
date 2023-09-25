import scrapy
from ..items import AthomeItem
from random import randrange
from time import sleep
from scrapy.exceptions import UsageError
from pathlib import Path
import yaml

class AthomeDirSpider(scrapy.Spider):
    name = 'athome'
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
        
    def start_requests(self):
        if hasattr(self, "filter"):
            yaml_config_path = (Path(__file__).parent / f'../../config/{self.name}.yaml').resolve()
            with open(yaml_config_path) as file:
                spider_config = yaml.safe_load(file)
            
            if self.filter in spider_config['filters']:
                self.start_url = spider_config['filters'][self.filter]
            else:
                raise UsageError(f'Filter name {self.filter} is not found in config file.')    
        else:
            # log something here
            raise UsageError(f'Syntax: scrapy crawl {self.name} -a filter="<...>"')
            
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
            sleep(randrange(10)) # be nice to the web site
            yield scrapy.Request(next_page, callback=self.parse, headers = self.request_header)