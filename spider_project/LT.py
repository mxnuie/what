from requests_html import HTMLSession, user_agent
import json
import pymysql
import random
import time

conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='cscs123456',
                       db='lt',
                       charset='utf8')
cursor = conn.cursor()

session = HTMLSession()
# user_agent = user_agent(style=None)
USER_AGENT_LIST = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1" \
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3", \
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3", \
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24", \
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"

]


def get_page(url):
    user_agent = random.choice(USER_AGENT_LIST)
    r = session.get(
        url,
        headers={'User-Agent': user_agent})
    a = r.html.xpath("div[@class='pagingArea pt15']/div[@class='paging pt15']/a")
    page = a[-1].search("javascript:fn_movePage({})")[0]
    return page


def start_url():
    classification = ['BB/CC霜', '妆前乳/隔离霜', '蜜粉', '遮瑕膏', '两用粉饼/粉饼', '气垫粉', '粉底液', '阴影/腮红/高光',
                      '眉笔', '眼影', '眼线', '睫毛膏', '口红', '唇彩', '润唇膏', '染唇液', '唇膏笔/唇线笔', '底妆套装', '眼妆套装',  # 19
                      '唇妆套装', '综合彩盘', '指甲油', '护甲油', '洗甲水', '美甲工具', '美甲套装', '粉扑/海绵', '化妆刷', '睫毛夹',  # 29
                      '化妆棉/吸油纸', '镜子', '削笔刀/镊子', '口红盒/眼影盒', '蜜粉盒/粉底盒', '化妆品空盒', '化妆包']  # 共36个
    disp_shop_no = 1200052
    # start_list = []
    for i in range(36):
        url = "http://chn.lottedfs.com/kr/display/GetPrdList?viewType01=0&catNo=" + classification[
            i] + "&dispShopNo=" + str(
            disp_shop_no) + "&sortStdCd=01&brndNoList=&prcRngCd=&genList=&fvrList=&prdAttrCdList=&soExclList=&etcFilterList=&cntPerPage=60&curPageNo=1&treDpth=3"
        # 调用get_page函数，来获取页数
        page = get_page(url)

        for i1 in range(1, int(page) + 1):
            url = 'http://chn.lottedfs.com/kr/display/GetPrdList?viewType01=0&catNo=' + classification[
                i] + '&dispShopNo=' + str(
                disp_shop_no) + '&sortStdCd=01&brndNoList=&prcRngCd=&genList=&fvrList=&prdAttrCdList=&soExclList=&etcFilterList=&cntPerPage=60&curPageNo=' + str(
                i1) + '&treDpth=3'
            # start_list.append(url)
            yield url
        disp_shop_no += 1


def get_product_first_prdNo(url):
    user_agent = random.choice(USER_AGENT_LIST)
    r = session.get(
        url,
        headers={'User-Agent': user_agent})
    b = r.html.xpath(
        "//div[@class='imgType']/ul[@class='listUl']/li[@class='productMd' or @class='productMd soldOut']/a[@class='link gaEvtTg js-contextmenu']")
    c = r.html.xpath(
        "//div[@class='imgType']/ul[@class='listUl']/li[@class='productMd']/a[@class='link gaEvtTg js-contextmenu']/div[@class='info']/div[@class='brand']")
    d = r.html.xpath(
        "//div[@class='imgType']/ul[@class='listUl']/li[@class='productMd']/a[@class='link gaEvtTg js-contextmenu']/div[@class='info']/div[@class='product']")
    for i1, i2, i3 in zip(b, c, d):
        prdNo = i1.search('href="javascript:ga_adltCheckPrdDtlMove({},')
        yield prdNo[0], i2.text, i3.text


def get_soYn_url(prdNo, cookie, user_agent):
    referer = [
        'http://chn.lottedfs.com/kr/display/category/third?dispShopNo1=1200050&dispShopNo2=1200060&dispShopNo3=1200061&treDpth=3',
        'http://chn.lottedfs.com/kr/display/category/third?dispShopNo1=1200050&dispShopNo2=1200051&dispShopNo3=1200054&treDpth=3']
    refer = random.choice(referer)
    print(user_agent)
    try:
        r = session.get(
            'http://chn.lottedfs.com/kr/product/productDetail?prdNo=' + prdNo,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                'Cookie': cookie,
            })

        a = r.html.search('var prd = {}};')
        j = a[0] + '}'
        pytext = json.loads(j)
        for i in pytext['prdChocOpt']['prdChocOpt1List']:
            # print(i['soYn'])
            # print(i['prdChocOptNm'])
            url = 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=%s&prdOptNo=%s' % (i['prdNo'], i['prdOptNo'])
            yield i['prdNo'], i['prdOptNo'], i['prdChocOptNm'], i['soYn'], url
    except BaseException as e:
        print('这个ID号是：', prdNo)
        print(r.status_code)
        print('>>>>>>>>>>>>>请求失败，停止10秒，记录到数据库<<<<<<<<<<<<<<')
        print(e)
        cursor.execute('INSERT INTO url_prdno VALUES (%s);', (prdNo))
        conn.commit()
        time.sleep(random.uniform(5, 10))


