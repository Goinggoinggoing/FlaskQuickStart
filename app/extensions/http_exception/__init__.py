# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/21.
"""
__all__ = ['InvalidAPIUsage', 'BaseAPI', 'code_4xx', 'code_2xx', 'ajax_error_response']

from .base_api import InvalidAPIUsage, BaseAPI
from . import code_4xx
from . import code_2xx


def ajax_error_response(msg="", error_code=999, json_msg=False):
    # if json_msg: msg 存储json格式数据
    # else: 字符串
    msg = msg if json_msg else u'%s' % msg
    return {
        'error_code': error_code,
        'msg': msg,
        'request': InvalidAPIUsage.get_url_no_param(),
        'data': None
    }
