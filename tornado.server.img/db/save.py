#give the dir, save images under dir to DB
import pymongo
from pymongo import MongoClient

import os
import glob
from os.path import basename

import pandas as pd

dbIP = 'localhost';

class ImgDB:
	def connectDB(self, dbname, dbip, port):
		self._conn = MongoClient(dbip, port)
		self._db = self._conn[dbname]

	def fetchAllRecords(self, collectionname):
		self._collection = self._db[collectionname];
		return self._collection.find();

	def fetchRecords(self, collectionname, beginIndex, endIndex):
		self._collection = self._db[collectionname];
		liImgRecord = self._collection.find({'index': {'$gte': beginIndex, '$lt': endIndex}});
		return liImgRecord;

	def setCrop(self, collectionname, key, value, crop):
		self._collection = self._db[collectionname];
		# print('set crop record ', key, value, crop);
		self._collection.update_one({key: value}, {'$set': {'crop': crop}});

	def deleteRecord(self, collectionname, key, value):
		print('delete record', key, value);
		self._collection = self._db[collectionname];
		self._collection.remove({key: value});

	def getProInfo(self, collectionname, imgName):
		self._collection = self._db[collectionname];
		imgRecord = self._collection.find_one({'imgName': imgName});
		return imgRecord;
   
#load raw imgs in dir to DB
def saveRawImgstoDB(dir):
	print('[saveRawImgstoDB] Begin ', dir);
	#connect to MongoDB
	conn = MongoClient(dbIP, 27017)
	#get the DB
	db = conn['ImageDB']
	collection = db['rawimg']

	#get the images in the dir
	fileList = glob.glob(dir + '/*');
	beginIndex = collection.find({}).count();
	for filename in fileList:			
		filename = basename(filename)		
		doc = collection.find_one({'imgName': filename});
		if(doc == None):
			print('save raw img to DB ', filename);
			collection.insert({
				'imgName': filename,
				'index': beginIndex,
				'crop': False});
			beginIndex += 1
	print('[saveRawImgstoDB] End');

#load processed imgs in dir to DB
def saveProImgstoDB(dir):
	print('[saveProImgstoDB] Begin ', dir);
	#connect to MongoDB
	conn = MongoClient(dbIP, 27017)
	#get the DB
	db = conn['ImageDB']
	collection = db['proimg']

	#get the images in the dir
	fileList = glob.glob(dir + '/*');
	beginIndex = collection.find({}).count();
	for filename in fileList:			
		filename = basename(filename)
		imagename = os.path.splitext(filename)[0]
		proInfoDir = (os.path.join(dir, '../proimgmeta/', imagename + '.txt'));
		doc = collection.find_one({'imgName': filename});
		if(doc == None):
			print('save processed img to DB ', filename);
			df = pd.read_csv(proInfoDir);
			#get the contour info
			liContours = [];
			for index, row in df.iterrows():				
				contour = df.iloc[index].to_json()
				liContours.append(contour);
			collection.insert({
				'imgName': filename,
				'index': beginIndex,
				'contours': liContours,
				});
			beginIndex += 1

	print('[saveProImgstoDB] End');

saveProImgstoDB("../../proimg")
