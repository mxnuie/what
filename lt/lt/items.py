# -*- coding: utf-8 -*-
# Define here the models for your scraped items
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join



class LtItem(scrapy.Item):
    prdNo = scrapy.Field()
    brand = scrapy.Field()
    name = scrapy.Field()
    classification = scrapy.Field()
    time = scrapy.Field()


class PriceItem(scrapy.Item):
    prdNo = scrapy.Field()
    prdOptNo = scrapy.Field()
    REF = scrapy.Field()
    prdChocOptNm = scrapy.Field()
    saleUntPrc = scrapy.Field()
    saleUntPrcGlbl = scrapy.Field()
    soyn = scrapy.Field()
    url = scrapy.Field()
    time = scrapy.Field()


# class LabelItem(scrapy.Item):
#     prdNo = scrapy.Field()
#     label = scrapy.Field()
#     text = scrapy.Field()

class LTSpiderLoader(ItemLoader):
    default_item_class = [LtItem,PriceItem]
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()