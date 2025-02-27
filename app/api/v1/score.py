# -*- coding: utf-8 -*-
"""
  Created by ByteBind on 2025/2/27.
"""
from app.extensions.http_exception.code_2xx import Success, SuccessWithMessage
from app.extensions.http_exception.code_4xx import NotFound
from app.extensions.jwt import login_required
from app.utils.redprint import Redprint
from app.extensions.validators.req_parse import RequestParser
from app.dao.score_dao import ScoreDAO
from flask import current_app

score_api = Redprint('score')


@score_api.route('/search_all', methods=['POST'])
@login_required()
def search_all():
    """获取所有成绩"""
    scores = ScoreDAO.get_all()
    return Success([x.to_dict() for x in scores])


@score_api.route('/search', methods=['POST'])
@login_required()
def search():
    """分页搜索成绩"""
    parse = RequestParser()
    parse.add_argument('page', type=int, default=1)
    parse.add_argument('per_page', type=int, default=current_app.config.get('DEFAULT_PER_PAGE'))
    parse.add_argument('keyword', type=str, required=False)

    form = parse.parse_args()
    page = form["page"]
    per_page = form["per_page"]
    keyword = form["keyword"]

    result = ScoreDAO.search(keyword, page, per_page)

    return Success({
        "total": result.total,
        "page": page,
        "per_page": per_page,
        "items": [x.to_dict() for x in result.items]
    })


@score_api.route('/add', methods=['POST'])
@login_required()
def add():
    """添加成绩"""
    parse = RequestParser()
    parse.add_argument('student_id', type=int, required=True)
    parse.add_argument('subject', type=str, required=True)
    parse.add_argument('score_value', type=float, required=True)
    parse.add_argument('semester', type=str, required=True)

    form = parse.parse_args()

    new_score = ScoreDAO.add(
        student_id=form["student_id"],
        subject=form["subject"],
        score_value=form["score_value"],
        semester=form["semester"]
    )

    return SuccessWithMessage("成绩添加成功", new_score.to_dict())


@score_api.route('/update', methods=['POST'])
@login_required()
def update():
    """更新成绩"""
    parse = RequestParser()
    parse.add_argument('score_id', type=int, required=True)
    parse.add_argument('score_value', type=float, required=True)

    form = parse.parse_args()

    score = ScoreDAO.update(
        score_id=form["score_id"],
        score_value=form["score_value"]
    )

    if not score:
        raise NotFound()

    return SuccessWithMessage("成绩更新成功", score.to_dict())


@score_api.route('/delete', methods=['POST'])
@login_required()
def delete():
    """删除成绩"""
    parse = RequestParser()
    parse.add_argument('score_id', type=int, required=True)

    form = parse.parse_args()

    score = ScoreDAO.delete(form["score_id"])

    if not score:
        raise NotFound()

    return SuccessWithMessage("成绩删除成功")