# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
from functools import wraps

from flask_jwt_extended import (
    JWTManager,
    get_current_user,
    verify_jwt_in_request
)

from app.extensions.http_exception.code_4xx import UnAuthorization

jwt = JWTManager()


def admin_required():
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_current_user()
            if not current_user.is_admin:
                raise UnAuthorization('只有超级管理员可操作')
            return func(*args, **kwargs)

        return wrapped_func

    return decorator


def login_required():
    def decorator(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_current_user()
            if current_user.is_ban:
                raise UnAuthorization('当前账号处于未激活状态')
            return func(*args, **kwargs)

        return wrapped_func

    return decorator


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    from app.models.user import User
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()
