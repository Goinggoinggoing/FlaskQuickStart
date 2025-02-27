# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/19.
"""
from flask_jwt_extended import jwt_required

from app.extensions.http_exception.code_2xx import Success
from app.extensions.jwt import login_required
from app.utils.redprint import Redprint

test_api = Redprint('test')

@test_api.route('')
def hello():
    return Success('test ok')


@test_api.route('/token')
@login_required()
def hello2():
    return Success('test ok')
