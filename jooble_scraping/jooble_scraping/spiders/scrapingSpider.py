import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, NoSuchElementException)
from ..items import JoobleScrapingItem
from random import randint
from selenium.webdriver.common.keys import Keys
from time import sleep


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
        #urls = []
#        driver.get("https://realtylink.org/en/properties~for-rent?view=Thumbnail")
#        for _ in range(5):
#            innner_urls = wait.until(EC.presence_of_all_elements_located((
#                By.XPATH, '//div[@class="thumbnail property-thumbnail-feature legacy-reset"]//a[@class="property-thumbnail-summary-link"]'
#            )))
#            for x in range(len(innner_urls)):
#                urls.append(innner_urls[x].get_attribute("href"))
#            next_element = driver.find_element(By.XPATH, "//li[@class='next']")
#            next_element.click()
#            wait.until(EC.staleness_of(innner_urls[0]))
            
        urls = response.xpath('//div[@class="thumbnail property-thumbnail-feature legacy-reset"]//a[@class="property-thumbnail-summary-link"]/@href').getall()
        for i in range(len(urls)):
            if i == 1:
                break
            item["url"] = urls[i]
            url_to_get = "https://realtylink.org"+urls[i]
            driver.get(url_to_get)
            driver.maximize_window()
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
                
            try:
                stack = []
                button_img = driver.find_element(By.XPATH, '//div[@class="primary-photo-container"]')
                action.move_to_element(button_img).click().perform()
                images = wait.until(EC.presence_of_all_elements_located((
                    By.XPATH, '//li[@style="margin-right: 3px; width: 104px;"]/img'
                )))
                for y in range(1, len(images)):
                    action.move_to_element(images[y]).click().perform()
                    driver.implicitly_wait(3)
                    stack.append(images[y].get_attribute('src'))
                    #action.send_keys(Keys.END)
                item["images"] = stack
                exit_click = driver.find_element(By.XPATH, '//div[@class="close icon-close"]')
                action.move_to_element(exit_click).click().perform()
            except NoSuchElementException:
                empty_img = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '//img[@class="noPointer"]'
                    )))
                item["images"] = [empty_img.get_attribute("src")]
            try:
                dates = wait.until(EC.visibility_of_all_elements_located((
                    By.XPATH, '//table[@class="table table-striped"]//tbody/tr/td[1]'
                )))
                stack_date = [date.text for date in dates]
                item["date"] = stack_date
            except TimeoutException:
                item["date"] = "No data"
            price = wait.until(EC.presence_of_element_located((
                By.XPATH, '//div[@class="price-container"]//div[@class="price text-right"]/meta[@itemprop="price"]'
            )))
            item["price"] = price.get_attribute("content")
            #count rooms isn't working properly!
            count_rooms = wait.until(EC.visibility_of_all_elements_located((
                By.XPATH, '//div[starts-with(@class, "col-lg-3 col-sm-6")]'
            )))
            item["count_rooms"] = sum(int(char) for room in count_rooms for char in room.text if char.isdigit())
            try:
                area_estate = wait.until(EC.visibility_of_element_located((
                    By.XPATH, '//div[@class="carac-value"]/span'
                )))
                item["area_estate"] = area_estate.text
            except TimeoutException:
                item["area_estate"] = "No data"
            yield item
            
            
            
            