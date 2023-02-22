"""
Inference : Used for Video Inferencing
Given the amount of given time depleted , this class
try to capture last frame of streaming and perform yolo inference using cv2.DNN module
By: Abel Yohannes
Internship Project for jimma university
"""




import cv2
from time import time
from Camera import Camera
from utils import *
from cvzone.Utils import *
from evaluate import evaluate , rowWriter



class Deep_Vision:
	'''
	This class holds Game information interacting with the Board and Chess Engine
	'''

	def __init__(self):
		self.camera =  Camera()


	def detection_model(self,frame, board):
		# Player 1
		player1 = []
		player2 = []

		start_time = time()

		# Capture frame-by-frame
		#frame = cv2.imread("res/checker.jpg", cv2.IMREAD_COLOR)
		img = frame.copy()
		# do perspective shift, display in 2nd window

		if img.shape[0] > 0 and img.shape[1] > 0:
			# Binarize the photo
			adaptiveThresh, gray = self.camera.clean_Image(img)
			# Black out all pixels outside the border of the chessboard
			mask, approx = self.camera.initialize_mask(adaptiveThresh, img)

			pts = find_outer_corners(img, approx)
			img_orig = do_perspective_transform(mask, pts)

			img_orig = cv2.resize(img_orig, (512, 512), interpolation=cv2.INTER_AREA)
			# save original copy for piece prediction
			img_orig_predict = img_orig.copy()
			imgs = split_chessboard(img_orig)

			#######################################################
			############        YOLO RECOGNITION         ##########
			#######################################################
			test = img_orig_predict.copy()
			# Display the resulting frame
			test = self.camera.format_yolov5(test)
			outs = self.camera.detect(test, self.camera.net)

			class_ids, confidences, boxes = self.camera.wrap_detection(test, outs[0])

			for (classid, confidence, box) in zip(class_ids, confidences, boxes):

				if classid == 0:

					x, y, w, h = box[0], box[1], box[2], box[3]
					cx, cy = int(box[0] + w / 2), int(box[1] + h / 2)
					test = cv2.circle(test, (cx, cy), 5, (0, 0, 255), -1)

					player1.append([cx, cy])

				else:
					x, y, w, h = box[0], box[1], box[2], box[3]
					cx, cy = int(box[0] + w / 2), int(box[1] + h / 2)
					test = cv2.circle(test, (cx, cy), 5, (0, 0, 255), -1)
					player2.append([cx, cy])

				color = self.camera.colors[int(classid) % len(self.camera.colors)]
				cv2.rectangle(test, box, color, 2)
				cv2.rectangle(test, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
				cv2.putText(test, self.camera.class_list[classid], (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5,
							(0, 0, 0))

			end_time = time()
			sectake = end_time - start_time

			# print(f"Frames Per Second : {fps}")
			start_time = end_time

			# print("player1 detected : ", player1)
			# print("player2 detected : ", player2)

			w, h, _ = test.shape
			dims = list(range(0, w + 1, w // 8))

			for i in dims:
				# Draw Vertical Line
				test = cv2.line(test, (i, 0), (i, w), (255, 0, 0), 2)
				# Draw Horizontal Line
				test = cv2.line(test, (0, i), (w, i), (255, 0, 0), 2)

			if sectake > 0:
				sectake = "Inf Time : %.2f" % sectake
				test, bboxss = putTextRect(test, str(sectake), [10, 20], .5, 1, offset=8, border=3,
										   font=cv2.FONT_HERSHEY_DUPLEX)

			##############################################
			#########       EVALUATE BOARD    ############
			##############################################

			temp_board = evaluate(board, player1, player2)
			return temp_board

		else:
			print("INVALID FRAME DETECTION")
			return 0





