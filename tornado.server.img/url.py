#!/usr/bin/env python
#coding:utf-8

import sys

from handler.imgdbhandler import IndexHandler
from handler.imgdbhandler import LoadImgDBHandler
from handler.imgdbhandler import LoadProImgDBHandler
from handler.imgdbhandler import GetImgProInfo
from handler.imgdbhandler import DeleteImgDBHandler
from handler.imgdbhandler import CropImgDBHandler

# from handler.imgqueryhandler import LoadProImgHandler
from handler.imgqueryhandler import QuerybyImageColor

url=[
	(r'/', IndexHandler),
    
    (r'/fetchImgs', LoadImgDBHandler),
    (r'/fetchProImgs', LoadProImgDBHandler),

    (r'/getProInfo', GetImgProInfo),

    (r'/deleteImg', DeleteImgDBHandler),
    (r'/cropImg', CropImgDBHandler),

    #query
    (r'/loadProImgs', QuerybyImageColor),
    # (r'/query_image_color', QuerybyImageColor),
    # (r'/img/(\w+)', ShowCropHandler),
    # (r'/img2/(\w+)', ShowCropHandler2),
]