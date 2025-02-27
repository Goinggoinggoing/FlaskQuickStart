# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/4/9.
"""
import os
from datetime import timedelta

ECHO_SQL = False
SECRET_KEY = 'cooperation translate platform key'
PROPAGATE_EXCEPTIONS = True
APP_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


LOG_PATH = os.path.join(APP_PATH, "log")
SQLALCHEMY_TRACK_MODIFICATIONS = True

MAIN_HOST = '127.0.0.1'

MAIN_DB = {
    'host': '',
    'db_name': '',
    'user': '',
    'password': '',
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
    '192.168.1.4': 4,
    'VM-0-14-ubuntu': 5
}

CHECK_API_TOKEN = False

# JWT 相关
JWT_COOKIE_SECURE = False
JWT_TOKEN_LOCATION = ["cookies", "headers", "query_string", "json"]
JWT_SECRET_KEY = '74823d6d3dae49e082110585a8fc6d4f'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)


DEFAULT_PER_PAGE = 10