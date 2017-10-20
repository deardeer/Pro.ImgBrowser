#!/usr/bin/env python
#coding:utf-8

import sys
# from imp import reload
# reload(sys)
# sys.setdefaultencoding('utf-8')

from handler.imgdbhandler import LoadImgDBHandler

url=[
    (r'/fetchImgs', LoadImgDBHandler),
]