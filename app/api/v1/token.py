# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

from app.extensions.http_exception.code_2xx import Success
from app.extensions.http_exception.code_4xx import Forbidden
from app.extensions.jwt import login_required
from app.models.user import User
from app.utils.redprint import Redprint
from app.validators.auth import TokenValidator

token_api = Redprint('token')


@token_api.route('', methods=['POST'])
def get_token():
    form = TokenValidator.post_get_token()
    tokens = User.gene_token(**form)
    return Success(data=tokens)


@token_api.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    user = User.query.get(identity)
    if user.status == 0:
        raise Forbidden('用户状态不可用，请联系管理员')
    return Success({'access_token': user.generate_access_token()})


@token_api.route('/auth', methods=['GET'])
@login_required()
def auth_token():
    return Success({'jwt': get_jwt()})
