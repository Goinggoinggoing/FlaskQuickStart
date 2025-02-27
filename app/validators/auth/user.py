# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
import re
from flask_restful import inputs
from werkzeug.routing import ValidationError

from app.extensions.validators.req_parse import RequestParser
from app.models import User
from app.utils.enum_types import LoginEnum
from app.validators.validate_type_func import len_limit


class UserValidator:
    regex_email = r"^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$"
    regex_pwd = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$"
    regex_phone = r"1[3|4|5|7|8][0-9]{9}"

    @classmethod
    def post_auth_login(cls):
        """
        邮箱校验登录
        """
        parse = RequestParser()
        parse.add_argument('account', required=True, trim=True, help='账号不能为空')
        parse.add_argument('secret', required=True, trim=True)
        parse.add_argument('type', type=int, choices=[item.value for item in LoginEnum],
                           default=LoginEnum.EMAIL.value, help="请选择正确的登录方式",
                           dest='login_type')
        args = parse.parse_args()
        if args['login_type'] == 0 and not re.match(cls.regex_email, args['account']):
            raise ValidationError('邮箱格式错误')
        # elif args['login_type'] == 1 and not re.match(cls.regex_phone, args['account']):
        #     raise ValidationError('手机号格式错误')
        return args

    @classmethod
    def post_auth_register(cls):
        """账号注册"""
        parse = RequestParser()
        parse.add_argument("nickname", type=len_limit(min_len=1, max_len=128, data_type=str))
        parse.add_argument('account', type=inputs.regex(cls.regex_email), required=True, trim=True, help='邮箱格式错误')
        parse.add_argument('secret', type=inputs.regex(cls.regex_pwd), required=True, trim=True, help='密码格式错误')
        parse.add_argument('confirm_secret', type=inputs.regex(cls.regex_pwd), required=True, trim=True, help='密码格式错误')
        args = parse.parse_args()

        if args.get('secret') != args.get('confirm_secret'):
            raise ValidationError("密码输入不一致")
        UserValidator._validate_user_exist(args)

        return args

    @classmethod
    def post_auth_ty_register(cls):
        """账号注册"""
        parse = RequestParser()
        parse.add_argument("account", type=len_limit(min_len=1, max_len=128, data_type=str), dest='phone')
        parse.add_argument('username', type=str, required=True, trim=True, )
        parse.add_argument('password', type=inputs.regex(cls.regex_pwd), required=True, trim=True, help='密码格式错误')
        parse.add_argument('confirmPassword', type=inputs.regex(cls.regex_pwd), required=True,
                           trim=True, help='密码格式错误', dest='confirm_password')
        parse.add_argument('location', type=int, required=True)
        args = parse.parse_args()

        if args.get('password') != args.get('confirm_password'):
            raise ValidationError("密码输入不一致")
        UserValidator._validate_user_exist(args)

        args['nickname'] = UserValidator._secure_nickname(args['username'])

        return args

    @staticmethod
    def _validate_user_exist(args):
        """校验用户存在性"""
        user = User.query.filter_by(phone=args['phone']).first()
        if user:
            raise ValidationError("该手机号已被注册")

        user = User.query.filter_by(email=args['email']).first()
        if user:
            raise ValidationError('该邮箱已被注册')

    @staticmethod
    def _secure_nickname(nickname):
        nickname_count = User.query.filter(User.nickname.like(f'{nickname}%')).count()
        if nickname_count > 0:
            return '%s_%s' % (nickname, nickname_count)
        return nickname

    @classmethod
    def put_auth_profile(cls):
        parse = RequestParser()
        parse.add_argument("nickname", type=len_limit(min_len=1, max_len=128, data_type=str))
        parse.add_argument('avatar_id')
        args = parse.parse_args()
        return args

    @classmethod
    def post_auth_reset_pwd(cls):
        """修改密码"""
        parse = RequestParser()
        parse.add_argument('old_pwd', type=inputs.regex(cls.regex_pwd), required=True, trim=True, help='密码格式错误')
        parse.add_argument('pwd', type=inputs.regex(cls.regex_pwd), required=True, trim=True, help='密码格式错误')
        parse.add_argument('confirm_pwd', type=inputs.regex(cls.regex_pwd), required=True, trim=True, help='密码格式错误')
        args = parse.parse_args()
        if args.get('pwd') != args.get('confirm_pwd'):
            raise ValidationError("密码输入不一致")
        args.pop("confirm_pwd")
        return args

    @classmethod
    def post_auth_register(cls, is_ban: bool = False):
        parse = RequestParser()
        parse.add_argument('purpose', type=len_limit(min_len=1, max_len=512, data_type=str), help='用途必填')
        parse.add_argument('username', type=len_limit(min_len=1, max_len=128, data_type=str), help='姓名必填')
        parse.add_argument('identity', type=len_limit(min_len=1, max_len=512, data_type=str), help='职称/身份必填')
        parse.add_argument('field', type=len_limit(min_len=1, max_len=512, data_type=str), help='专业领域必填')
        parse.add_argument('address', type=len_limit(min_len=1, max_len=512, data_type=str), help='联系地址必填')
        parse.add_argument('email', type=inputs.regex(cls.regex_email), required=True, trim=True, help='邮箱格式错误')
        parse.add_argument('postal_code', type=len_limit(min_len=1, max_len=32, data_type=str), help='邮编必填')
        parse.add_argument('phone', type=inputs.regex(cls.regex_phone), required=True, trim=True, help='手机号错误')
        parse.add_argument('secret', type=len_limit(min_len=8, max_len=64, data_type=str),
                           required=True, trim=True, help='密码格式错误')
        parse.add_argument('confirm_secret', type=len_limit(min_len=8, max_len=64, data_type=str),
                           required=True, trim=True, help='密码格式错误')
        args = parse.parse_args()
        args.setdefault('is_ban', is_ban)

        if args.get('secret') != args.get('confirm_secret'):
            raise ValidationError("密码输入不一致")

        UserValidator._validate_user_exist(args)

        return args

    @classmethod
    def post_auth_login(cls):
        parse = RequestParser()
        parse.add_argument('account', required=True, trim=True, help='账号不能为空')
        parse.add_argument('secret', required=True, trim=True)

        args = parse.parse_args()

        if re.match(cls.regex_email, args['account']) is not None:
            args['login_type'] = LoginEnum.EMAIL.value
        else:
            args['login_type'] = LoginEnum.PHONE.value

        return args
