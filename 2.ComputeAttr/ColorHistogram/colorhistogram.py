from color_histogram.maskbg import maskImgBG
from color_histogram.maskbg import getMask
from color_histogram.io_util.image import loadRGB
from color_histogram.io_util.image import loadRGB_lm
from color_histogram.core.hist_1d import Hist1D
import matplotlib.pyplot as plt

import cv2
import numpy as np

# maks bg
# img_maskbg = maskImgBG('../../cropimg/10.png')
imgdir = '../../img/Abastract timeline infographic template.jpg'
image_mask = maskImgBG(imgdir)
# cv2.imshow('mask', image_mask)
# cv2.waitKey(0)

image = loadRGB_lm(image_mask);
# print('image type ', type(image), image.shape);

# 16 bins, Lab color space, target channel L ('Lab'[0])
hist1D = Hist1D(image, num_bins=300, alpha=0, color_space='hsv', channel=0)
hist1D_L = Hist1D(image, num_bins=300, alpha=0, color_space='Lab', channel=0)

fig1 = plt.figure()
ax = fig1.add_subplot(111)
hist1D.plot(ax)
fig2 = plt.figure()
ax_L = fig2.add_subplot(111)
hist1D_L.plot(ax_L)
plt.show()