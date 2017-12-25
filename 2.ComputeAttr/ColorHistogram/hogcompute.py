import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from os.path import basename

class HOGCom:

	def computeHOG(self, imgDir):
		image = cv2.imread(imgDir, 0)
		winSize = (64,64)
		blockSize = (16,16)
		blockStride = (8,8)
		cellSize = (8,8)
		nbins = 3
		derivAperture = 1
		winSigma = 4.
		histogramNormType = 0
		L2HysThreshold = 2.0000000000000001e-01
		gammaCorrection = 0
		nlevels = 64
		hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
		                        histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
		#compute(img[, winStride[, padding[, locations]]]) -> descriptors
		
		winStride = (8,8)
		padding = (8,8)
		locations = ((10,20),)
		hist = hog.compute(image,winStride,padding,locations)
		return hist.tolist();
		# hist_downsampe = self.downsampleHIST(hist)
		# print(len(hist), len(hist_downsampe))
		# # self.plot(hist);
		# plt.plot(hist_downsampe, linewidth=1)
		# plt.show();

	def downsampleHIST(self, hist):
		hist_np = np.array(hist)#[::9]
		return hist_np.tolist();

	def compute_saveDB(self, imgDir, collection):
		#save to db: update or add	
		hist = self.computeHOG(imgDir)
		filebasename = basename(imgDir)		
		doc = collection.find_one({'imgName': filebasename});
		print('save HOG begin ', filebasename)
		if(doc == None):
			collection.insert({
					'imgName': filebasename,
					'HOG': hist,
					# 'index': beginIndex,
					});
		else:
			collection.update(
				{
					'imgName': filebasename
					},
				{
					'$set':{
						'HOG': hist
					}
				},
				upsert=False
			)
			
		print('ok')


 #    def plot(self, ax):
 #        color_samples = self._hist1D.colorCoordinates()
 #        color_densities = self._hist1D.colorDensities()

 #        colors = self._hist1D.rgbColors()

 #        #log the color density
 #        new_log_colordens = []
 #        for temp_den in color_densities:
 #            if(temp_den != 0):
 #                new_log_colordens.append(math.log(temp_den));
 #            else:
 #                new_log_colordens.append(temp_den);

 #        max_newlog = np.max(new_log_colordens);
 #        min_newlog = np.min(new_log_colordens);
 #        new_log_colordens = (new_log_colordens - min_newlog)/(max_newlog - min_newlog);

 #        color_range = self._hist1D.colorRange()
 #        width = (color_range[1] - color_range[0]) / float(self._hist1D.numBins())

 #        # print('new_log_colordens ', new_log_colordens, 'colors ', colors);
 #        ax.bar(color_samples, new_log_colordens, width=width, color=colors) #edgecolor='black'
 #        self._axisSetting(ax)

	# def _axisSetting(self, ax):
 #        color_space = self._hist1D.colorSpace()
 #        channel = self._hist1D.channel()

 #        ax.set_xlabel(color_space[channel])
 #        ax.set_ylabel("Density")

 #        color_range = self._hist1D.colorRange()
 #        tick_range = np.array([color_range, [0.0, 1.0]])
 #        xticks, yticks = range2ticks(tick_range)

 #        ax.set_xticks(xticks)
 #        ax.set_yticks(yticks)

 #        xlim, ylim = self._range2lims(tick_range)

 #        ax.set_xlim(xlim)
 #        ax.set_ylim(ylim)