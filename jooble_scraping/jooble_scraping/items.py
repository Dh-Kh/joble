# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class JoobleScrapingItem(Item):
    url = Field()
    title = Field()
    region = Field()
    address = Field()
    description = Field()
    images = Field()
    #date = Field()
    #price = Field()
    #count_rooms = Field()
    #area_estate = Field()
