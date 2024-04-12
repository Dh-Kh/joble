import scrapy
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from ..items import JoobleScrapingItem
from random import randint


class ScrapingSpider(scrapy.Spider):
    name = "scraping_spider"
    allowed_domains = ["realtylink.org"]
    
    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
        'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]
    
    def start_requests(self):
        url = "https://realtylink.org/en/properties~for-rent"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            headers={
                "User-Agent": self.user_agent_list[randint(0, len(self.user_agent_list)-1)]
            }
        )
    
    def parse(self, response):
        item = JoobleScrapingItem()
        driver = response.request.meta["driver"]
        wait = WebDriverWait(driver, 3)
        action = ActionChains(driver)
        #for _ in range(5):
        #range for urls with pagination made separently
        urls = response.xpath('//div[@class="thumbnail property-thumbnail-feature legacy-reset"]//a[@class="property-thumbnail-summary-link"]/@href').getall()
        for i in range(len(urls)):
            item["url"] = urls[i]
            url_to_get = "https://realtylink.org"+urls[i]
            driver.get(url_to_get)
            title = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//div[@class="col text-left pl-0"]//h1/span[@data-id="PageTitle"]'
            )))
            item["title"] = title.text
            location_data = wait.until(EC.visibility_of_element_located((
                By.XPATH, '//div[@class="col text-left pl-0"]//div[@class="d-flex mt-1"]/h2[@itemprop="address"]'
            )))
            location_data_text = location_data.text.split(", ")
            item["region"] = location_data_text[1]
            item["address"] = location_data_text[0]
            try:
                description = wait.until(EC.presence_of_element_located((
                    By.XPATH, '//div[@class="property-description col-md-12"]/div[@itemprop="description"]'
                )))
                item["description"] = description.text
            except TimeoutException:
                item["description"] = "No description"
            #try:
            #    button_img = driver.find_element(By.XPATH, '//div[class="photo-buttons legacy-reset"]/button[@class="btn btn-primary photo-btn"]')
            #    imgs_amount = button_img.text
            #    action.move_to_element(button_img).click()
            #    first_selected_img = driver.find_element(By.XPATH, '//li[@class="selected"]/img')
            #    item["images"] = " ".join(first_selected_img.get_attribute("src"))
            #    images = driver.find_elements(By.XPATH, '//li[@style="margin-right: 3px; width: 104px;"]/img/')
            #    for y in range(imgs_amount-1):
            #        item["images"] = " ".join(images[y].get_attribute("src"))
            #    exit_click = driver.find_element(By.XPATH, '//div[@class="close icon-close"]')
            #    action.move_to_element(exit_click).click()
            #except NoSuchElementException:
            #    empty_img = driver.find_element(By.XPATH, '//img[@class="noPointer"]')
            #    item["images"] = empty_img.get_attribute("src")
            #yield item
            
       
        #prices = response.xpath("//div[@class='price']//span/text()").getall()
        #for i in range(len(urls)):
            #dates = response.xpath("//table[@class='table table-striped']//tbody/tr/td[1]/text()").get()
            #if len(dates) < 1:
            #    item["date"] = "No data"
            #else:
            #    item["date"] = dates
            #item["price"] = prices[i]
            #count_rooms = response.xpath("//div[@class='col-lg-3 col-sm-6 cac']").getall()
            #item["count_rooms"] = len(count_rooms)
            #area_estate = response.xpath("//div[@class='carac-value']//span/text()").get()
            #if len(area_estate) < 1:
            #    item["area_estate"] = "No data"
            #else:    
            #    item["area_estate"] = area_estate
            
            #next_element = driver.find_element(By.XPATH, "//li[@class='next']")
            #driver.execute_script("arguments[0].click();", next_element)
            
            