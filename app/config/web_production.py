# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/4/9.
"""
import posixpath

from app.config.base import *

DEBUG = False

# 日志设置
LOG_FILE = posixpath.join(LOG_PATH, 'web_server.log')
LOG_LEVEL = 'DEBUG'
API_LOG_LEVEL = 'DEBUG'
MOBILE_LOG_LEVEL = 'DEBUG'

BASE_SERVER_URL = 'http://127.0.0.1:5000'
