
import tornado.web
from tornado.options import options

import pymongo
from pymongo import MongoClient

import setting

from PIL import Image
import io
import os.path

import json

import subprocess

class LoadImgDBHandler(tornado.web.RequestHandler):
    def post(self):
        print('TEST! ', self.get_argument('fetchNum'));
        self.set_header("Access-Control-Allow-Origin", '*');
        result = {
        'world': 'hhh'
        }
        self.write(result);

