# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/18.
"""
from werkzeug.routing import ValidationError


def len_limit(min_len, max_len, data_type=None):
    """参数长度限制

    :param min_len:
    :param max_len:
    :param data_type: 参数类型
    :return:
    """
    def validate(data):
        if data_type is not None and not isinstance(data, data_type):
            raise ValidationError('data_type must be %s' % data_type)

        if not (min_len <= len(data) <= max_len):
            raise ValidationError('length must between %s and %s' % (min_len, max_len))

        return data

    return validate
