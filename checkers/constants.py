"""
Declare all static file here
By: Abel Yohannes
Internship Project for jimma university
"""

import pygame
import cv2
import sys
sys.path.append('../')

WIDTH, HEIGHT = 853,640
ROWS, COLS = 8, 8

FPS = 30

# Set Logo for this Software
logoset = pygame.image.load('Resource/img/logo.png')


#Player Name
PLAYER1 , PLAYER2  = "player1" , "player2"

# Cell Width and Cell Height
CELLWIDTH , CELLHEIGHT = 27.25, 26.25


# Initial Location
INITIALX , INITIALY = 25 , 198


#Simulation Stack Image List
STACKWIDTH , STACKHIGHT = 581 , 606


# Time Remaining for Player
START_TIME = 10
REQUIRED_FRAME_FOR_GIVEN_TIME = START_TIME * FPS


# define a video capture object
vid = cv2.VideoCapture('Resource/vid/checker.mp4')


# Initialized ALL Image
def image_loader():
    _splash = pygame.image.load("Resource/img/2.png").convert()
    _loading = pygame.image.load("Resource/img/3.png").convert()
    _loading_bar = pygame.image.load("Resource/img/bar.png").convert_alpha()
    _start_game = pygame.image.load("Resource/img/6.png").convert()
    _simulation = pygame.image.load("Resource/img/7.png").convert()
    _bigLogo = pygame.image.load("Resource/img/bigLogo.png").convert_alpha()


    # Player Asset
    player1 = pygame.image.load("Resource/img/Cap/Bottle/player1.png").convert_alpha()
    player1_crown = pygame.image.load("Resource/img/Cap/Bottle/player1_king.png").convert_alpha()
    player2 = pygame.image.load("Resource/img/Cap/Bottle/player2.png").convert_alpha()
    player2_crown = pygame.image.load("Resource/img/Cap/Bottle/player2_king.png").convert_alpha()




    #Image Loading
    images = [_splash, _loading , _loading_bar , _start_game , _simulation , _bigLogo , player1 , player1_crown
              ,player2 , player2_crown]

    return images


# Define Color
GREEN = (0,255,0)
WHITE = (255, 255, 255)

