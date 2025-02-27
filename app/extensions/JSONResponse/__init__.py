# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/21.
"""
__all__ = ['JSONResponse']

from flask import Response


class JSONResponse(Response):
    def __init__(self):
        super(JSONResponse, self).__init__(content_type='application/json')
