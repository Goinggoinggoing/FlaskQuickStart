# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/7/13.
"""
import base64

import decimal
import os
import io

from io import BytesIO

import requests
from flask import current_app

try:
    from PIL import Image as PILImage, ImageDraw, ImageFont
except ImportError:
    import Image as PILImage, ImageDraw, ImageFont

import cv2
import numpy as np


class CommonImgHelper:
    """集成进行图片相关操作的常用方法"""

    @staticmethod
    def bytes_to_cv2(img_bytes, flags=cv2.IMREAD_UNCHANGED):
        """二进制流数据转cv2图片

        :param img_bytes: 图片数据流
        :param flags: 读取模式
        :return: cv2 格式的图片
        """
        return cv2.imdecode(np.fromstring(img_bytes, np.uint8), flags)

    @staticmethod
    def base64_to_bytes(base64_string):
        """base64数据转二进制流"""
        if base64_string.startswith("data:image"):
            base64_string = CommonImgHelper.base64_filter(base64_string)
        return base64.b64decode(base64_string)

    @classmethod
    def get_cv2_img_by_image_id(cls, image_id):
        """通过image_id获取cv2格式的图片"""
        return cls.bytes_to_cv2(cls.get_bytes_img_by_image_id(image_id))

    @classmethod
    def get_cv2_img_by_image_file(cls, image_file):
        """通过 image_file 对象获取 cv2 格式的图像数据
        
        :param image_file: ImageFile 的实例
        :return: cv2 格式图像
        """
        return cls.bytes_to_cv2(cls.get_bytes_img_by_image_file(image_file))

    @classmethod
    def get_pil_img_by_image_file(cls, image_file):
        """通过 image_file 对象获取 PIL 格式的图像数据
        
        :param image_file: 
        :return: 
        """
        return PILImage.open(io.BytesIO(cls.get_bytes_img_by_image_file(image_file)))

    @classmethod
    def get_bytes_img_by_image_file(cls, image_file):
        """通过 image_file 获取二进制图像数据
        
        :param image_file: ImageFile 的实例
        :return: 图像字节流
        """
        flag = 3
        img_bytes = image_file.get_content()
        while img_bytes is None and flag:
            img_bytes = image_file.get_content()
            flag -= 1
        return img_bytes

    @staticmethod
    def base64_to_cv2img(base64_string, flag=cv2.IMREAD_UNCHANGED):
        u"""
        转化base64 string to opencv image
        :param base64_string: string
        :param flag: string
        :return: opencv image
        """
        if base64_string.startswith("data:image"):
            base64_string = CommonImgHelper.base64_filter(base64_string)
        img_data = base64.b64decode(base64_string)

        ny = np.fromstring(img_data, np.uint8)
        dst = cv2.imdecode(ny, flag)
        dst = np.array(dst)

        return dst

    @staticmethod
    def base64_to_pilimg(base64_str):
        return PILImage.open(io.BytesIO(CommonImgHelper.base64_to_bytes(base64_str)))

    @staticmethod
    def base64_filter(base64_string):
        u"""
        过滤base64数据为可用
        :param base64_string: string
        :return: string
        """
        if base64_string.startswith('data:'):
            params, data = base64_string.split(',', 1)
            return data
        else:
            return base64_string

    @staticmethod
    def cv2_to_base64(dst_img, with_head=True, filetype='jpg'):
        """
        将矩阵图片数据转为base64
        :param dst_img:
        :param with_head:
        :param filetype: 文件类型
        :return:
        """
        cnt = cv2.imencode('.%s' % filetype, dst_img)[1]
        dst_base64 = base64.b64encode(cnt).decode('utf-8')
        if with_head:
            return "data:image/%s;base64,%s" % (filetype, dst_base64)

        return dst_base64

    @staticmethod
    def pil_to_base64(pil_img, with_head=True, filetype='JPEG'):
        output_buffer = BytesIO()
        pil_img.save(output_buffer, format=filetype)
        byte_data = output_buffer.getvalue()
        return CommonImgHelper.bytes_to_base64(byte_data, with_head, filetype)

    @staticmethod
    def bytes_to_base64(img_bytes, with_head=True, filetype='jpeg'):
        """将字节流图片数据转换为base64数据"""
        if with_head:
            return ("data:image/%s;base64," % filetype) + base64.b64encode(img_bytes).decode('utf-8')
        else:
            return base64.b64encode(img_bytes).decode('utf-8')

    @staticmethod
    def get_base64_by_image_id(image_id, with_head=True):
        """通过Image.id返回图片的base64数据"""
        img_bytes = CommonImgHelper.get_bytes_img_by_image_id(image_id)
        return CommonImgHelper.bytes_to_base64(img_bytes, with_head)

    @staticmethod
    def stick_jpg_img(bg_img, img, x, y, with_base64=False):
        """将非透明 img 粘贴到原图
        
        :param bg_img: 要粘贴的背景图
        :param img: 要粘贴的图
        :param x: 在原图的 left_top_x
        :param y: 在原图的 left_top_y
        :param with_base64: 传入的 img 是否为 base64 格式
        :return: 
        """
        if with_base64:
            img = CommonImgHelper.base64_to_cv2img(img, cv2.IMREAD_COLOR)
        height, width, channel_num = img.shape
        if channel_num == 4:
            img = CommonImgHelper.channel4to3(img)
        left, top = int(x), int(y)
        right = left + width if left + width <= bg_img.shape[1] else bg_img.shape[1]
        bottom = top + height if top + height <= bg_img.shape[0] else bg_img.shape[0]

        bg_img[top:bottom, left:right] = img[0:bottom-top, 0:right-left]
        return bg_img

    @staticmethod
    def stick_png_img(bg_img, img, x, y, with_base64=False):
        """将 png 粘贴到原图(jpg)"""
        if with_base64:
            img = CommonImgHelper.base64_to_cv2img(img)
        # 判断 jpg 图像是否已经为4通道
        if bg_img.shape[2] == 3:
            bg_img = CommonImgHelper.add_alpha_channel(bg_img)

        # 当叠加图像时，可能因为叠加位置设置不当，导致png图像的边界超过背景jpg图像，而程序报错
        # 这里设定一系列叠加位置的限制，可以满足png图像超出jpg图像范围时，依然可以正常叠加
        height, width = img.shape[0], img.shape[1]
        # 在背景图上贴图的区域坐标
        left, top = int(x), int(y)
        right = left + width if left + width <= bg_img.shape[1] else bg_img.shape[1]
        bottom = top + height if top + height <= bg_img.shape[0] else bg_img.shape[0]

        # 获取要覆盖图像的alpha值，将像素值除以255，使值保持在0-1之间
        alpha_png = img[0:bottom-top, 0:right-left, 3] / 255.0
        alpha_jpg = 1 - alpha_png

        # 开始叠加
        for c in range(0, 3):
            bg_img[top:bottom, left:right, c] = (
                (alpha_jpg * bg_img[top:bottom, left:right, c]) + (alpha_png * img[0:bottom-top, 0:right-left, c]))

        return bg_img

    @staticmethod
    def order_points(pts):
        # pts为轮廓坐标
        # 列表中存储元素分别为左上角，右上角，右下角和左下角
        rect = np.zeros((4, 2), dtype="float32")
        # 左上角的点具有最小的和，而右下角的点具有最大的和
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        # 计算点之间的差值
        # 右上角的点具有最小的差值,
        # 左下角的点具有最大的差值
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # 返回排序坐标(依次为左上右上右下左下)
        return rect

    @staticmethod
    def inscribed_rect(cnt):
        rect = CommonImgHelper.order_points(cnt.reshape(cnt.shape[0], 2))
        xs = sorted([i[0] for i in rect])
        ys = sorted([i[1] for i in rect])
        # 内接矩形的坐标为
        return map(decimal.Decimal, [xs[1].item(), ys[1].item(), (xs[2] - xs[1]).item(), (ys[2] - ys[1]).item()])

    @staticmethod
    def inscribed_rect_v2(cont):
        """绘制不规则最大内接正矩形"""
        x, y, w, h = cv2.boundingRect(cont)
        cX, cY, x_min, x_max, y_min, y_max = x + w / 2, y + h / 2, x, x + w, y, y + h
        c = cont  # 单个轮廓
        range_x, range_y = x_max - x_min, y_max - y_min  # 轮廓的X，Y的范围
        x1, x2, y1, y2 = cX, cX, cY, cY  # 中心扩散矩形的四个顶点x,y
        cnt_range, radio = 0, 0
        shape_flag = 1  # 1：轮廓X轴方向比Y长；0：轮廓Y轴方向比X长
        if range_x > range_y:  # 判断轮廓 X方向更长
            radio, shape_flag = int(range_x / range_y), 1
            range_x_left = cX - x_min
            range_x_right = x_max - cX
            if range_x_left >= range_x_right:  # 取轴更长范围作for循环
                cnt_range = int(range_x_left)
            if range_x_left < range_x_right:
                cnt_range = int(range_x_right)
        else:  # 判断轮廓 Y方向更长
            radio, shape_flag = int(range_y / range_x), 0
            range_y_top = cY - y_min
            range_y_bottom = y_max - cY
            if range_y_top >= range_y_bottom:  # 取轴更长范围作for循环
                cnt_range = int(range_y_top)
            if range_y_top < range_y_bottom:
                cnt_range = int(range_y_bottom)
        # print("X radio Y: %d " % radio)
        # print("---------new drawing range: %d-------------------------------------" % cnt_range)
        flag_x1, flag_x2, flag_y1, flag_y2 = False, False, False, False
        radio = 3  # 暂时设5，统一比例X:Y=5:1 因为发现某些会出现X:Y=4:1, 某些会出现X:Y=5:1
        if shape_flag == 1:
            radio_x = radio - 1
            radio_y = 1
        else:
            radio_x = 1
            radio_y = radio - 1
        for ix in range(1, cnt_range, 1):  # X方向延展，假设X:Y=3:1，那延展步进值X:Y=3:1
            # 第二象限延展
            if flag_y1 == False:
                y1 -= 1 * radio_y  # 假设X:Y=1:1，轮廓XY方向长度接近，可理解为延展步进X:Y=1:1
                p_x1y1 = cv2.pointPolygonTest(c, (x1, y1), False)
                p_x2y1 = cv2.pointPolygonTest(c, (x2, y1), False)
                if p_x1y1 <= 0 or y1 <= y_min or p_x2y1 <= 0:  # 在轮廓外，只进行y运算，说明y超出范围
                    for count in range(0, radio_y - 1, 1):  # 最长返回步进延展
                        y1 += 1  # y超出, 步进返回
                        p_x1y1 = cv2.pointPolygonTest(c, (x1, y1), False)
                        if p_x1y1 <= 0 or y1 <= y_min or p_x2y1 <= 0:
                            pass
                        else:
                            break
                    # print("y1 = %d, P=%d" % (y1, p_x1y1))
                    flag_y1 = True

            if flag_x1 == False:
                x1 -= 1 * radio_x
                p_x1y1 = cv2.pointPolygonTest(c, (x1, y1), False)  # 满足第二象限的要求，像素都在轮廓内
                p_x1y2 = cv2.pointPolygonTest(c, (x1, y2), False)  # 满足第三象限的要求，像素都在轮廓内
                if p_x1y1 <= 0 or x1 <= x_min or p_x1y2 <= 0:  # 若X超出轮廓范围
                    # x1 += 1  # x超出, 返回原点
                    for count in range(0, radio_x - 1, 1):  #
                        x1 += 1  # x超出, 步进返回
                        p_x1y1 = cv2.pointPolygonTest(c, (x1, y1), False)  # 满足第二象限的要求，像素都在轮廓内
                        p_x1y2 = cv2.pointPolygonTest(c, (x1, y2), False)  # 满足第三象限的要求，像素都在轮廓内
                        if p_x1y1 <= 0 or x1 <= x_min or p_x1y2 <= 0:
                            pass
                        else:
                            break
                    # print("x1 = %d, P=%d" % (x1, p_x1y1))
                    flag_x1 = True  # X轴像左延展达到轮廓边界，标志=True
            # 第三象限延展
            if flag_y2 == False:
                y2 += 1 * radio_y
                p_x1y2 = cv2.pointPolygonTest(c, (x1, y2), False)
                p_x2y2 = cv2.pointPolygonTest(c, (x2, y2), False)
                if p_x1y2 <= 0 or y2 >= y_max or p_x2y2 <= 0:  # 在轮廓外，只进行y运算，说明y超出范围
                    for count in range(0, radio_y - 1, 1):  # 最长返回步进延展
                        y2 -= 1  # y超出, 返回原点
                        p_x1y2 = cv2.pointPolygonTest(c, (x1, y2), False)
                        if p_x1y2 <= 0 or y2 >= y_max or p_x2y2 <= 0:  # 在轮廓外，只进行y运算，说明y超出范围
                            pass
                        else:
                            break
                    # print("y2 = %d, P=%d" % (y2, p_x1y2))
                    flag_y2 = True  # Y轴像左延展达到轮廓边界，标志=True
            # 第一象限延展
            if flag_x2 == False:
                x2 += 1 * radio_x
                p_x2y1 = cv2.pointPolygonTest(c, (x2, y1), False)  # 满足第一象限的要求，像素都在轮廓内
                p_x2y2 = cv2.pointPolygonTest(c, (x2, y2), False)  # 满足第四象限的要求，像素都在轮廓内
                if p_x2y1 <= 0 or x2 >= x_max or p_x2y2 <= 0:
                    for count in range(0, radio_x - 1, 1):  # 最长返回步进延展
                        x2 -= 1  # x超出, 返回原点
                        p_x2y1 = cv2.pointPolygonTest(c, (x2, y1), False)  # 满足第一象限的要求，像素都在轮廓内
                        p_x2y2 = cv2.pointPolygonTest(c, (x2, y2), False)  # 满足第四象限的要求，像素都在轮廓内
                        if p_x2y1 <= 0 or x2 >= x_max or p_x2y2 <= 0:
                            pass
                        elif p_x2y2 > 0:
                            break
                    # print("x2 = %d, P=%d" % (x2, p_x2y1))
                    flag_x2 = True
            if flag_y1 and flag_x1 and flag_y2 and flag_x2:
                # print("(x1,y1)=(%d,%d)" % (x1, y1))
                # print("(x2,y2)=(%d,%d)" % (x2, y2))
                break

        return map(decimal.Decimal, [x1, y1, abs(x2-x1), abs(y2-y1)])

    @staticmethod
    def add_alpha_channel(img):
        """为jpg图像添加alpha通道

        :param img: cv2 格式的图片
        :return: 添加透明通道的图
        """
        b_channel, g_channel, r_channel = cv2.split(img)  # 剥离jpg图像通道
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255  # 创建Alpha通道
        img_new = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))  # 融合通道

        return img_new

    @staticmethod
    def channel4to3(img):
        """4通道转3通道"""
        b, g, r, a = cv2.split(img)
        return cv2.merge((b, g, r))

    @staticmethod
    def make_img_bytes_to_io_bytes(img_bytes):
        """将图片流保存在io流中，并返回io流"""
        pil_img = PILImage.open(BytesIO(img_bytes))
        byte_io = BytesIO()
        pil_img.convert('RGB').save(byte_io, 'JPEG')
        byte_io.seek(0)
        return byte_io

    @staticmethod
    def write_local(filename, cv2img, output_path='/data/images/'):
        """将图片写入本地"""
        filename = os.path.join(output_path, filename)
        cv2.imwrite(filename, cv2img)

    @staticmethod
    def secure_ori_words_xy(ori_words_x, ori_words_y):
        """返回安全的原词坐标"""
        secure_x = ori_words_x if ori_words_x > 1 else 0
        secure_y = ori_words_y if ori_words_y > 1 else 0
        return secure_x, secure_y

    @staticmethod
    def rm_base64_head(img_base64: str) -> str:
        """移除图片base64头"""
        return (img_base64.split(',', maxsplit=1)[-1]
                if img_base64.startswith('data:image')
                else img_base64)

    @staticmethod
    def overlying_white_bg(img_cv2):
        """为图像叠加白色背景"""
        rows, cols, channels = img_cv2.shape
        for i in range(rows):
            for j in range(cols):
                if np.all(img_cv2[i][j] == 0):
                    img_cv2[i][j] = [255] * 4
        return img_cv2

    @staticmethod
    def get_threshold_mask(img_base64: str) -> str:
        """
        将base64透明部分置黑，其余为白
        @param img_base64:
        @return:
        """
        dst = CommonImgHelper.base64_to_cv2img(img_base64)
        # 转为灰度图
        gray = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)
        # 二值化
        ret, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)
        mask_base64 = CommonImgHelper.cv2_to_base64(binary, with_head=True)
        return mask_base64

    @staticmethod
    def get_cv2_img_by_url(url: str) -> np.ndarray:
        """将图片url数据转为cv2格式数据并返回"""
        resp = requests.get(url)
        return CommonImgHelper.bytes_to_cv2(resp.content)

    @staticmethod
    def pil_to_cv2(pil_img):
        return cv2.cvtColor(np.asarray(pil_img), cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(cv2_img, flags=cv2.COLOR_BGR2RGB):
        return PILImage.fromarray(cv2.cvtColor(cv2_img, flags))

    @staticmethod
    def rgb_to_hex(rgb):
        color = '#'
        for i in rgb:
            color += str(hex(int(i)))[-2:].replace('x', '0').upper()

        return color

    @staticmethod
    def extract_img_to_alpha(cv2_img, mask):
        """将mask区域图像抠到透明底图上"""
        # 3通道图增加第4通道
        if cv2_img.shape[2] != 4:
            cv2_img = CommonImgHelper.add_alpha_channel(cv2_img)

        for x in range(mask.shape[0]):
            for y in range(mask.shape[1]):
                if mask[x][y] == 0:
                    cv2_img[x][y][3] = 0

        return cv2_img


def get_adapted_picture_from_dir(base_dir, filename):
    """从 base_dir 下找到与 filename（不包含后缀）同名的图片，
    若存在则返回绝对路径，否则返回 None"""
    _file_path = os.path.join(base_dir, filename)
    possible_ext = current_app.config['POSSIBLE_PICTURE_EXT']
    file_path = _file_path
    if not os.path.exists(_file_path):
        for ext in possible_ext:
            file_path = '%s.%s' % (_file_path, ext)
            if os.path.exists(file_path):
                break
        else:
            return None

    return file_path


def get_adapted_rubbing_picture(zhu_lu_name: str) -> list:
    ret = []
    head, tail = zhu_lu_name.split('·')
    head = head[2:]
    base_filename = '%s册_%s' % (head, str(int(tail)))

    file_path = get_adapted_picture_from_dir(current_app.config['TA_PIAN_BASE_DIR'], base_filename)

    if file_path is not None:
        ret.append(file_path)
        return ret

    index = 1
    filename = '%s.%s' % (base_filename, index)
    file_path = get_adapted_picture_from_dir(current_app.config['TA_PIAN_BASE_DIR'], filename)

    while file_path is not None:
        ret.append(file_path)
        index += 1
        filename = '%s.%s' % (base_filename, index)
        file_path = get_adapted_picture_from_dir(current_app.config['TA_PIAN_BASE_DIR'], filename)

    if len(ret) > 0:
        return ret

    for item in ['A', 'B', 'C', 'D', 'E']:
        filename = '%s.%s' % (base_filename, item)
        file_path = get_adapted_picture_from_dir(current_app.config['TA_PIAN_BASE_DIR'], filename)
        if file_path is not None:
            ret.append(file_path)
        else:
            break

    return ret


if __name__ == '__main__':
    ori_img = cv2.imread(r'C:\Users\wy\Desktop\617a3a2bb435b-b.png', cv2.IMREAD_UNCHANGED)
    res_img = CommonImgHelper.overlying_white_bg(ori_img)
    cv2.imwrite('res_img.png', res_img)
