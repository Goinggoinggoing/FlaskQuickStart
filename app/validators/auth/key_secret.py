# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/23.
"""
from app.extensions.validators.req_parse import RequestParser


class KeySecretValidator:

    @staticmethod
    def plain_key_secret(required=True):
        parse = RequestParser()
        parse.add_argument('app_key', required=required)
        parse.add_argument('app_secret', required=required)
        return parse.parse_args()

    @staticmethod
    def app_code(required=True):
        parse = RequestParser()
        parse.add_argument('app_code', required=required)
        return parse.parse_args()
