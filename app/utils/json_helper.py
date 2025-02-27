# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/18.
"""
from typing import Union

from app import setting
from app.extensions.http_exception.code_2xx import Success


def jsonify_paginate(paginate, append: tuple = (), hide: tuple = (), to_dict=True):
    items = ([item.to_dict(append, hide) for item in paginate.items]
             if to_dict
             else paginate.items)
    data = {
        "items": items,
        "pageinfo": jsonify_pageinfo(paginate)
    }
    return Success(data)


def jsonify_pageinfo(paginate):
    return {
        "page": paginate.page,
        "page_size": paginate.per_page,
        "has_next": paginate.has_next,
        "pages": paginate.pages,
        "total": paginate.total
    }


def build_full_url(url: str) -> str:
    return '%s%s' % (setting.BASE_SERVER_URL, url)


def wrap_two_length(number: Union[int, str]) -> str:
    if len(str(number)) < 2:
        number = '0%s' % number

    return number
