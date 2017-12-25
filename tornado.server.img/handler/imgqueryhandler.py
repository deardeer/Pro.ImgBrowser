import tornado.web
from tornado.options import options

import pymongo
from pymongo import MongoClient

import json

from db.save import ImgDB
import math
import numpy as np

_proImgDB = ImgDB();
_proImgDB.connectDB('ImageDB', 'localhost', 27017);

#test
testConn = MongoClient('localhost', 27017);
testDB = testConn['ImageDB']
testColl = testDB['proimg']
testRecord = testColl.find_one({'imgName': '1.png'});
#get color
liMainColor = testRecord['mainColor']
lireferColor = [[20,30,50], [4,2,29]];
length = len(lireferColor)
if(len(lireferColor) > len(liMainColor)):
	length = len(liMainColor)
lireferColor = lireferColor[:length]
liMainColor = liMainColor[:length];


# class LoadProImgHandler(tornado.web.RequestHandler):
# 	def post(self):
# 		self.set_header('Access-Control-Allow-Origin', "*")
# 		liAllRecord = _proImgDB.fetchAllRecords('proimg');
# 		liImg = [];	
# 		for record in liAllRecord:
# 			imgName = record['imgName']			
# 			liImg.append({

# 				})

class QuerybyImageColor(tornado.web.RequestHandler):
	def post(self):
		self.set_header('Access-Control-Allow-Origin', "*")
		print('query image');

		liAllRecord = _proImgDB.fetchAllRecords('proimg');
		liImg = [];	
            
		for record in liAllRecord:
			imgName = record['imgName']
			liMainColor = record['mainColor'];
			imgDir = self.static_url('proimg/' + imgName)
			liImg.append({
				'imgName': imgName,
				'imgDir': imgDir,
				'mainColor': liMainColor,
			});
		#get the image by color		
		# for color in liColor:
		# 	print('color ', color, type(color));
		result = {
		'imgList': liImg
		}
		self.write(result);

	# def transferRGB2HSV(self, liDensityRGB):
	# 	liDensityHSV = []
	# 	for index in range(0, len(liDensityRGB)):
	# 		DC = liDensityRGB[index]
	# 		density = DC[0]
	# 		rgb = DC[1]
	# 		hsv = 
	# 		liDensityHSV.append(hsv)
	# 	return liDensityHSV

	def getColorDistance(self, lireferColor, record):
		liMainColor = record['mainColor']
		weightSum = 0.;	

		length = len(lireferColor)
		if(len(lireferColor) > len(liMainColor)):
			length = len(liMainColor);

		for index in range(0, length):
			DC = liMainColor[index]
			density = DC[0]
			referColor = np.array(lireferColor[index])
			mainColor = np.array(DC[1], dtype=int)
			# print('maincolor ', mainColor, referColor)
			weightSum += density * math.sqrt(sum([i ** 2 for i in referColor - mainColor]))
			
		print('mainColor weightSum', weightSum);
		return weightSum;