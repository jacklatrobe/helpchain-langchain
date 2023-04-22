from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from telstra import TelstraSupportSpider
 
 
process = CrawlerProcess(get_project_settings())
process.crawl(TelstraSupportSpider)
process.start()