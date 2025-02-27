# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/19.
"""
from flask import Blueprint


def create_v1():
    bp_v1 = Blueprint("api/v1", __name__)

    from .auth import auth_api
    from .test import test_api
    from .token import token_api
    from .user import user_api

    auth_api.register(bp_v1)
    test_api.register(bp_v1)
    token_api.register(bp_v1)
    user_api.register(bp_v1)
    
    from .score import score_api
    score_api.register(bp_v1)

    return bp_v1
