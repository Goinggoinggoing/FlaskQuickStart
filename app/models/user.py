# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/14.
"""
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, func, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, TINYINT, VARCHAR, BOOLEAN
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions.http_exception.code_4xx import UnAuthorization
from app.utils import memcache_tool
from app.models import Base, id_generate, db
from app.utils.enum_types import LoginEnum


class User(Base):
    """用户表

    用户邮箱与手机号二者至少存在一个，且全局唯一
    """
    __tablename__ = 'user'

    # 不展示属性
    _hide_column_names_ = ['pw_hash']
    _append_column_names_ = ['avatar', 'roles']

    id = Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
    nickname = Column(VARCHAR(128), nullable=False, unique=True)  # 用户昵称
    username = Column(VARCHAR(128), nullable=True, unique=False)  # 用户真实姓名
    email = Column(VARCHAR(128), unique=True)  # 邮箱
    phone = Column(VARCHAR(32), unique=True)  # 手机号
    pw_hash = Column(VARCHAR(128), nullable=True)  # 密码加密后内容
    avatar_id = Column(BIGINT(unsigned=True))  # 用户头像
    # status = Column(TINYINT, default=1)  # 状态
    is_ban = Column(BOOLEAN, default=False)  # 是否禁用
    is_admin = Column(BOOLEAN, default=False)  # 是否为admin账户
    purpose = Column(VARCHAR(512), nullable=False, doc='用途')
    identity = Column(VARCHAR(512), nullable=False, doc='职称/身份')
    field = Column(VARCHAR(512), nullable=False, doc='专业领域')
    address = Column(VARCHAR(512), nullable=False, doc='联系地址')
    postal_code = Column(VARCHAR(32), nullable=False, doc='邮编')
    we_mini_id = Column(VARCHAR(128), unique=True, doc='微信小程序用户标识')

    def set_password(self, pw, **kwargs):
        if kwargs.get('key'):
            if memcache_tool.memcache_get(kwargs.get('key')) == self.email:
                memcache_tool.memcache_set(kwargs.get('key'), None)
            else:
                return False

        self.pw_hash = generate_password_hash(pw, salt_length=16)
        db.session.add(self)
        db.session.commit()
        return True

    def check_password(self, pw):
        return check_password_hash(self.pw_hash, pw)

    def generate_token(self):
        return {
            'access_token': self.generate_access_token(),
            'refresh_token': self.generate_refresh_token()
        }

    def generate_access_token(self):
        """
        生成 access_token
        :return:
        """
        return create_access_token(
            identity=self.id,
            additional_claims={'is_admin': self.is_admin})

    def generate_refresh_token(self):
        return create_refresh_token(
            identity=self.id,
            additional_claims={'is_admin': self.is_admin})

    @classmethod
    def search_user(
            cls,
            query: BaseQuery,
            username: str = None,
            nickname: str = None,
            email: str = None,
            phone: str = None
    ) -> BaseQuery:
        if username:
            query = query.filter(User.username.like(f'%{username}%'))
        if nickname:
            query = query.filter(User.nickname.like(f"%{nickname}%"))
        if email:
            query = query.filter(User.email.like(f"%{email}%"))
        if phone:
            query = query.filter(User.phone.like(f"%{phone}%"))

        return query

    @classmethod
    def base_register(cls, nickname, email, pw):
        user_model = cls.create(nickname=nickname, email=email)
        user_model.set_password(pw)

        return user_model

    @classmethod
    def register_by_phone(cls, phone, pw, username, nickname):
        user_model = cls.create(phone=phone, nickname=nickname, username=username)
        user_model.set_password(pw)

        return user_model

    @classmethod
    def register_by(cls, purpose: str, username: str, identity: str, field: str, address: str,
                         email: str, postal_code: str, phone: str, secret: str, is_ban: bool):
        exists_user_count = cls.query.filter(cls.nickname == username).count()

        if exists_user_count > 0:
            nickname = '%s_%s' % (username, exists_user_count + 1)
        else:
            nickname = username

        user_model = cls.create(purpose=purpose, username=username, nickname=nickname, identity=identity, field=field,
                                address=address, email=email, postal_code=postal_code, phone=phone, is_ban=is_ban)
        user_model.set_password(secret)

        return user_model

    @classmethod
    def login(cls, account, secret=None, login_type=LoginEnum.EMAIL.value, is_admin=False):
        if login_type == LoginEnum.EMAIL.value:
            user = User.query.filter_by(email=account).first_or_404('account not found.')
        else:
            user = User.query.filter_by(phone=account).first_or_404('account not found.')

        if is_admin:
            if not user.is_admin:
                raise UnAuthorization('无权限登录')

        if user.is_ban:
            raise UnAuthorization('账号被禁用')

        if not user.check_password(secret):
            raise UnAuthorization('账号或密码错误')

        return user

    @property
    def roles(self):
        roles_map = []
        if self.is_admin:
            roles_map.append('admin')
        else:
            roles_map.append('visitor')

        return roles_map
