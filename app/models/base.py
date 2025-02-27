# -*- coding: utf-8 -*-
"""
定制的Base
"""
import os
import time
import datetime
import threading
import sqlalchemy as SA
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, Numeric, orm, inspect
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import object_session
from sqlalchemy.ext.declarative import declarative_base
from app.config import setting


class tBase(object):
    session = property(lambda self: object_session(self))
    _append_column_names_ = []  # 序列化时额外展示的字段
    _hide_column_names_ = []  # 序列化时不展示的字段

    # created_date = SA.Column(DATETIME(fsp=6), default=datetime.datetime.now, index=True)
    # modified_date = SA.Column(DATETIME(fsp=6), default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        m = self.__class__.__module__
        c = self.__class__.__name__
        return "<%s.%s id=%s>" % (m, c, self.id)

    @classmethod
    def create(cls, with_commit=True, **kwargs):
        """
          通用创建方法，将属性通过字典形式传入 默认提交，不提交时传入 with_commit=False
          @param kwargs:  键值对
          @return:
        """
        m = cls()
        for k, v in kwargs.items():
            if k in cls.__table__.c.keys():
                setattr(m, k, v)
        db.session.add(m)
        if with_commit:
            db.session.commit()
        return m

    def update(self, with_commit=True, **kwargs):
        """
        通用更新方法，将属性通过字典形式传入 默认提交，不提交时传入 with_commit=False
        @param with_commit: 是否写入数据库
        @param kwargs:  键值对
        @return:
        """
        for k, v in kwargs.items():
            if k in self.__table__.c.keys():
                setattr(self, k, v)
        db.session.add(self)
        if with_commit:
            db.session.commit()
        return self

    def delete(self, with_commit=True):
        db.session.delete(self)
        if with_commit:
            db.session.commit()

    def to_dict(self, append: tuple = (), hide: tuple = ()):
        """通用的将Model转化成dict的简便方法

        :param append: 额外要序列化的属性列表
        :param hide: 不序列化的属性列表
        :return:
        """

        def convert_datetime(value):
            if value:
                return value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                return ""

        d = {}

        for col in self.__table__.columns:
            if col.name in self._hide_column_names_:
                continue
            if col.name in hide:
                continue
            if isinstance(col.type, DateTime):
                value = convert_datetime(getattr(self, col.name))
            elif isinstance(col.type, Numeric):
                value = float(getattr(self, col.name))
            elif col.name.endswith('id') and getattr(self, col.name) is not None:
                value = str(getattr(self, col.name))
            else:
                value = getattr(self, col.name)
            d[col.name] = value

        # for col in [self.__table__.c.created_date, self.__table__.c.modified_date]:
        #     value = convert_datetime(getattr(self, col.name))
        #     d[col.name] = value

        for key in append:
            d[key] = getattr(self, key)

        for key in self._append_column_names_:
            d[key] = getattr(self, key)

        return d


machine_no = None


def get_machine_no():
    """
    从环境变量获取机器编号
    """
    #    machine_no_str = os.environ.get('MACHINE_NO')
    global machine_no
    if not machine_no:
        import socket

        host = socket.gethostname()
        machine_no = setting.MACHINE_NO_DICT.get(host, 1)
        # if machine_no is None:
        #     raise Exception("HOSTNAME: %s is not in the MACHINE_NO_DICT. Please check configuration. " % host)

    return machine_no


# 目前支持的机器编号范围为0~15，每个机器一个机器编号，不允许重复
MACHINE_NO = get_machine_no()


class IdGenerator(object):
    _inc = 0
    _inc_lock = threading.Lock()

    _machine_no = MACHINE_NO

    @staticmethod
    def generate():
        # 32 bits time
        id = (int(time.time()) & 0xffffffff) << 32
        # 4 bits machine number
        id |= (IdGenerator._machine_no & 0xf) << 28
        # 8 bits pid
        id |= (os.getpid() % 0xFF) << 20
        # 20 bits increment number
        IdGenerator._inc_lock.acquire()
        id |= IdGenerator._inc
        IdGenerator._inc = (IdGenerator._inc + 1) % 0xFFFFF
        IdGenerator._inc_lock.release()

        return id


def id_generate():
    return IdGenerator.generate()


Base = declarative_base(cls=tBase)

db = SQLAlchemy(model_class=Base, session_options={"enable_baked_queries": True, "expire_on_commit": False}, )
metadata = db.metadata


class MixinJSONSerializer:
    # 使模型类支持序列化
    @orm.reconstructor
    def init_on_load(self):
        self._fields = []
        # self._include = []
        self._exclude = []

        self._set_fields()
        self.__prune_fields()

    def _set_fields(self):
        """在具体模型类中设置序列化数据，默认序列化处理所有字段。

        若要设置序列化的具体字段，则在模型类中添加此方法，并按例子中格式设置需要序列化的字段。

        eg：
        class Project(Base, MixinJSONSerializer):
            __tablename__ = "project"

            id = SA.Column(BIGINT(unsigned=True), default=id_generate, primary_key=True)
            # 项目标题
            title = SA.Column(VARCHAR(128), nullable=False)
            # 项目封面路径
            cover_id = SA.Column(VARCHAR(128), nullable=True)
            lang = SA.Column(SA.String(10), default="cn", nullable=False)
            # tar_lang = SA.Column(SA.String(10), default="cn", nullable=False)
            image_count = SA.Column(INTEGER, default=0, nullable=True)

            def _set_fields(self):
                self._fields = ['id', 'title']

        Project 类在 _set_fields() 方法中只设置了 'id', 'title' 两个字段，自动序列化时只处理这两个字段。
        """
        pass

    def __prune_fields(self):
        columns = inspect(self.__class__).columns
        if not self._fields:
            all_columns = set(columns.keys())
            self._fields = list(all_columns - set(self._exclude))

    def hide(self, *args):
        """序列化时剔除字段"""
        for key in args:
            self._fields.remove(key)
        return self

    def append(self, *keys):
        """序列化时追加字段"""
        for key in keys:
            self._fields.append(key)
        return self

    def keys(self):
        return self._fields

    def __getitem__(self, key):
        return getattr(self, key)


if __name__ == '__main__':
    pass

