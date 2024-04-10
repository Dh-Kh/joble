import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ScrapingSpider(scrapy.Spider):
    name = "scraping_spider"
    allowed_domains = ["realtylink.org"]
    
    def start_requests(self):
        url = "https://realtylink.org/en/properties~for-rent"
        yield SeleniumRequest(
            url=url,
            callback=self.parse
        )
    
    def parse(self, response):
        pass