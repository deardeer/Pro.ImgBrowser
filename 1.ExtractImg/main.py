import argparse
import imutils
import cv2
import extractcontour
import ComCntAtt
import pandas as pd 

import ColorLabel as CL 
import ShapeDetector as SD
cl = CL.ColorLabeler()
sd = SD.ShapeDetector();

def getBackgroundGray(img):
	#get the [0, 3]
	return img[0, 1];

ap = argparse.ArgumentParser()
ap.add_argument("-i", required=True,
	help="path to the input image");
args = vars(ap.parse_args())

#load the image
imgdir = args['i']
cnts = extractcontour.extractContours(imgdir)

# liXY = extractcontour.extractHarrisPoints(imgdir)
image = cv2.imread(imgdir)
imgLab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

#draw contour & feature points
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

liShape = ['rect', 'circle', 'v-line', 'h-line', 'path'];
index = 0
for temp_index in range(0, len(cnts)):
	c = cnts[temp_index];
	M = cv2.moments(c)
	if(M["m00"] != 0):
		color = cl.label(imgLab, c)
		rgbcolor = cl.computeMeanColor(image, c)
		shape = sd.detect(c);
		text = "{}".format(shape)
		if(shape=='rect'):
			cv2.drawContours(image, [c], -1, (0,255,0), 2); 
		else:
			cv2.drawContours(image, [c], -1, (0,0,0), 2); 
	index = index + 1

cv2.imshow('dst', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

#write to DataFrame
liCRow = []
for temp_index in range(0, len(cnts)):
	c = cnts[temp_index]
	M = cv2.moments(c)
	if(M["m00"] != 0):
		c_type = sd.detect(c);
		c_pointlist = c.flatten().tolist()
		c_attrs = ComCntAtt.computeAttr(c, image)
		row = {
			'c_type': c_type,
			'c_points': c_pointlist,
		}
		for attr in c_attrs:
			row[attr] = c_attrs[attr]
		liCRow.append(row)
df = pd.DataFrame(liCRow);
#write to csv
# print('./img/meta' + imgdir + '.txt');
df.to_csv(imgdir + '_meta.txt', index = None);

# print('extract contour #', len(cnts));

# image = cv2.imread(args['i'])
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# blurred = cv2.GaussianBlur(gray, (3,3), 0)
# #get the background gray
# bgGray = getBackgroundGray(blurred)
# print('Gray ', bgGray)
# if(bgGray < 128):
# 	#more black
# 	bgGray = bgGray + 10;
# 	thresh = cv2.threshold(blurred, bgGray, 255, cv2.THRESH_BINARY)[1]
# else:
# 	#more white
# 	bgGray = bgGray - 10;
# 	thresh = cv2.threshold(blurred, bgGray, 255, cv2.THRESH_BINARY_INV)[1]
# # bilateralFilter = cv2.bilateralFilter(image, 9, 75, 75)

# newimg, cnts, hierarchy  = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE);

# liContourColor = [
# 	[255, 0, 0],
# 	[0, 255, 0],
# 	[0, 0, 255],
# 	[255, 255, 0],
# 	[0, 255, 255],
# 	[255, 0, 255],
# 	[155, 155, 0],
# 	[0, 155, 155],
# 	[155, 0, 155],
# ];

# # cv2.drawContours(image, cnts, -1, (0,255,0), 3)

# print('Detect Contour # = ', len(cnts))

# index = 0
# for temp_index in range(0, len(cnts)):
# 	c = cnts[temp_index];
# 	cv2.drawContours(image, [c], -1, liContourColor[index%len(liContourColor)], 2);
# 	print('contour ', index, len(c));
# 	index = index + 1

# # cv2.imshow('gray', gray)
# cv2.imshow('origin', image)

# cv2.waitKey(0)
# cv2.destroyAllWindows()