"""
Camera : method setup for image manipulation
used in inference.py

By: Abel Yohannes
Internship Project for jimma university
"""




# import the necessary packages
import time
import cv2
import numpy as np
import sys


class Camera:

	def __init__(self, conf_threshold=0.7, score_threshold=0.5, nms_threshold=0.3):
		self.conf = conf_threshold
		self.score = score_threshold
		self.nms = nms_threshold
		self.class_list = self.load_classes()
		self.INPUT_WIDTH = 640
		self.INPUT_HEIGHT = 640

		# Create a VideoCapture object and read from input file
		self.model = "model/v5/mymodel.onnx"

		# print("\n\nDevice Used:", self.device)

		is_cuda = len(sys.argv) > 1 and sys.argv[1] == "cuda"

		self.net = self.build_model(is_cuda)
		self.colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]

	def detect(self, image, net):
		blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (self.INPUT_WIDTH, self.INPUT_HEIGHT), swapRB=True, crop=False)
		net.setInput(blob)
		outputs = net.forward()
		# print(len(outputs))
		return outputs

	def load_classes(self):
		class_list = []
		with open("classes.txt", "r") as f:
			class_list = [cname.strip() for cname in f.readlines()]
		return class_list

	def wrap_detection(self, input_image, output_data):
		class_ids = []
		confidences = []
		boxes = []

		rows = output_data.shape[0]

		image_width, image_height, _ = input_image.shape

		x_factor = image_width / self.INPUT_WIDTH
		y_factor = image_height / self.INPUT_HEIGHT

		for r in range(rows):
			row = output_data[r]
			confidence = row[4]
			if confidence >= 0.4:

				classes_scores = row[5:]
				_, _, _, max_indx = cv2.minMaxLoc(classes_scores)
				class_id = max_indx[1]
				if (classes_scores[class_id] > .25):
					confidences.append(confidence)

					class_ids.append(class_id)

					x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
					left = int((x - 0.5 * w) * x_factor)
					top = int((y - 0.5 * h) * y_factor)
					width = int(w * x_factor)
					height = int(h * y_factor)
					box = np.array([left, top, width, height])
					boxes.append(box)

		indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

		result_class_ids = []
		result_confidences = []
		result_boxes = []

		for i in indexes:
			result_confidences.append(confidences[i])
			result_class_ids.append(class_ids[i])
			result_boxes.append(boxes[i])

		return result_class_ids, result_confidences, result_boxes

	def format_yolov5(self, frame):
		row, col, _ = frame.shape
		_max = max(col, row)
		result = np.zeros((_max, _max, 3), np.uint8)
		result[0:row, 0:col] = frame
		return result

	def build_model(self, is_cuda):
		net = cv2.dnn.readNet(self.model)
		if is_cuda:
			print("Attempty to use CUDA")
			net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
			net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA_FP16)
		else:
			print("Running on CPU")
			net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
			net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
		return net

	def clean_Image(self,frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
		adaptiveThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 125, 1)
		#adaptiveThresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 9, 3)

		return adaptiveThresh, gray

	def initialize_mask(self, adaptiveThresh,frame):
		'''
		Finds border of checker board and blacks out all unneeded pixels
		'''

		# Find contours (closed polygons)
		contours, hierarchy = cv2.findContours(adaptiveThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

		# Create copy of original image
		imgContours = frame.copy()

		for c in range(len(contours)):
			# Area
			area = cv2.contourArea(contours[c])
			# Perimenter
			perimeter = cv2.arcLength(contours[c], True)
				# Filtering the chessboard edge / Error handling as some contours are so small so as to give zero division
				#For test values are 70-40, for Board values are 80 - 75 - will need to recalibrate if change
				#the largest square is always the largest ratio
			if c ==0:
				Lratio = 0
			if perimeter > 0:
				ratio = area / perimeter
				if ratio > Lratio:
					largest=contours[c]
					Lratio = ratio
					Lperimeter=perimeter
					Larea = area
			else:
					pass

		# Draw contours
		imgContours = cv2.drawContours(imgContours, [largest], -1, (0,0,0), 1)


		# Epsilon parameter needed to fit contour to polygon
		epsilon = 0.1 * Lperimeter
		# Approximates a polygon from chessboard edge
		checkerboardEdge = cv2.approxPolyDP(largest, epsilon, True)

		# Create new all black image
		mask = np.zeros((frame.shape[0], frame.shape[1]), 'uint8')*125
		# Copy the checkerboard edges as a filled white polygon size of chessboard edge
		cv2.fillConvexPoly(mask, checkerboardEdge, 255, 1)
		# Assign all pixels that are white (i.e the polygon, i.e. the checkerboard)
		extracted = np.zeros_like(frame)
		extracted[mask == 255] = frame[mask == 255]
		# remove strip around edge
		extracted[np.where((extracted == [125, 125, 125]).all(axis=2))] = [0, 0, 20]


		return extracted , checkerboardEdge

