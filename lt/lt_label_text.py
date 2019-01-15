# -*- coding:utf-8 -*-
from requests_html import HTMLSession
import pymysql
import time

session = HTMLSession()

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='cscs123456',
                       db='lt',
                       charset='utf8')
cursor = conn.cursor()

sql = "SELECT ref_price_form.prdNo,MAX(ref_price_form.prdOptNo) FROM ref_price_form WHERE prdNo IN (SELECT ss.prdNo FROM (SELECT a.prdNo,b.prdNo AS BP FROM `prdno_form` a LEFT JOIN `label_text_from` b ON a.prdNo = b.prdNo) ss WHERE ss.BP IS NULL) GROUP BY prdNo ;"

cursor.execute(sql)
results = cursor.fetchall()

print(results)


def get_url():
    for i in results:
        prdNo = i[0]
        prdOptNo = i[1]
        url = 'http://chn.lottedfs.com/kr/product/productDetailBtmInfoAjax?prdNo=%s&prdOptNo=%s&previewYn=' % (
            prdNo, prdOptNo)
        yield url, prdNo


url = get_url()

for xx in url:
    try:
        print(xx[0])
        time.sleep(1.75)
        r = session.get(xx[0], headers={
            'Host': 'chn.lottedfs.com',
            'Connection': 'keep-alive',
            'Accept': 'text/html, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Referer': 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=20000388137',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-HK,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh-TW;q=0.5',
            'Cookie': 'language=zh; lang_pc=ZH; cntry_pc=KR; cntry_gate=OT; lang_gate=ZH; lang=ZH; cntry=KR; dprt.KR=D01; crc=CNY; _ga=GA1.2.677836714.1542620278; RB_PCID=1542620277537167247; _atrk_siteuid=6OZ8X6oCDohzBih7; _ga=GA1.3.677836714.1542620278; RB_GUID=c63b632e-abfc-4081-9ec0-71e7075460b4; dimension={"dimension1":"PC Web","dimension2":"%EC%A4%91%EB%AC%B8_%ED%95%9C%EA%B5%AD","dimension3":"U","dimension4":"U","dimension5":"U","dimension6":"U","dimension7":"U","dimension8":"N","dimension9":"U","dimension10":"","dimension11":""}; __zjc9064=4858149652; JSESSIONID=11f19724-9d78-4d00-8d8d-8bf3b28c2166; _gid=GA1.2.341179984.1546397065; appier_tp=; appier_utmz=%7B%7D; _atrk_ssid=yHBijYUK29L37Yq5M8mphD; _atrk_sessidx=2; _dc_gtm_UA-84350687-2=1; _dc_gtm_UA-84350687-3=1; _gat_UA-84350687-3=1; _gat_UA-84350687-2=1; __ZEHIC7012=1546397063; __z_a=4060536518383495316738349; lodfsAdltYn=null; RB_SSID=DSdx8FNrmi; ldfsRecentPrd=20000388137%7C6042903130%7C10002353433%7C8081438199%7C6081805771%7C10002137947%7C10000022128%7C10002278636%7C10001913162'
        })

        a = r.html.xpath('//div[@class="tableBox"]')[0].search_all('<th scope="row">{}</th>')
        b = r.html.xpath("//div[@class='tableBox']/table/tbody/tr/td | (td/div)")
        print(a)
        print(b)

        for i1, i2 in zip(a, b):
            try:
                print(i1[0])
                print(i2.text)
                print('>>>>>>>>>>>>>>>')
                print(
                    "INSERT INTO label_text_from(`prdNo`, `label`, `text`) VALUES ('%s','%s','%s') ON DUPLICATE KEY UPDATE prdNo = '%s', label = '%s', text = '%s';" % (
                    xx[1], i1[0], i2.text, xx[1], i1[0], i2.text,),
                    )
                cursor.execute(
                    "INSERT INTO label_text_from(`prdNo`, `label`, `text`) VALUES ('%s','%s','%s') ON DUPLICATE KEY UPDATE prdNo = '%s', label = '%s', text = '%s';" % (
                    xx[1], i1[0], i2.text, xx[1], i1[0], i2.text,),
                )
                conn.commit()
            except:
                print('出错了')
    except Exception as e:
        print(e)
