
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
imgDB.connectDB('ImageDB', 'localhost', 27017);

class IndexHandler(tornado.web.RequestHandler):     
    def get(self):
        #print("index handler")
        # self.render(("index.html"))
        self.render(("index.html")) #, paperNum= paperCollection.count(), papers=papers)
	

class LoadImgDBHandler(tornado.web.RequestHandler):
    
    def post(self):
        liImg = [];
        liImgRecord = imgDB.fetchRecords('rawimg', int(self.get_argument('beginIndex')), int(self.get_argument('endIndex')));
        for record in liImgRecord:
            imgName = record['imgName']
            crop = record['crop']
            imgDir = self.static_url('img/' + imgName)
            liImg.append({
                'imgName': imgName,
                'imgDir': imgDir,
                'crop': crop,
                'imgPro': False
                });
        result = {
        'imgList': liImg
        }
        self.set_header('Access-Control-Allow-Origin', '*');
        self.write(result);

class LoadProImgDBHandler(tornado.web.RequestHandler):
    def post(self):
        print('load pro img');
        liImg = [];
        liImgRecord = imgDB.fetchRecords('proimg', int(self.get_argument('beginIndex')), int(self.get_argument('endIndex')));
        for record in liImgRecord:
            imgName = record['imgName']
            imgDir = self.static_url('proimg/' + imgName)
            liImg.append({
                'imgName': imgName,
                'imgDir': imgDir,
                'imgPro': True,
                });
        result = {
        'imgList': liImg
        }
        self.set_header('Access-Control-Allow-Origin', '*');
        self.write(result);

class GetImgProInfo(tornado.web.RequestHandler):
    def post(self):
        result = {}
        print('Get Img Pro Info');
        imgName = self.get_argument('imgName');
        #get the meta data        
        imgProInfo = imgDB.getProInfo('proimg', imgName);
        print(imgProInfo['contours']);
        result={
            'contours': imgProInfo['contours']
        }
        # for key in imgProInfo:
        self.write(result);

class DeleteImgDBHandler(tornado.web.RequestHandler):
    def post(self):
        imgName = self.get_argument('imgName');
        imgDB.deleteRecord('rawimg', 'imgName', imgName);
        self.write({'imgName': imgName});


class CropImgDBHandler(tornado.web.RequestHandler):
    def post(self):
        imgName = self.get_argument('imgName');
        imgCrop = self.get_argument('crop');
        imgDB.setCrop('rawimg', 'imgName', imgName, imgCrop);
        self.write({'imgName': imgName});



# class ShowCropHandler(tornado.web.RequestHandler):
#     def get(self, para):
#         print(' here ? ', para);
#         self.write('ok');
        # self.render()
