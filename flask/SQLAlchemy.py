# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
# 连接数据库
engine = create_engine("mysql+pymysql://root:cscs123456@localhost:3306/lt?charset=utf8",encoding="utf-8", echo=True)
# 获取元数据
metadata = MetaData()
# 定义表
user = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(20)),
    Column('fullname', String(40)),
  )

address = Table('address', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', None),
    Column('email', String(60), nullable=False)
  )
# 创建数据表，如果数据表存在，则忽视
metadata.create_all(engine)
# 获取数据库连接
conn = engine.connect()