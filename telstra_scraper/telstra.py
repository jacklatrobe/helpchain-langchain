## POC to demonstrate ability to scan existing search tool on a public company website
import requests
import json
import scrapy

class SearchSpider(scrapy.Spider):
    name = 'support-spider'
    start_urls = ['https://www.telstra.com.au/support/search?query=telstra%20prepaid&area=personal']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        RESULT_FILTER = '.tcom-lego-search-page__list__content'
        HEADING_FILTER = 'h3::text'
        BODY_FILTER = 'p::text'
        URL_FILTER = 'a::attr("href")'
        
        for quote in response.css(RESULT_FILTER):
            yield {
                'heading': quote.css(HEADING_FILTER).extract_first(),
                'body': quote.css(BODY_FILTER).extract_first(),
                'url': quote.css(URL_FILTER).extract_first(),
            }
