
# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
from app.extensions.http_exception import BaseAPI


class ParameterException(BaseAPI):
    status_code = 400
    error_code = 1000
    msg = 'invalid parameter'


class NotFound(BaseAPI):
    status_code = 404
    error_code = 1001
    msg = "Not Found"


class TokenInvalid(BaseAPI):
    status_code = 401
    error_code = 1002
    msg = "Token Invalid"


class TokenExpired(BaseAPI):
    status_code = 422
    error_code = 1003
    msg = "Token Expired"


class UnAuthorization(BaseAPI):
    status_code = 401
    error_code = 1004
    msg = 'Authorization Failed'


class Forbidden(BaseAPI):
    status_code = 401
    error_code = 10070
    msg = "Forbidden"

