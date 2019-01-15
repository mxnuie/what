# -*- coding:utf-8 -*-
from requests_html import HTMLSession
import pymysql

session = HTMLSession()

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='cscs123456',
                       db='lt',
                       charset='utf8')
cursor = conn.cursor()

sql = "SELECT prdNo,max(prdOptNo) FROM `ref_price_form` GROUP BY prdNo"

cursor.execute(sql)
results = cursor.fetchall()


def get_url():
    for i in results:
        prdNo = i[0]
        print(prdNo)
        prdOptNo = i[1]
        url = 'http://chn.lottedfs.com/kr/product/productDetailBtmInfoAjax?prdNo=%s&prdOptNo=%s&previewYn=' % (
        prdNo, prdOptNo)
        yield url,prdNo



url = get_url()

for xx in url:
    r = session.get(xx[0], headers={
        'Referer': 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=10002353433&dispShopNo1=1200050&dispShopNo2=1200051&dispShopNo3=1200058',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    })

    a = r.html.xpath('//div[@class="tableBox"]')[0].search_all('<th scope="row">{}</th>')
    b = r.html.xpath("//div[@class='tableBox']/table/tbody/tr/td | (td/div)")

    for i1, i2 in zip(a, b):
        print(i1[0])
        print(i2.text)
        print('>>>>>>>>>>>>>>>')
