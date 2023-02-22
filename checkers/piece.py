"""
Piece Object and individual piece related info method
By: Abel Yohannes
"""

import pygame
import math
from checkers.constants import CELLWIDTH , CELLHEIGHT , INITIALX , INITIALY

class Piece:

    def __init__(self, row, col, playername):
        self.row = row
        self.col = col
        self.playername = playername
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()


    def calc_pos(self):
        self.x = math.ceil(INITIALX + CELLWIDTH * self.col)
        self.y = math.ceil(INITIALY + CELLHEIGHT * self.row)
        self.y = math.ceil(self.y + CELLHEIGHT / 2)

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.playername)