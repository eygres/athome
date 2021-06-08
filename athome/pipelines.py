# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
from scrapy.exporters import CsvItemExporter
from scrapy.exceptions import DropItem
from datetime import datetime
import re
import logging
from pathlib import Path

class AthomePipeline:

    def __init__(self):
        self.df = pd.DataFrame(columns=['href','price', 'm2', 'price_m2', 'place', 'title', 'timestamp', 'status'])
    
    def process_item(self, item, spider):
        if (self.df['href'] == item['href']).any():
            raise DropItem(f"{spider.name} duplicate {item['href']}")
        else:
            time_stamp = datetime.now()       
            item['timestamp'] = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
            item['price'] = re.sub(r'''[^0-9]''', '', item['price'])
            item['m2'] = re.sub(r'''[^0-9\.]''', '', item['m2'])
            if(float(item['m2']) > 0):
                item['price_m2'] = float(item['price']) / float(item['m2'])
            else:
                item['price_m2'] = ''
            item['place'] = re.findall('\s([A-Z][A-zÀ-ÿ-\(\)\s]+)$', item['title'])
            item['status'] = "N"
            self.new_count += 1
            logging.log(logging.INFO, f"{spider.name} new: {item['href']}")
            self.exporter.export_item(item)
        return item

    def open_spider(self, spider):
        self.new_count = 0
        out_file_path = (Path(__file__).parent / f'../output/{spider.name}.csv').resolve()
        logging.log(logging.INFO, f'Output path: {out_file_path}')
            
        try:
            header = False
            self.df = pd.read_csv(out_file_path)
            self.df['status'] = 'S'
            self.df.to_csv(out_file_path, index = False)
        except IOError as e:
            logging.log(logging.INFO, f'Creating {out_file_path}')
            header = True
        except pd.errors.EmptyDataError:
            logging.log(logging.WARNING, "The output file is empty.")        
            header = True 
          
        self.file = open(out_file_path, 'ab')
        self.exporter = CsvItemExporter(self.file, include_headers_line = header)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        logging.log(logging.INFO, f'{spider.name} new ads: {self.new_count}')
        del self.df

