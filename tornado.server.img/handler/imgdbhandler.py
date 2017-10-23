
import tornado.web
from tornado.options import options

import pymongo
from pymongo import MongoClient

from db.save import ImgDB

import setting

from PIL import Image
import io
import os.path

import json

import subprocess

imgDB = ImgDB();
imgDB.connectDB('localhost', 27017);

class IndexHandler(tornado.web.RequestHandler):     
    def get(self):
        #print("index handler")
        # self.render(("index.html"))
        self.render(("index.html")) #, paperNum= paperCollection.count(), papers=papers)
	


class LoadImgDBHandler(tornado.web.RequestHandler):
    def post1(self):
    	liImg = [];
    	liImgRecord = imgDB.fetchRecords(int(self.get_argument('beginIndex')), int(self.get_argument('endIndex')));


        # for record in liImgRecord:
        #     imgName = record['imgName'];
        #     crop = record['crop'];
    	# for record in liImgRecord:
     #        imgName = record['imgName']
     #        imgDir = self.static_url('img/' + imgName);
    	# 	liImg.append({'imgName': imgName,'imgDir': imgDir,'crop': crop})
        
     #    result = {
     #    'imgList': liImg
     #    }
    	# self.set_header("Access-Control-Allow-Origin", '*');
    	# self.write(result);
    def post(self):
        liImg = [];
        liImgRecord = imgDB.fetchRecords(int(self.get_argument('beginIndex')), int(self.get_argument('endIndex')));
        for record in liImgRecord:
            imgName = record['imgName']
            crop = record['crop']
            imgDir = self.static_url('img/' + imgName)
            liImg.append({
                'imgName': imgName,
                'imgDir': imgDir,
                'crop': crop
                });
        result = {
        'imgList': liImg
        }
        self.set_header('Access-Control-Allow-Origin', '*');
        self.write(result);
