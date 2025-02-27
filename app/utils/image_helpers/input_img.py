# -*- coding: utf-8 -*-
"""
  Created by 怀月 on 2021/12/17.
"""
import numpy as np

from app.utils.image_helpers.common_img_helper import CommonImgHelper


def load_image(base64_str, mode='RGB', return_orig=False):
    img = np.array(CommonImgHelper.base64_to_pilimg(base64_str).convert(mode))
    if img.ndim == 3:
        img = np.transpose(img, (2, 0, 1))
    out_img = img.astype('float32') / 255
    if return_orig:
        return out_img, img
    else:
        return out_img