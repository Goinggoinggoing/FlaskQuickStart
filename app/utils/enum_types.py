# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2022/3/14.
"""
from enum import Enum, unique


@unique
class FileChannelEnum(Enum):
    """文件存储渠道"""
    ALIOSS = 0                  # 阿里OSS
    SEAWEED = 1                 # seaweed
    LOCAL = 2                   # 本地


@unique
class UserActionEnum(Enum):
    """用户行为类型"""
    REGISTER = 0                # 注册
    LOGIN = 1                   # 登录
    LOGOUT = 2                  # 登出


@unique
class DownloadCountChangeEnum(Enum):
    """下载数量改变类型"""
    INIT = 0                    # 初始化
    PAY = 1                     # 充值购买
    DOWNLOAD = 2                # 下载
    C_P_REWARD = 3              # 累计充值奖励


@unique
class NoticeEnum(Enum):
    """通知类型"""
    DEFAULT = 0


@unique
class PayTypeEnum(Enum):
    """支付类型"""
    PAYPAL = 0
    WECHAT = 1
    ALIPAY = 2
    OFFICIAL = 3


@unique
class PayStateEnum(Enum):
    """支付状态"""
    INIT = 0                    # 初始化
    PENDING = 1                 # 处理中
    SUCCESS = 2                 # 已应用,和商户对接完成
    CANCEL = 3                  # 取消了
    FAILED = 4                  # 失败了


@unique
class PayPlanStateEnum(Enum):
    """购买套餐状态"""
    INIT = 0                    # 初始化
    PENDING = 1                 # 处理中
    SUCCESS = 2                 # 成功。完成加量
    CANCEL = 3                  # 取消
    FAILED = 4                  # 失败


@unique
class LoginEnum(Enum):
    """登录/注册类型"""
    EMAIL = 0                   # 邮箱登录
    PHONE = 1                   # 手机登录


@unique
class FontTypeEnum(Enum):
    """字体文件类型"""
    ADMIN = 0
    USER = 1


@unique
class PayPlanTypeEnum(Enum):
    """套餐类型"""
    INIT = 0                    # 初始套餐
    OFFICIAL = 1                # 官方制定的套餐
    CUSTOM = 2                  # 用户自由购买的套餐
