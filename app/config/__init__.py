# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/4/9.
"""

__all__ = ['setting']

import os

from . import web_production, development, production

setting_dict = {
    "web_production": lambda: web_production,
    "development": lambda: development,
    "production": lambda: production,
}

current_evn = os.environ.get("APP_ENV") or "development"

setting = setting_dict.get(current_evn)()


del development
del web_production

print("current_flask_server_env = %s " % current_evn)
