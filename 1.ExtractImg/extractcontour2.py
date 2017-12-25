import argparse
import imutils
import cv2
import extractcontour
import ComCntAtt

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
liXY = extractcontour.extractHarrisPoints(imgdir)
print('liXY ', len(liXY), liXY[0])
image = cv2.imread(imgdir)
for temp_index in range(0, len(cnts)):
	c = cnts[temp_index]
	ComCntAtt.computeAttr(c, image)

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