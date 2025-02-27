# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/14.
"""
from flask import Blueprint, render_template

test_bp = Blueprint('experiment', __name__, static_folder='static', template_folder='templates')


@test_bp.route("/")
def experiment():
    return render_template('test.html')
