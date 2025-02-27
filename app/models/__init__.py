# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/4/9.
"""
__all__ = ['db', 'Base', 'id_generate', 'User', 'Score']

from .base import db, Base, id_generate
from .score import Score
from .user import User