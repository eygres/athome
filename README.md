# Web crawler for ATHome and Immotop

* Scrapes Luxembourg athome and immotop rental ads into csv file (in the ./output subdirectory).
* New ads are added to the end of the file
* Tested with Python 3.8 and Scrapy 2.4.1
* Command line: 
  * ATHome.lu: ```scrapy crawl athome -a filter=<filter_name>```, `filter_name' refers to the name of the search URL in the config yaml file.
      * Example: ```scrapy crawl athome -a filter=2bed-lux-central-terrace```
  * Immotop: ```scrapy crawl immotop```
* Named filters are configured in the ./config folder (one yaml file per spider). 
* The output CSV goes to ./output folder.