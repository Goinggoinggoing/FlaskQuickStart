# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/17.
"""
from app.extensions.http_exception.code_2xx import Success
from app.utils.redprint import Redprint
from app.validators.auth.user import UserValidator
from app.models import User

auth_api = Redprint('auth')


@auth_api.route('/register', methods=['POST'])
def register():
    form = UserValidator.post_auth_register()
    form.pop('confirm_secret')
    user = User.register_by(**form)
    return Success(user.generate_token())


@auth_api.route('/login', methods=['POST'])
def login():
    form = UserValidator.post_auth_login()
    user = User.login(**form)
    return Success(user.generate_token())
