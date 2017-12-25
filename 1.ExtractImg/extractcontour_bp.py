import cv2
import math
import numpy as np
import random

def bgr2hsv(r, g, b):
	color_bgr = np.uint8([[[b, g, r]]])
	color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV);
	return color_hsv;

def disBetweenHSV(hsv1, hsv2):
	dh = min(abs(hsv1[0] - hsv2[0]), 360 - abs(hsv1[0] - hsv2[0]))/180.;
	return dh;

def disBetweenBGR(bgr1, bgr2):
	return math.sqrt((bgr1[0] - bgr2[0])*(bgr1[0] - bgr2[0]) + (bgr1[1] - bgr2[1])*(bgr1[1] - bgr2[1]) + (bgr1[2] - bgr2[2])*(bgr1[2] - bgr2[2]))

def isColorExist(color, liColor):
	disThred = 70;#math.sqrt(20*20*3);
	liDis = []
	minDis = math.sqrt(255*255*3)
	minColor = [];
	for index in range(0, len(liColor)):
		referColor = liColor[index];
		dis = disBetweenBGR(color, referColor);
		if(dis < disThred):
			return True;
		elif(dis < minDis):
			minColor = referColor;
			minDis = dis;
	# print('Diff ', minDis, color, minColor);
	return False;

def isContourExist(contour, liContour):
	similarThred = 0.01;
	minSimilar = 1;
	for index in range(0, len(liContour)):
		referContour = liContour[index];
		similar = cv2.matchShapes(contour, referContour, 1, 0.0);
		if(similar < similarThred):
			return True;
		elif(minSimilar > similar):
			minSimilar = similar;
	print(' min Similar = ', minSimilar);
	return False;

#find mask by color
def findMask(img, r, g, b):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
	dri = 40;
	avg_color = bgr2hsv(r, g, b).tolist()[0][0];
	low_color = np.array([avg_color[0] - dri, avg_color[1] - dri, avg_color[2] - dri])#bgr2hsv(13,115,178)
	high_color = np.array([avg_color[0] + dri, avg_color[1] + dri, avg_color[2] + dri])#bgr2hsv(16,113,174);
	mask = cv2.inRange(hsv, low_color, high_color);
	# add the mask to original img
	# res = cv2.bitwise_and(img, img, mask=mask)
	return mask

def findContour(img):
	newimg, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	return contours;

def extractContours(img, originimg):
	h, w, channels = img.shape;

	liContourColor = [
	[255, 0, 0],
	[0, 255, 0],
	[0, 0, 255],
	[255, 255, 0],
	[0, 255, 255],
	[255, 0, 255],
	[155, 155, 0],
	[0, 155, 155],
	[155, 0, 155],
	];
	#sample 100 times
	maxSampleTime = 500;
	sampleTime = 0
	liColor = [];
	liContour = [];	
	while(1):
		if(sampleTime >= maxSampleTime):
			break;
		x_random = math.floor(random.uniform(0, 1) * w);
		y_random = math.floor(random.uniform(0, 1) * h);
		#random sample, color
		bgr = img[y_random, x_random].tolist();
		if(isColorExist(bgr, liColor) == False):
			#find the object with color
			liColor.append(bgr);
			mask = findMask(img, bgr[2], bgr[1], bgr[0]);
			contours = findContour(mask);
			contours_new = [];
			#check for similar contour
			for temp_index in range(0, len(contours)):
				temp_contour = contours[temp_index];
				if(isContourExist(temp_contour, liContour) == False):
					contours_new.append(temp_contour);
					liContour.append(temp_contour);
				else:
					print('index = ', len(liColor), ' Contour Exist!');
			# draw contours
			if(len(contours_new) > 0):
				cv2.drawContours(originimg, contours_new, -1, liContourColor[len(liColor)%len(liContourColor)], 2)
				print('draw index = ', len(liColor), ' contour = ', len(contours_new));
			cv2.circle(originimg, (x_random, y_random), 2, (0,0,0), -1);
			font = cv2.FONT_HERSHEY_SIMPLEX
			# cv2.putText(originimg, str(len(liColor)), (x_random,y_random), font, 1, liContourColor[len(liColor)%len(liContourColor)], 2, cv2.LINE_AA)
		#check if exist	
		sampleTime = sampleTime + 1;
	return liContour;

imgscr = 'img/14.png'
originimg = cv2.imread(imgscr);
img = cv2.imread(imgscr);
# h, w, channels = img.shape;
# print(h, w);

#smoothing
img = cv2.bilateralFilter(img, 9, 100, 75)
liContour = extractContours(img, originimg);
print(' Extract #Contour = ', len(liContour));
# for index in range(0, len(liContour)):
# 	cv2.drawContours(originimg, liContour[index], -1, liContourColor[index%len(liContourColor)], 2);

# kernel = np.ones((5,5), np.float32)/25
# img = cv2.filter2D(img,-1,kernel)




#show the image
cv2.imshow('img', originimg);
cv2.waitKey(0)
cv2.destroyAllWindows();