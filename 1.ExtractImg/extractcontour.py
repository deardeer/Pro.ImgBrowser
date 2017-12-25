import argparse
import imutils
import cv2
import ShapeDetector as SD
import ColorLabel as CL
import numpy as np

def getBackgroundGray(img):
	return img[0, 1];

sd = SD.ShapeDetector()
cl = CL.ColorLabeler()

def extractHarrisPoints(imgDir):
	image = cv2.imread(imgDir);
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = np.float32(gray)

	corners = cv2.goodFeaturesToTrack(gray, 100, 0.01, 10)
	# dst = cv2.dilate(dst, None)
	corners = np.int0(corners)
	liXY = []
	for i in corners:
		x, y = i.ravel()
		liXY.append([x,y])
		# cv2.circle(image, (x, y), 3, 255, -1)
	return liXY
	# image[dst > 0.01  * dst.max()] = [0, 0, 255]

def extractContours(imgDir):
	#load the image
	image = cv2.imread(imgDir)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = gray
	# blurred = cv2.GaussianBlur(gray, (3,3), 0)

	imgLab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

	#get the background gray
	bgGray = getBackgroundGray(blurred)
	print('Gray ', bgGray)
	if(bgGray < 128):
		#more black
		bgGray = bgGray + 10;
		thresh = cv2.threshold(blurred, bgGray, 255, cv2.THRESH_BINARY)[1]
	else:
		#more white
		bgGray = bgGray - 10;
		thresh = cv2.threshold(blurred, bgGray, 255, cv2.THRESH_BINARY_INV)[1]
	# bilateralFilter = cv2.bilateralFilter(image, 9, 75, 75)

	newimg, cnts, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);

	
	# cv2.imshow('gray', gray)
	return cnts