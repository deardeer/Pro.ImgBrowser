#!/usr/bin/env python
#coding:utf-8

import sys

from handler.imgdbhandler import IndexHandler
from handler.imgdbhandler import LoadImgDBHandler

url=[
	(r'/', IndexHandler),
    (r'/fetchImgs', LoadImgDBHandler),
]