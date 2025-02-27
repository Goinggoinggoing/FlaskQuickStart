# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/16.
"""
import logging
from logging import FileHandler

from flask import Flask
from flask_jwt_extended import verify_jwt_in_request
from flask_migrate import Migrate
from flask_cors import CORS

from app.config import setting
from app.extensions.http_exception import ajax_error_response, InvalidAPIUsage
from app.models import db
from app.extensions.jwt import jwt

def create_web_app():
    _app = Flask(__name__)
    _app.config.from_object(setting)
    configure_db(_app)
    register_web_blueprints(_app)
    configure_error_handler(_app)
    configure_commands(_app)
    configure_jwt(_app)
    configure_logger(_app)
    CORS(_app)
    Migrate(_app, db)
    configure_init_web_data(_app)

    return _app


def register_web_blueprints(_app):
    from app.api.v1 import create_v1
    from app.views.test import test_bp

    _app.register_blueprint(create_v1(), url_prefix='/api/v1')
    _app.register_blueprint(test_bp, url_prefix='/api/test')


def configure_db(_app):
    db.init_app(_app)
    with _app.app_context():
        # 在创建表之前导入一下表的代码，才能正常创建
        # 之后添加新表后，要在 models.__init__.py 中加一个导入代码
        import app.models
        db.create_all()
    Migrate(_app, db)


def configure_error_handler(_app):
    from app.extensions.http_exception import InvalidAPIUsage
    from werkzeug.exceptions import HTTPException
    from werkzeug.routing import ValidationError
    import traceback

    @_app.errorhandler(InvalidAPIUsage)
    def invalid_api_usage(e):
        return ajax_error_response(e.to_dict()['msg'], e.error_code), e.status_code

    @_app.errorhandler(ValidationError)
    def handle_validation_error(e):
        # 能 json 化的数据以 json 化格式返回
        # 不能 json 化的返回字符串
        info = str(e)
        try:
            info = eval(info)
        except Exception:
            info = str(e)
        return ajax_error_response(info, 400, json_msg=True), 400

    @_app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return ajax_error_response(e.description, 999), e.code

    @_app.errorhandler(Exception)
    def handle_error(e):
        # 日志记录
        info = traceback.format_exc()
        _app.logger.error(info)
        return ajax_error_response('Internal server error'), 500


def configure_json_encoder(_app):
    from app.extensions.JSONResponse import JSONResponse
    _app.response_class = JSONResponse


def configure_commands(_app):
    from app.commands import COMMAND_LIST
    for command in COMMAND_LIST:
        _app.cli.add_command(command)


def configure_jwt(_app):
    from flask_jwt_extended import get_current_user
    from flask import g

    jwt.init_app(_app)

    # Token 过期的自定义函数
    @jwt.expired_token_loader
    def my_expired_token_callback(jwt_header, jwt_payload):
        return ajax_error_response(msg='Token Expired', error_code=1003), 401

    @jwt.invalid_token_loader
    def my_invalid_token_callback(jwt_payload):
        return ajax_error_response(msg=jwt_payload, error_code=1002), 422

    @jwt.unauthorized_loader
    def my_unauthorized_callback(jwt_payload):
        return ajax_error_response(msg='Missing Token', error_code=1002), 401

    @_app.before_request
    def push_current_user():
        url = InvalidAPIUsage.get_url_no_param()
        skip_urls = ('/api/v1/auth/login', '/api/v1/auth/register', '/api/v1/token/refresh',
                     '/api/admin/auth/login')

        skip_urls = ['POST %s' % item for item in skip_urls]
        if not url.startswith('OPTIONS') and url not in skip_urls:
            verify_jwt_in_request(optional=True)
            g.current_user = get_current_user()


def configure_logger(app):
    format_str = '%(asctime)s %(levelname)s in %(pathname)s:%(lineno)d :\n%(message)s'
    formatter = logging.Formatter(format_str)
    debug_log = app.config['LOG_FILE']

    debug_file_handler = FileHandler(debug_log)
    if app.config["LOG_LEVEL"]:
        log_level = app.config["LOG_LEVEL"]
    else:
        if app.config["DEBUG"]:
            log_level = logging.DEBUG
        else:
            log_level = logging.WARNING

    debug_file_handler.setLevel(log_level)
    debug_file_handler.setFormatter(formatter)
    # 正常情况下默认有一个 StreamHandler，再加一个 FileHandler，一共有两个
    # reloader 会在启动 app 后再次从新载入，导致添加两个 FileHandler，在日志文件写两次日志
    # 所以判断下是否已有两个 handler，有的话则不再 addHander
    if not app.debug and len(app.logger.handlers) != 2:
        app.logger.addHandler(debug_file_handler)

def configure_init_web_data(_app):
    """"""
    pass
