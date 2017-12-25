# import the necessary packages
import cv2
import math

class ShapeDetector:
	def __init__(self):
		pass

	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "path"

		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.005 * peri, True)

		# # if the shape is a triangle, it will have 3 vertices
		# if len(approx) == 3:
		# 	shape = "triangle"

		# # if the shape has 4 vertices, it is either a square or
		# # a rectangle
		# elif len(approx) == 4:
		# 	# compute the bounding box of the contour and use the
		# 	# bounding box to compute the aspect ratio
		# 	(x, y, w, h) = cv2.boundingRect(approx)
		# 	ar = w / float(h)	

		# 	# a square will have an aspect ratio that is approximately
		# 	# equal to one, otherwise, the shape is a rectangle
		# 	shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

		# # if the shape is a pentagon, it will have 5 vertices
		# elif len(approx) == 5:
		# 	shape = "pentagon"

		# otherwise, we assume the shape is a circle
		# else:
			#a rectangular
		(x, y, w, h) = cv2.boundingRect(approx)
		# print( w/h);
		if(w/h >= 20):
			shape = 'h-line'
		elif(h/w >= 20):
			shape = 'v-line'
		else:
			area = cv2.contourArea(c)
			rectarea = w * h
			if area < rectarea:
				if area/rectarea > 0.8:
					shape = 'rect'
			elif area >= rectarea:
				if area/rectarea < 1.2:
					shape = 'rect'
			if shape == 'path':
				(x,y), radius = cv2.minEnclosingCircle(c)
				circlearea = radius * radius * math.pi
				# print('circle ratio ', area/circlearea)
				if area < circlearea:
					if area/circlearea >= 0.9:
						shape = 'circle'
				elif area >= circlearea:
					if area/circlearea <= 1.1:
						shape = 'circle'
		# return the name of the shape
		return shape