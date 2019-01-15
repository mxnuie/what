import pymysql

conn = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='cscs123456',
                             db='lt',
                             charset='utf8')
cursor = conn.cursor()

