
import matplotlib.pyplot as plt

import argparse
import cv2
import numpy as np
import os
import glob
from os.path import basename

import pymongo
from pymongo import MongoClient

from hogcompute import HOGCom 
from colorcompute import ColorCom

ap = argparse.ArgumentParser()
ap.add_argument("-i", 
	help="path to the input image");
ap.add_argument("-d", 
	help="path to the input file");
args = vars(ap.parse_args())
imgdir = args['i']
imgFileDir = args['d'];

#connect MongoDB
_dbIp = 'localhost'
_conn = MongoClient(_dbIp, 27017)
_db = _conn['ImageDB']
_collection = _db['proimg']

_colorCom = ColorCom();
_hogCom = HOGCom();

if imgdir != None:
	_colorCom.compute_saveDB(imgdir, _collection);
	_hogCom.compute_saveDB(imgdir, _collection);

	# saveColorHis(imgdir)

if imgFileDir != None:
	fileList = glob.glob(imgFileDir + '/*.png');
	for imgdir in fileList:			
		# filebasename = basename(filename)
		print('file name ', imgdir);
		_colorCom.compute_saveDB(imgdir, _collection);
		_hogCom.compute_saveDB(imgdir, _collection);
		# saveColorHis(filename)		
		# print(filebasename);


# print('top ', list(z))  

# fig1 = plt.figure()
# ax = fig1.add_subplot(111)
# hist1D.plot(ax)
# fig2 = plt.figure()
# ax_L = fig2.add_subplot(111)
# hist1D_L.plot(ax_L)
# plt.show()