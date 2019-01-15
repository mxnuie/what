# -*- coding:utf-8 -*-
from scrapy_redis.spiders import RedisSpider
# import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
import random
from lt.items import LtItem, PriceItem
import json
from lxml import etree
import datetime
import re
import urllib.request

class ltSpider(RedisSpider):  # scrapy.Spider
    name = 'lt'
    '''
        start_requests函数：
        1.用于构建每一商品类别URL的第一页
    '''

    def start_requests(self):
        classification = ['BB/CC霜', '妆前乳/隔离霜', '蜜粉', '遮瑕膏', '两用粉饼/粉饼', '气垫粉', '粉底液', '阴影/腮红/高光',
                          '眉笔', '眼影', '眼线', '睫毛膏', '口红', '唇彩', '润唇膏', '染唇液', '唇膏笔/唇线笔', '底妆套装', '眼妆套装',  # 19
                          '唇妆套装', '综合彩盘', '指甲油', '护甲油', '洗甲水', '美甲工具', '美甲套装', '粉扑/海绵', '化妆刷', '睫毛夹',  # 29
                          '化妆棉/吸油纸', '镜子', '削笔刀/镊子', '口红盒/眼影盒', '蜜粉盒/粉底盒', '化妆品空盒', '化妆包']  # 共36个
        disp_shop_no = 1200052
        for i in range(36):
            url = "http://chn.lottedfs.com/kr/display/GetPrdList?viewType01=0&lodfsAdltYn=N&catNo=" + str(
                disp_shop_no) + "&catNm=" + classification[i] + "&dispShopNo=" + str(
                disp_shop_no) + "&sortStdCd=01&brndNoList=&prcRngCd=&genList=&fvrList=&prdAttrCdList=&soExclList=&svmnUseRtRngList=&etcFilterList=&cntPerPage=60"

            yield Request(url, meta={'classification': classification[i], 'dispShopNo': str(disp_shop_no)},
                          callback=self.parse)
            disp_shop_no += 1

    '''
        parse函数：
        1.完善每一商品类别URL，加上了后续的页数
    '''

    def parse(self, response):
        page = response.xpath("//div[@class='pagingArea pt15']/div[@class='paging pt15']/a")[-1].re(
            '(?<=javascript:fn_movePage\().*?(?=\))')[0]
        page = int(page) + 1
        for i1 in range(1, page):
            url = "http://chn.lottedfs.com/kr/display/GetPrdList?viewType01=0&lodfsAdltYn=N&catNo=" + response.meta[
                'dispShopNo'] + "&catNm=" + response.meta['classification'] + "&dispShopNo=" + response.meta[
                      'dispShopNo'] + "&sortStdCd=01&brndNoList=&prcRngCd=&genList=&fvrList=&prdAttrCdList=&soExclList=&svmnUseRtRngList=&etcFilterList=&cntPerPage=60&curPageNo=" + str(
                i1) + "&treDpth=3"
            yield Request(url, meta={'classification': response.meta['classification']},
                                 callback=self.get_product_first_prdNo)

    '''
        get_product_first_prdNo函数：
        1.用于构造每件商品的URL
        2.将每一页的类别URL中出现的商品的ID，品牌，名称存入数据库                    
    '''

    def get_product_first_prdNo(self, response):
        prdNo = response.xpath(
            "//div[@class='imgType']/ul[@class='listUl']/li[@class='productMd' or @class='productMd soldOut']/a[@class='link gaEvtTg js-contextmenu']").re(
            '(?<=href="javascript:ga_adltCheckPrdDtlMove\().*?(?=,)')
        brand = response.xpath("//div[@class='brand']/strong/text()").extract()[0:60]
        product = response.xpath("//div[@class='product']/text()").extract()[0:60]
        item = LtItem()

        cookies = [
            '', '1127880195321195202732119',
            '1636588328379128490337912', '1637439131181785725918178',
            '1775940129184604226118460', '2563488628388978033438897',
            '2858660398303480781230348', '3150660123358345909358345',
            '3307398707248380576248380', '3525182655155972747315597',
            '586361035993190861993190', '752329658338791571338791',
        ]

        for i1, i2, i3 in zip(prdNo, brand, product):
            pN = i1.replace('\r', '').replace('\n', '').replace('\t', '')
            item['prdNo'] = pN
            item['classification'] = response.meta['classification']
            item['brand'] = i2.replace('\r', '').replace('\n', '').replace('\t', '')
            item['name'] = i3
            item['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            yield item
            url = 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=' + pN

            # if xxx % 15 == 0:
            #     m = n % 12
            #     n += 1
            # print('第' + str(xxx) + '个')
            # xxx += 1
            cookie = random.choice(cookies)

            yield Request(url, cookies={'__z_a': cookie}, meta={'qwe': cookie}, callback=self.get_soYn_url)

    def get_soYn_url(self, response):
        item = PriceItem()
        # a = response.re('var prd = {}};')
        a = response.xpath('//html').re('(?<=var prd = ).*?(?=};)')
        j = a[0] + '}'
        pytext = json.loads(j)
        list = pytext['prdChocOpt']['prdChocOpt1List']
        # num = pytext['prdChocOpt']['prdChocOpt1List']

        cookies = [
            '', '1127880195321195202732119',
            '1636588328379128490337912', '1637439131181785725918178',
            '1775940129184604226118460', '2563488628388978033438897',
            '2858660398303480781230348', '3150660123358345909358345',
            '3307398707248380576248380', '3525182655155972747315597',
            '586361035993190861993190', '752329658338791571338791',
        ]
        prdNoList = []
        prdOptNoList = []

        if len(list) == 1:
            for i in list:
                url = 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=%s&prdOptNo=%s' % (
                    i['prdNo'], i['prdOptNo'])
                item['prdNo'] = i['prdNo']
                item['prdOptNo'] = i['prdOptNo']
                item['REF'] = pytext['erpRefNo']
                item['prdChocOptNm'] = i['prdChocOptNm']
                item['saleUntPrc'] = pytext['saleUntPrc']
                item['saleUntPrcGlbl'] = pytext['saleUntPrcGlbl']
                item['soyn'] = i['soYn']
                item['url'] = url
                item['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                yield item
                # prdNo = i['prdNo']
                # prdOptNo = i['prdOptNo']
                # uurl = 'http://chn.lottedfs.com/kr/product/productDetailBtmInfoAjax?prdNo=%s&prdOptNo=%s&previewYn=' % (prdNo, prdOptNo)
                # yield scrapy.Request(uurl, headers={
                #     'Referer': 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=10002353433&dispShopNo1=1200050&dispShopNo2=1200051&dispShopNo3=1200058'},
                #                      meta={'prdNo': prdNo}, callback=self.get_label_text)
        else:
            for i in list:
                url = 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=%s&prdOptNo=%s' % (
                    i['prdNo'], i['prdOptNo'])
                prdNoList.append(i['prdNo'])
                prdOptNoList.append(i['prdOptNo'])
                cookie = random.choice(cookies)
                yield Request(url, cookies={'__z_a': cookie},
                                     meta={'prdNo': i['prdNo'], 'prdOptNo': i['prdOptNo'],
                                           'prdChocOptNm': i['prdChocOptNm'], 'soyn': i['soYn'], 'url': url},
                                     callback=self.get_REF_price)
            # prdNo = random.choice(prdNoList)
            # prdOptNo = random.choice(prdOptNoList)
            # uurl = 'http://chn.lottedfs.com/kr/product/productDetailBtmInfoAjax?prdNo=%s&prdOptNo=%s&previewYn=' % (prdNo, prdOptNo)
            # yield scrapy.Request(uurl, headers={
            #     'Referer': 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=10002353433&dispShopNo1=1200050&dispShopNo2=1200051&dispShopNo3=1200058'},
            #                      meta={'prdNo': prdNo}, callback=self.get_label_text)

    def get_REF_price(self, response):
        item = PriceItem()
        a = response.xpath('//html').re('(?<=var prd = ).*?(?=};)')
        j = a[0] + '}'
        pytext = json.loads(j)
        item['prdNo'] = response.meta['prdNo']
        item['prdOptNo'] = response.meta['prdOptNo']
        item['REF'] = pytext['erpRefNo']
        item['prdChocOptNm'] = response.meta['prdChocOptNm']
        item['saleUntPrc'] = pytext['saleUntPrc']
        item['saleUntPrcGlbl'] = pytext['saleUntPrcGlbl']
        item['soyn'] = response.meta['soyn']
        item['url'] = response.meta['url']
        item['time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        yield item

    # def get_label_text(self, response):
    #     item = LabelItem()
    #     print(response)
    #
    #     ResponseProduct = etree.HTML(response.text)
    #
    #     label = response.xpath('//div[@class="tableBox"]').re('(?<=<th scope="row">).*?(?=</th>)')
    #     print(label)
    #     text = ResponseProduct.xpath("//div[@class='tableBox']/table/tbody/tr/td | (td/div)")
    #     print(len(text))
    #     for a,b in zip(label,text):
    #         print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    #         item['prdNo'] = response.meta['prdNo']
    #         item['label'] = a
    #         item['text'] = b.text.replace('\r', '').replace('\n', '').replace('\t', '')
    #         yield item
