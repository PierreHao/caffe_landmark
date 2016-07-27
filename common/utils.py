# coding: utf-8

import cv2
import numpy as np

class BBox(object):
	# bbox is a list of [left, right, top, bottom]
	def __init__(self, bbox):
		self.left = bbox[0]
		self.right = bbox[1]
		self.top = bbox[2]
		self.bottom = bbox[3]
		self.x = bbox[0]
		self.y = bbox[2]
		self.w = bbox[1] - bbox[0]
		self.h = bbox[3] - bbox[2]

	# scale to [0,1]
	def projectLandmark(self, landmark):
		
		for i, point in enumerate(landmark):
			landmark[i] = ((point[0]-self.x)/self.w, (point[1]-self.y)/self.h)
		return landmark

	# landmark of (5L, 2L) from [0,1] to real range
	def reprojectLandmark(self, landmark):
		for i, point in enumerate(landmark):
			x = point[0] * self.w + self.x
			y = point[1] * self.h + self.y
			landmark[i] = (x, y)
		return landmark

def drawLandmark(img, bbox, landmark):
	'''
	Input:
	- img: gray or RGB
	- bbox: type of BBox
	- landmark: reproject landmark of (5L, 2L)
	Output:
	- img marked with landmark and bbox
	'''
	cv2.rectangle(img, (bbox.left, bbox.top), (bbox.right, bbox.bottom), (0,0,255), 2)
	for x, y in landmark:
		cv2.circle(img, (int(x), int(y)), 3, (0,255,0), -1)
	return img

def processImage(imgs):
	'''
	Subtract mean and normalize, imgs [N, 1, W, H]
	'''
	imgs = imgs.astype(np.float32)
	for i, img in enumerate(imgs):
		m = img.mean()
		s = img.std()
		imgs[i] = (img-m)/s
	return imgs

def flip(face, landmark):
	'''
	flip a face and its landmark
	'''
	face_ = cv2.flip(face, 1) # 1 means flip horizontal
	landmark_flip = np.asarray(np.zeros(landmark.shape))
	for i, point in enumerate(landmark):
		landmark_flip[i] = (1-point[0], point[1])
	landmark_flip[[0,1]] = landmark_flip[[1,0]]
	landmark_flip[[3,4]] = landmark_flip[[4,3]]
	return (face_, landmark_flip)

def check_bbox(img, bbox):
	'''
	Check whether bbox is out of the range of the image
	'''
	img_w, img_h = img.shape
	if bbox.x > 0 and bbox.y > 0 and bbox.right < img_w and bbox.bottom < img_h:
		return True
	else:
		return False