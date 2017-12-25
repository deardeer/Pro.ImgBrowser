# compute the center of the contour
import cv2
import math
import ColorLabel as CL 

cl = CL.ColorLabeler()

def computeAttr(c, img):

	Attrs = {}

	M = cv2.moments(c)

	## Geometry Shape ##
	#centroid of contour
	cX = int(M["m10"]/ M["m00"])
	cY = int(M["m01"]/ M["m00"]) #/ M["m00"]
	Attrs['center_x'] = cX;
	Attrs['center_y'] = cY;
	# print('cX = int(M["m10"] / M["m00"]) ', M["m10"], M["m00"]);
	# print('centroid ', cX, cY);
	#area
	area = cv2.contourArea(c)
	# print('area ', area, M['m00']);
	Attrs['area'] = area
	Attrs['area_ratio'] = area / (img.shape[0] * img.shape[1]);
	#perimeter
	perimeter = cv2.arcLength(c,True)
	# print('perimeter ', perimeter);
	Attrs['peri'] = perimeter
	#bounding rect	
	x,y,w,h = cv2.boundingRect(c)
	boundingrect = {
	'x': x,
	'y': y,
	'width': w,
	'height': h
	}
	Attrs['bound_w'] = w
	Attrs['bound_h'] = h
	Attrs['ratio'] = w/h
	# print('bounding rect ', boundingrect, w * h / area);
	#enclosing circle
	(x,y), radius = cv2.minEnclosingCircle(c)
	center = (int(x),int(y))
	radius = int(radius)
	boundingcircle = {
	'cx': x,
	'cy': y,
	'radius': radius,
	'area': radius * radius * math.pi
	}
	Attrs['enclosecircle_r'] = radius
	# print('bounding circle ', boundingcircle, radius * radius * math.pi / area)

	## Color ##
	grbcolor = cl.computeMeanColor(img, c)
	rgbcolor = [grbcolor[2], grbcolor[1], grbcolor[0]]
	Attrs['mean_color'] = rgbcolor;
	# print("avg rgbcolor ", rgbcolor);

	return Attrs


 