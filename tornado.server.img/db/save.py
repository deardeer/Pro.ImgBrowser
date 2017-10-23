#give the dir, save images under dir to DB
import pymongo
from pymongo import MongoClient

import os
import glob
from os.path import basename

dbIP = 'localhost';

class ImgDB:
	def connectDB(self, dbip, port):
		self._conn = MongoClient(dbip, port)
		self._db = self._conn['ImageDB']
		self._collection = self._db['rawimg'];
	def fetchRecords(self, beginIndex, endIndex):
		liImgRecord = self._collection.find({'index': {'$gte': beginIndex, '$lt': endIndex}});
		return liImgRecord;

#load raw imgs in dir to DB
def saveRawImgstoDB(dir):
	print('[saveRawImgstoDB] Begin ', dir);
	#connect to MongoDB
	conn = MongoClient(dbIP, 27017)
	#get the DB
	db = conn['ImageDB']
	collection = db['rawimg']

	#get the images in the dir
	fileList = glob.glob(dir);
	beginIndex = collection.find({}).count();
	for filename in fileList:			
		filename = basename(filename)
		# imagename = fios.path.splitext(filename)
		doc = collection.find_one({'imgName': filename});
		if(doc == None):
			print('save raw img to DB ', filename);
			collection.insert({
				'imgName': filename,
				'index': beginIndex,
				'crop': False});
			beginIndex += 1
	print('[saveRawImgstoDB] End');

saveRawImgstoDB("../../img/*")
