# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
from app.extensions.http_exception import InvalidAPIUsage, BaseAPI


# class Success(InvalidAPIUsage):
#     status_code = 200
#
#     def __init__(self, data=None, msg='ok', error_code=0):
#         super().__init__(
#             msg=msg,
#             status_code=Success.status_code,
#             payload={
#                 'error_code': error_code,
#                 'data': data
#             }
#         )


class TrialForbidden(BaseAPI):
    status_code = 200
    error_code = 2000
    msg = 'The number of trials has been used up.'


# TODO: 封装 Success 类
# def Success(data=None):
#     return {
#             "msg": "ok",
#             "data": data,
#             "request": InvalidAPIUsage.get_url_no_param(),
#             "error_code": 0
#         }

def Success(data=None):
    return {
        "msg": "ok",
        "data": data,
        "request": InvalidAPIUsage.get_url_no_param(),
        "error_code": 0
    }

def SuccessWithMessage(msg=None, data=None):
    return {
        "msg": msg,
        "data": data,
        "request": InvalidAPIUsage.get_url_no_param(),
        "error_code": 0
    }

class BalanceNotEnough(BaseAPI):
    status_code = 200
    error_code = 3001
    msg = '余额不足，请充值'