# def get_base_information():
#     r = session.get(
#         'http://chn.lottedfs.com/kr/product/productDetail?prdNo=10002278636&dispShopNo1=1200050&dispShopNo2=1200060&dispShopNo3=1200061',
#         headers={'User-Agent': user_agent})
#     a = r.html.xpath("//div[@class='wrap']/div[@class='container']/section[@class='detailSpec']/div[@id='prdDetailTopArea']/div[@class='productName']/span[@class='brand']/text()")
#     b = r.html.xpath("//div[@class='wrap']/div[@class='container']/section[@class='detailSpec']/div[@id='prdDetailTopArea']/div[@class='productName']/em[@class='name']/text()")
#     print(a[0])
#     print(b[0])
# yield a[0], b[0]

def get_REF_price(prdNo, prdOptNo, cookie, user_agent):
    referer = [
        'http://chn.lottedfs.com/kr/display/category/third?dispShopNo1=1200001&dispShopNo2=1200018&dispShopNo3=1200020&treDpth=3',
        'http://chn.lottedfs.com/kr/display/category/third?dispShopNo1=1200001&dispShopNo2=1200011&dispShopNo3=1200016&treDpth=3']
    refer = random.choice(referer)
    try:
        r = session.get('http://chn.lottedfs.com/kr/product/productDetail?prdNo=' + prdNo + '&prdOptNo=' + prdOptNo,
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
                            'Cookie': cookie,
                        })
        a = r.html.search('var prd = {};')
        pytext = json.loads(a[0])
        yield pytext['erpRefNo'], pytext['saleUntPrc'], pytext['saleUntPrcGlbl']
    except BaseException as e:
        print('状态为：')
        print(r.status_code)
        print('>>>>>>>>>>>REF<<<<<<<<<<<<<')
        print(e)
        cursor.execute('INSERT INTO url_prdoptno VALUES (%s,%s);', (prdNo, prdOptNo))
        time.sleep(random.uniform(5, 10))


def get_label_text():
    r = session.get(
        'http://chn.lottedfs.com/kr/product/productDetailBtmInfoAjax?prdNo=10002278636&prdOptNo=10002278636&previewYn=',
        headers={

            'Referer': 'http://chn.lottedfs.com/kr/product/productDetail?prdNo=10002278636&dispShopNo1=1200050&dispShopNo2=1200060&dispShopNo3=1200061',

        })
    a = r.html.xpath(
        "//div[@class='proudctDetail'][2]/div[@class='proudctInfo']/div[@class='tableArea infoTable']/div[@class='tableBox']/table/tbody/tr/th/text()")
    b = r.html.xpath(
        "//div[@class='proudctDetail'][2]/div[@class='proudctInfo']/div[@class='tableArea infoTable']/div[@class='tableBox']/table/tbody/tr/td | (td/div[@class='over current'])")
    # b.remove('\n')
    # for i in b:
    #     print(i.text)
    # print(b)

    for z, x in zip(a, b):
        print(z + '>>>>>>>>' + x.text.replace('\r', '').replace('\n', ''))


def frist():
    UrlList = start_url()
    for url in UrlList:
        a = get_product_first_prdNo(url)
        for i in a:
            cursor.execute('INSERT INTO prdno_form VALUES (%s,%s,%s);', (i[0], i[1], i[2]))
            conn.commit()
            yield i[0]


def two(prdNoList):
    n = 6
    m = 0
    xxx = 0
    cookies = [
        '', '__z_a=1127880195321195202732119', '__z_a=1636588328379128490337912',
        '__z_a=1637439131181785725918178',
        '__z_a=1775940129184604226118460']
    for prdNo in prdNoList:
        time.sleep(random.uniform(0.5, 1))

        if xxx % 15 == 0:
            m = n % 5
            n += 1
        print('第' + str(xxx) + '个')
        xxx += 1
        # cookie = cookies[m]
        user_agent = random.choice(USER_AGENT_LIST)
        print(m)
        print('cookie:', cookies[m])

        a = get_soYn_url(prdNo, cookies[m], user_agent)

        for i in a:
            try:
                cursor.execute(
                    'INSERT INTO ref_price_form(prdNo,prdOptNo,prdChocOptNm,soyn,url) VALUES (%s,%s,%s,%s,%s);',
                    (i[0], i[1], i[2], i[3], i[4]))
                conn.commit()
                yield i[0], i[1]
            except BaseException as e:
                print('数据库问题')
                print(e)


if __name__ == '__main__':
    prdNoList = frist()
    prdOptNo = two(prdNoList)

    n = 6
    m = 0
    xxx = 0
    cookies = ['__z_a=2563488628388978033438897'
        , '__z_a=2858660398303480781230348', '__z_a=3150660123358345909358345'
        , '__z_a=3307398707248380576248380', '__z_a=3525182655155972747315597']
    for i in prdOptNo:
        if xxx % 15 == 0:
            m = n % 5
            n += 1

        user_agent = random.choice(USER_AGENT_LIST)
        time.sleep(random.uniform(1, 1.5))
        a = get_REF_price(i[0], i[1], cookies[m], user_agent)
        for i2 in a:
            try:
                cursor.execute(
                    'UPDATE ref_price_form SET `REF` = %s ,`saleUntPrc` = %s ,`saleUntPrcGlbl` = %s WHERE `prdOptNo` = %s;',
                    (i2[0], i2[1], i2[2], i[1]))
                conn.commit()
                print(i2)
            except BaseException as e:
                print('数据库问题')
                print(e)
