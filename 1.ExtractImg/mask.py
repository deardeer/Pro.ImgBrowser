import cv2
import numpy as np 
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn import metrics

def bgr2hsv(r,g,b):
	color_bgr = np.uint8([[[b,g,r]]])
	color_hsv = cv2.cvtColor(color_bgr, cv2.COLOR_BGR2HSV);
	return color_hsv;

#find mask by color
def findMask(img, r, g, b):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV);
	dri = 20;
	avg_color = bgr2hsv(r, g, b).tolist()[0][0];
	low_color = np.array([avg_color[0] - dri, avg_color[1] - dri, avg_color[2] - dri])#bgr2hsv(13,115,178)
	high_color = np.array([avg_color[0] + dri, avg_color[1] + dri, avg_color[2] + dri])#bgr2hsv(16,113,174);
	mask = cv2.inRange(hsv, low_color, high_color);
	# add the mask to original img
	# res = cv2.bitwise_and(img, img, mask=mask)
	return mask

def findContour(img):
	newimg, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	return contours;

def drawHist(img):
	hist = cv2.calcHist([img], [0], None, [256], [0, 256]);
	plt.hist(hist);
	plt.show();

def getPointListfromContour(contour):
	liPos = [];
	for index in range(0, len(contours)):
		print('contour ', index)
		contour = contours[index];
		for x in np.nditer(contour):
			liPos.append(x)
	return liPos

def computeCentroidofContour(contour):
	M = cv2.moments(contours[0])
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])
	return cx, cy

def computeBondaryBoxofContour(contour):
	x,y,w,h = cv2.boundingRect(contour)
	return x,y,w,h

def computeAspectRatio(contour):	
	x,y,w,h = cv2.boundingRect(contour)
	return float(w)/h;

# define criteria, number of clusters(K) and apply kmeans()
def KmeansColor(img, K):	
	Z = img.reshape((-1,3))
	# convert to np.float32
	Z = np.float32(Z)
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
	ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

	# Now convert back into uint8, and make original image
	center = np.uint8(center)
	res = center[label.flatten()]
	res2 = res.reshape((img.shape))
	return center, label, res2;

def centroid_histogram(labels):
	numLabels = np.arange(0, len(np.unique(labels)) + 1)
	(hist, _) = np.histogram(labels, bins = numLabels);
	#normalize the histogram, 
	hist = hist.astype('float');
	hist /= hist.sum()
	return hist;

# def computeExtentofContour(contour):
# 	area = cv2.contourArea(contour);
image = cv2.imread('img/12.png');
origin = cv2.imread('img/12.png');
image_gray = cv2.imread('img/13.png', cv2.IMREAD_GRAYSCALE);
cv2.imshow('gray', image_gray);

th2 = cv2.adaptiveThreshold(image_gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)
th3 = cv2.adaptiveThreshold(image_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,5,2)
liImg = [th2, th3]
for i in range(0, 2):
    plt.subplot(2,1,i+1),plt.imshow(liImg[i],'gray')
    plt.xticks([]),plt.yticks([])
plt.show()
# res_new = cv2.bitwise_and(origin,origin, mask=th3)

# plt.imshow(th2);
# plt.show();
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#resize it
h, w, _ = image.shape;
print('image size ', h, w);
# w_new = int( 200 * w/max(w, h) )
# h_new = int( 200 * h/max(w, h) )
# image = cv2.resize(image, (w_new, h_new));
cv2.imshow('origin', origin);
cv2.imshow('blur', image);
cv2.imshow('res_new', res_new);
# cv2.imshow('resize', image);

#### KMeans by Numpy ####
#reshape the image to be a list of pixles
# image_array = image.reshape(image.shape[0] * image.shape[1], 3);
# #cluster the pixels
# clt = KMeans(n_clusters=10)
# clt.fit(image_array);
# label = clt.labels_;
# center = clt.cluster_centers_;

#### KMeans by CV ####
center, label, res2 = KmeansColor(image, 8);

#finds how many pixels are in each cluster
hist = centroid_histogram(label);

cv2.imshow('flaten', res2);

#compute the silhouette score
# silhouette = metrics.silhouette_score(image_array, clt.labels_, metric="euclidean")
# print("SI", silhouette);


#sort the clusters according to how many pixels they have
zipped = zip(hist, center);
sorted_list = sorted(zip(hist, center), reverse=True, key=lambda x: x[0]);
hist, center = zip(*sorted_list);

liColor = [
[255, 0, 0],
[0, 255, 0],
[0, 0, 255]
];

# contours = findContour(res2);
# cv2.drawContours(origin, contours, -1, liColor[index%3], 1)
# cv2.imshow('mask' + str(index), neworigin);

contours_all = [];
for index in range(0, len(center)):	
	if(index != 1):
		continue;
	bgr = center[index];
	#find the contour for 
	neworigin = origin;
	mask = findMask(res2, bgr[2], bgr[1], bgr[0]);
	contours = findContour(mask);	
	print('Top ', index, ' #=', hist[index], ' Color ', bgr, ' Contour#=', len(contours));	
	cv2.drawContours(neworigin, contours, -1, liColor[index%3], 1)
cv2.imshow('mask' + str(index), neworigin);

	# print('color ', index, clt.cluster_centers_[index]);

# print('hist ', hist)
# print('cluster center ', clt.cluster_centers_);



# print(hist);
# zipped.sort(reverse=True, key=lambda x: x[0])


# labels = dbScan(img);

# rows, cols, chs = img.shape;
# print(' row col ', rows, cols, chs);

# center, label, kmeansimg = KmeansColor(img);
# # new_kmeansimg = kmeansimg;

# green = 20;
# for index in range(0, len(center)):
# 	bgr = center[index];
# 	print('color ', bgr[0], bgr[1], bgr[2]);
# 	# licolor = img[bgr[0], bgr[1], bgr[2]];
# 	# plt.plot(histr, color='r')
# 	# plt.show();	
# 	#find the mask of different center
# 	mask = findMask(kmeansimg, bgr[2], bgr[1], bgr[0]);
# 	contours = findContour(mask);
# 	print('cluster ', index, ' contour=', len(contours));
# 	#draw the mask
# 	cv2.drawContours(mask, contours, -1, (0, green + index * 10, 0), 1)
# 	cv2.imshow('mask' + str(index), mask);

# cv2.imshow('origin', img);
# cv2.imshow('contour',new_kmeansimg)

cv2.waitKey(0)
cv2.destroyAllWindows()

# aspect_ratio = float(w)/h
# cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

# img = cv2.circle(img,(cx, cy), 5, (0,0,255), -1)

# mask = findMask(img, 157, 157, 157);


# print(type(avg_color), avg_color, avg_color[0][0], low_color);

#get the contour
# def getContour(img):

# cv2.drawContours(img, contours, -1, (0,255,0), 3)

# cv2.imshow('img', img)
# cv2.imshow('mask', mask)
# # cv2.imshow('res', res)
# cv2.waitKey(0)
# cv2.destroyAllWindows();
