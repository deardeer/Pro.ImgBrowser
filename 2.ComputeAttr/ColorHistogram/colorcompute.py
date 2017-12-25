from color_histogram.maskbg import maskImgBG
from color_histogram.maskbg import getMask
from color_histogram.io_util.image import loadRGB
from color_histogram.io_util.image import loadRGB_lm
from color_histogram.core.hist_1d import Hist1D

import matplotlib.pyplot as plt
import os
import glob
from os.path import basename

class ColorCom:

	def compute_saveDB(self, imgDir, collection):

		filebasename = basename(imgDir)	
		print('[save color histogram] imgdir ', imgDir, filebasename);
	# maks bg
	# img_maskbg = maskImgBG('../../cropimg/10.png')
	# imgdir = '../../img/Abastract timeline infographic template.jpg'
		image_mask = maskImgBG(imgDir)
		# cv2.imshow('mask', image_mask)
		# cv2.waitKey(0)

		image = loadRGB_lm(image_mask);
		# print('image type ', type(image), image.shape);

		# 16 bins, Lab color space, target channel L ('Lab'[0])
		hist1D = Hist1D(image, num_bins=10, alpha=0, color_space='hsv', channel=0)
		hist1D_L = Hist1D(image, num_bins=100, alpha=0, color_space='Lab', channel=0)

		#get color and density list
		liColor, liDensity = hist1D.getTopColorDensity();
		# print('licolor ', liColor, 'liDensity ', liDensity);
		# X = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
		# Y = [ 0,   1,   1,    0,   1,   2,   2,   0,   1]
		liDensityColor = sorted(zip(liDensity,liColor), reverse= True)

		#save to db: update or add	
		beginIndex = collection.find({}).count();
		# print(' begin index ', beginIndex);
		doc = collection.find_one({'imgName': filebasename});
		if(doc == None):
			collection.insert({
					'imgName': filebasename,
					'mainColor': liDensityColor,
					# 'index': beginIndex,
					});
		else:
			collection.update_one(
				{
					'imgName': filebasename
					},
				{
					'$set':{
						'mainColor': liDensityColor
					}
				},
				upsert=False
			)
			
		print('ok')