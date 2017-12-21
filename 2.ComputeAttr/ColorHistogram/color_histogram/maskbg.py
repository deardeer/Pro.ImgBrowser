import cv2

def getBackgroundGray(img):
	#get the [0, 3]
	return img[5, 5];

def getBackgroundColor(img):
	return img[5, 5];

def maskImgBG(imgdir):		

	image = cv2.imread(imgdir)
	bg_color = getBackgroundColor(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	bgGray = getBackgroundGray(gray)
	if(bgGray < 128):
		#more black
		bgGray = bgGray + 10;
		thresh = cv2.threshold(gray, bgGray, 255, cv2.THRESH_BINARY)[1]	
		img_masked = cv2.bitwise_and(image, image, mask=thresh);
	else:
		#more white
		bgGray = bgGray - 10;
		thresh = cv2.threshold(gray, bgGray, 255, cv2.THRESH_BINARY_INV)[1]
		img_masked = cv2.bitwise_and(image, image, mask=thresh);
	thresh = thresh < 255
	image[thresh] = bg_color;
	return image

def getMask(imgdir):		

	image = cv2.imread(imgdir)
	bg_color = getBackgroundColor(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	bgGray = getBackgroundGray(gray)
	if(bgGray < 128):
		#more black
		bgGray = bgGray + 10;
		thresh = cv2.threshold(gray, bgGray, 255, cv2.THRESH_BINARY)[1]	
		# img_masked = cv2.bitwise_and(image, image, mask=thresh);
	else:
		#more white
		bgGray = bgGray - 10;
		thresh = cv2.threshold(gray, bgGray, 255, cv2.THRESH_BINARY_INV)[1]
		# img_masked = cv2.bitwise_and(image, image, mask=thresh);
	return thresh