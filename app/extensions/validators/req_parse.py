# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/22.
"""
import six
from flask import current_app
from flask_restful.reqparse import Argument as BaseArgument
from flask_restful.reqparse import RequestParser as BaseRequestParser
from werkzeug.routing import ValidationError



class Argument(BaseArgument):
    def handle_validation_error(self, error, bundle_errors):
        """Called when an error is raised while parsing. Aborts the request
        with a 400 status and an error message

        :param error: the error that was raised
        :param bundle_errors: do not abort when first error occurs, return a
            dict with the name of the argument and the error message to be
            bundled
        """
        error_str = six.text_type(error)
        error_msg = self.help.format(error_msg=error_str) if self.help else error_str
        msg = {self.name: error_msg}

        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, msg
        raise ValidationError(msg)


class RequestParser(BaseRequestParser):
    def __init__(self):
        super(RequestParser, self).__init__(argument_class=Argument)
