# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/7/13.
"""
import uuid
import cv2
import os

import datetime
from flask import current_app

from app.utils.image_helpers.common_img_helper import CommonImgHelper


class TestImgHelper(CommonImgHelper):

    def __init__(self, is_test=None, test_output_path='/data/images/'):
        """辅助与图片相关的测试
        
        :param is_test: 是否开启测试
        :param test_output_path: 测试结果输出路径
        """
        super().__init__()
        # 是否为测试模式
        if is_test is None:
            self.is_test = current_app.config.get('DEBUG')
        else:
            self.is_test = is_test
        self.test_output_path = test_output_path  # 测试时写入图片的路径
        self.exists_test_output_path = False  # 测试结果输出路径是否存在

    def write_img(self, img_data, img_name, with_unique=False, suffix='jpg'):
        """将图片写入本地

        :param img_data: cv2 格式的图片
        :param img_name: 图片名
        :param with_unique: 图片名是否附加时间后缀
        :param suffix: 文件名后缀
        :return: None
        """
        if self.is_test:
            # 测试结果输出目录不存在时创建该目录
            if not self.exists_test_output_path and not os.path.exists(self.test_output_path):
                os.makedirs(self.test_output_path)
                os.chmod(self.test_output_path, 0o777)
                self.exists_test_output_path = True
            if with_unique:
                img_name = "%s_%s.%s" % (img_name, uuid.uuid4(), suffix)
            else:
                img_name = "%s.%s" % (img_name, suffix)
            cv2.imwrite(self.test_output_path + img_name, img_data)
            print('图片 %s 已保存在 %s' % (img_name, self.test_output_path + img_name))

    def rectangle_and_write(self, img_data, img_name, x, y, w, h, with_unique=False):
        """在图片（img_data）上绘制矩形并将图片写入本地
        
        :param img_data: 
        :param img_name: 
        :param x: 
        :param y: 
        :param w: 
        :param h: 
        :param with_unique: 图片命名是否附加独一无二的后缀
        :return: 
        """
        cv2.rectangle(img_data, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 2)
        if with_unique:
            filename, extension = img_name.split('.')
            img_name = filename + str(uuid.uuid4()) + '.' + extension
        self.write_img(img_data, img_name)

    def rectangle(self, img_data, x, y, w, h, color=(0, 255, 0)):
        cv2.rectangle(img_data, (int(x), int(y)), (int(x + w), int(y + h)), color, 2)

    @staticmethod
    def break_line():
        print("-"*30)
