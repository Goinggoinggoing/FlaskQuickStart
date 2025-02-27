# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
from app.extensions.validators.req_parse import RequestParser


class TokenValidator:

    @staticmethod
    def post_get_token():
        parse = RequestParser()
        parse.add_argument('app_key', type=str, required=True)
        parse.add_argument('app_secret', type=str, required=True)
        args = parse.parse_args()
        return args

    @staticmethod
    def post_auth_token():
        parse = RequestParser()
        parse.add_argument('token', type=str, required=True)
        args = parse.parse_args()
        return args


