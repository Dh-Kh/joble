import scrapy

class ScrapingSpider(scrapy.Spider):
    name = "scraping_spider"
    start_urls = ["https://realtylink.org/en/properties~for-rent"]
    def parse(self, response):
        pass