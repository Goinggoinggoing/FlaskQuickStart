# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
from flask import request


class InvalidAPIUsage(Exception):
    status_code = 400

    def __init__(self, msg='invalid request', status_code=None, payload=None):
        super().__init__()
        self.msg = msg
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['msg'] = self.msg
        rv['request'] = InvalidAPIUsage.get_url_no_param()
        return rv

    @staticmethod
    def get_url_no_param():
        """获取访问路由"""
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return "%s %s" % (request.method, main_path[0])


class BaseAPI(InvalidAPIUsage):
    status_code = 200
    error_code = 0
    msg = 'ok'

    def __init__(self, msg=None, data=None, error_code=None):
        if error_code is None:
            error_code = self.error_code
        if msg is None:
            msg = self.msg
        super().__init__(
            msg=msg,
            status_code=self.status_code,
            payload={
                'error_code':  error_code,
                'data': data
            }
        )
