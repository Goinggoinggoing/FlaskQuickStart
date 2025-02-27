# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/17.
"""
from flask_jwt_extended import get_jwt_identity
from flask import g
from werkzeug.routing import ValidationError

from app.extensions.http_exception.code_2xx import Success
from app.extensions.jwt import login_required
from app.utils.redprint import Redprint
from app.models import User
from app.validators.auth import UserValidator

user_api = Redprint('user')


@user_api.route('/profile', methods=['GET'])
@login_required()
def get_user_profile():
    user = g.current_user
    return Success(user.to_dict())


@user_api.route('/profile', methods=['PUT'])
@login_required()
def update_user_profile():
    form = UserValidator.put_auth_profile()
    user = g.current_user
    user = user.update(**form)
    return Success(user.to_dict())


@user_api.route('/reset_pwd', methods=['PUT'])
@login_required()
def update_user_pwd():
    form = UserValidator.post_auth_reset_pwd()
    user = g.current_user
    if not user.check_password(form['old_pwd']):
        raise ValidationError("原始密码错误")
    user.set_password(form['pwd'])
    return Success()
