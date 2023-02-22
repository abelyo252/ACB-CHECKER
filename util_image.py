"""
Stack Image
By: Abel Yohannes
Internship Project for jimma university
"""



import pygame
import cv2
import numpy as np
from cvzone.Utils import stackImages , overlayPNG , putTextRect
from checkers.constants import STACKWIDTH , STACKHIGHT , vid
from Inference import Deep_Vision
from Camera import Camera
from utils import *


vision = Deep_Vision()
process_camera =  Camera()
logo = cv2.imread('Resource/img/logo.png', cv2.IMREAD_UNCHANGED)
camera_not_detect = cv2.imread('Resource/img/camera_not_found.png', cv2.IMREAD_UNCHANGED)




def StackFrame(img , test=None):

    if img is not None:
        #img = vision.detection_model(img)
        img = cv2.imread("res/checker.jpg", cv2.IMREAD_COLOR)
        _ , width , _ = img.shape
        img, bbox = putTextRect(img, "ACB Checker", [int(0.7*width), 50], 2, 2, colorR=(3,186,252),offset=15, border=5)

        # Binarize the photo
        adaptiveThresh, gray = process_camera.clean_Image(img)
        # Black out all pixels outside the border of the chessboard
        mask, approx = process_camera.initialize_mask(adaptiveThresh, img)

        pts = find_outer_corners(img, approx)
        img_orig = do_perspective_transform(mask, pts)
        img_orig = cv2.resize(img_orig, (512, 512), interpolation=cv2.INTER_AREA)
        h, w, _ = img.shape
        test = cv2.resize(img_orig, (w, h), interpolation=cv2.INTER_AREA)


        imgList = [img, gray, adaptiveThresh,  mask , test]
        imgStacked = stackImages(imgList, 2, 0.5)
        imgStacked = cv2.resize(imgStacked, (STACKWIDTH , STACKHIGHT))
        fitter = overlayPNG(imgStacked, logo, pos=[0, 0])

        rgbframe = cv2.cvtColor(fitter, cv2.COLOR_BGR2RGB)
        rgbframe = np.rot90(rgbframe)
        image = pygame.surfarray.make_surface(rgbframe).convert()
        image = pygame.transform.flip(image, True, False)
        return image

    else:
        rgbframe = cv2.cvtColor(camera_not_detect, cv2.COLOR_BGR2RGB)
        rgbframe = np.rot90(rgbframe)
        image = pygame.surfarray.make_surface(rgbframe).convert()
        image = pygame.transform.flip(image, True, False)
        return image

