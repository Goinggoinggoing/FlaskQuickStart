# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/4/9.
"""
from app import create_web_app

application = create_web_app()

if __name__ == '__main__':
    from app.config import setting
    application.run(port=setting.PORT)
