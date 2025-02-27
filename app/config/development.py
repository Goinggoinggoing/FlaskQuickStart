# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/4/9.
"""
import posixpath
from datetime import timedelta

from app.config.base import *

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

# 日志设置
LOG_FILE = posixpath.join(LOG_PATH, 'admin_server.log')
LOG_LEVEL = 'DEBUG'
API_LOG_LEVEL = 'DEBUG'
MOBILE_LOG_LEVEL = 'DEBUG'

# 数据库设置
MAIN_HOST = '127.0.0.1'
BASE_SERVER_URL = 'http://%s:%s' % (HOST, PORT)

MAIN_DB = {
    'host': '127.0.0.1:3306',
    'db_name': 'flaskstudy',
    'user': 'root',
    'password': '123456',
}  # CREATE SCHEMA `cooperation` DEFAULT CHARACTER SET utf8 ;

MAIN_DB_URI = 'mysql+pymysql://%s:%s@%s/%s?charset=utf8mb4' % (
    MAIN_DB['user'], MAIN_DB['password'], MAIN_DB['host'], MAIN_DB['db_name'])

# SQLAlchemy Config
SQLALCHEMY_DATABASE_URI = MAIN_DB_URI
SQLALCHEMY_ECHO = False
SQLALCHEMY_POOL_SIZE = 5
SQLALCHEMY_POOL_TIMEOUT = 120
SQLALCHEMY_POOL_RECYCLE = 360

MEMCACHED_MACHINES = ['%s:11211' % MAIN_HOST]

#: 机器hostname 到 machine_no 的映射。机器编号范围为0~15
MACHINE_NO_DICT = {
    'LAPTOP-42FOC6P5': 0,
    'personal-cbec': 1,
    '192.168.1.4': 4
}

CHECK_API_TOKEN = False

# JWT 相关
JWT_COOKIE_SECURE = False
JWT_TOKEN_LOCATION = ["cookies", "headers", "query_string", "json"]
JWT_SECRET_KEY = 'absdafjlkasdf'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
