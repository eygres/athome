# Web crawler for ATHome and Immotop

* Scrapes Luxembourg athome and immotop rental ads into csv file (in the ./output subdirectory).
* New ads are added to the end of the file
* Tested with Python 3.8 and Scrapy 2.4.1
* Command line: 
  * ATHome.lu: ```scrapy crawl athome-dir```
  * Immotop: ```scrapy crawl immotop```

* Before starting change the URL in respective spider's directory to the one you need -> start_url = "search url from a browser"
