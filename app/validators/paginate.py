# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/18.
"""
from flask import current_app

from app.extensions.http_exception.code_4xx import ParameterException
from app.extensions.validators.req_parse import RequestParser


class PaginateValidator:

    @staticmethod
    def default():
        parse = RequestParser()
        parse.add_argument('page', type=int, default=1)
        parse.add_argument('per_page', type=int, default=current_app.config.get('DEFAULT_PER_PAGE'))

        return parse.parse_args()

    @staticmethod
    def keyword_search(required=True):
        parse = RequestParser()
        parse.add_argument('page', type=int, default=1)
        parse.add_argument('per_page', type=int, default=current_app.config.get('DEFAULT_PER_PAGE'))
        parse.add_argument('keyword', type=str, required=required)

        return parse.parse_args()

