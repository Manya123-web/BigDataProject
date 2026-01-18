# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FacultyFinderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    address = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()
    education = scrapy.Field()
    biography = scrapy.Field()
    specializations = scrapy.Field()
    teaching = scrapy.Field()
    publications = scrapy.Field()
    research = scrapy.Field()
    website_links = scrapy.Field()    
    pass
