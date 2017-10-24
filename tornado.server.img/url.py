#!/usr/bin/env python
#coding:utf-8

import sys

from handler.imgdbhandler import IndexHandler
from handler.imgdbhandler import LoadImgDBHandler
from handler.imgdbhandler import DeleteImgDBHandler
from handler.imgdbhandler import CropImgDBHandler

url=[
	(r'/', IndexHandler),
    (r'/fetchImgs', LoadImgDBHandler),
    (r'/deleteImg', DeleteImgDBHandler),
    (r'/cropImg', CropImgDBHandler),
    # (r'/img/(\w+)', ShowCropHandler),
    # (r'/img2/(\w+)', ShowCropHandler2),
]