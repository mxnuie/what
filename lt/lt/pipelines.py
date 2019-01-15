# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from lt.items import LtItem, PriceItem


class LtPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='118.31.73.184',
                                    port=3306,
                                    user='root',
                                    password='cscs123456',
                                    db='lt',
                                    charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, LtItem):
            self.cursor.execute(
                'INSERT INTO prdno_form VALUES (%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE prdNo = %s, classification = %s, brand = %s, name = %s, time = %s;',
                (item['prdNo'], item['classification'], item['brand'], item['name'], item['time'], item['prdNo'],
                 item['classification'], item['brand'], item['name'], item['time']))
            self.conn.commit()
            return item
        elif isinstance(item, PriceItem):
            self.cursor.execute(
                'INSERT INTO ref_price_form(`prdNo`, `prdOptNo`, `REF`, `prdChocOptNm`, `saleUntPrc`, `saleUntPrcGlbl`, `soyn`, `url`, `time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE prdNo = %s,prdOptNo = %s,REF = %s,prdChocOptNm = %s,saleUntPrc = %s,saleUntPrcGlbl = %s,soyn = %s,url = %s, time = %s;',
                (item['prdNo'], item['prdOptNo'], item['REF'], item['prdChocOptNm'], item['saleUntPrc'],
                 item['saleUntPrcGlbl'], item['soyn'], item['url'],item['time'], item['prdNo'], item['prdOptNo'], item['REF'],
                 item['prdChocOptNm'], item['saleUntPrc'], item['saleUntPrcGlbl'], item['soyn'], item['url'],item['time']))
            self.conn.commit()
            return item
        # elif isinstance(item, LabelItem):
        #     self.cursor.execute(
        #         'INSERT INTO label_text_from(`prdNo`, `label`, `text`) VALUES (%s,%s,%s) ON DUPLICATE KEY UPDATE prdNo = %s, label = %s, text = %s;',
        #         (item['prdNo'], item['label'], item['text'], item['prdNo'], item['label'], item['text'])
        #     )
        #     return item
