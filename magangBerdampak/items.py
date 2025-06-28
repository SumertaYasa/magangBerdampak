# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MagangberdampakItem(scrapy.Item):
    title = scrapy.Field()
    field = scrapy.Field()
    placement_location = scrapy.Field()
    company_location = scrapy.Field()
    description_company = scrapy.Field()
    description_job = scrapy.Field()
    assigments_details = scrapy.Field()
    criteria = scrapy.Field()
    learning_outcomes = scrapy.Field()
