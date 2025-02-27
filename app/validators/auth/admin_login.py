# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/18.
"""
from app.extensions.validators.req_parse import RequestParser


class AdminAuthValidator:

    @staticmethod
    def post_login():
        parse = RequestParser()
        parse.add_argument('account', required=True)
        parse.add_argument('secret', required=True)
        parse.add_argument('type', default=0)
        return parse.parse_args()
