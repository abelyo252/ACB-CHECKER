"""
Imange Manipulation technique used by inference.py
By: Abel Yohannes
Internship Project for jimma university
"""




import cv2
import numpy as np
import math



def distance(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def find_outer_corners(img, pts):
    rows, cols, _ = img.shape

    bl_dst = br_dst = tl_dst = tr_dst = float('inf')

    for p in pts:

        p = p[0]

        if distance(p, (cols * 0, rows * 1)) < bl_dst:
            bl_dst = distance(p, (cols * 0, rows * 1))
            bl = p

        if distance(p, (cols * 1, rows * 1)) < br_dst:
            br_dst = distance(p, (cols * 1, rows * 1))
            br = p

        if distance(p, (cols * 0, rows * 0)) < tl_dst:
            tl_dst = distance(p, (cols * 0, rows * 0))
            tl = p

        if distance(p, (cols * 1, rows * 0)) < tr_dst:
            tr_dst = distance(p, (cols * 1, rows * 0))
            tr = p

    pts1 = np.float32(
        [bl,  # btm left
         br,  # btm right
         tl,  # top left
         tr]  # top right
    )

    return pts1


def find_max_contour_area(contours):
    max_area = 0 - float('inf')
    max_c = None

    for c in contours:
        area = cv2.contourArea(c)

        if area > max_area:
            max_area = area
            max_c = c

    return [max_c]


def do_perspective_transform(img, pts, pts_type=1):
    rows, cols = img.shape[:2]

    bl = [cols * 0, rows * 1]
    br = [cols * 1, rows * 1]
    tl = [cols * 0, rows * 0]
    tr = [cols * 1, rows * 0]

    pts2 = np.float32([bl, br, tl, tr])

    if pts_type == 2:
        pts, pts2 = pts2, pts

    M = cv2.getPerspectiveTransform(pts, pts2)

    color = 255

    if len(img.shape) == 3:
        color = (255, 255, 255)

    img = cv2.warpPerspective(img, M, (cols, rows), borderValue=color)

    return img



def split_chessboard(img):
    w = img.shape[0]
    sq = w // 8

    imgs = []

    for i in range(0, w, sq):
        for j in range(0, w, sq):
            imgs.append(img[i: i + sq, j: j + sq])

    return imgs
