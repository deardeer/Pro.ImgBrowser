#give the dir, save images under dir to DB
import pymongo
from pymongo import MongoClient

import os
import glob
from os.path import basename

dbIp = 'localhost';

#load raw imgs in dir to DB
def saveRawImgstoDB(dir):
	print('[saveRawImgstoDB] Begin ', dir);
	#connect to MongoDB
	conn = MongoClient(dbIp, 27017)
	#get the DB
	db = conn['ImageDB']
	collection = db['rawimg']

	#get the images in the dir
	fileList = glob.glob(dir);
	for filename in fileList:			
		filename = basename(filename)
		# imagename = fios.path.splitext(filename)
		doc = collection.find_one({'imgName': filename});
		if(doc == None):
			print('save raw img to DB ', filename);
			collection.insert({'imgName': filename});
	print('[saveRawImgstoDB] End');

saveRawImgstoDB("../img2/*")
