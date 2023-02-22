
"""
Evaluation : Evaluate 2D board and validate accordingly
also place detected world piece to 2d form

By: Abel Yohannes
Internship Project for jimma university
"""



import sys

import cv2
import math
from checkers.piece import Piece
from copy import deepcopy


PLAYER1 = "player1"
PLAYER2 = "player2"
ROWS , COLS = 8 , 8
INITIALX , INITIALY = 0 , 0
CELLWIDTH , CELLHEIGHT = 64 ,64
board = []



ILLEGAL_MOVE = False


def get_row_col(pos):
    x, y = pos
    _current = 0
    row, col = 0, 0

    for i in range(ROWS):
        _current = i
        _next = i + 1
        bx1 = math.ceil(INITIALX + CELLWIDTH * _current)
        by1 = math.ceil(INITIALY + CELLHEIGHT * _current)

        bx2 = math.ceil(INITIALX + CELLWIDTH * _next)
        by2 = math.ceil(INITIALY + CELLHEIGHT * _next)

        if y > by1 and y < by2:
            row = _current
        if x > bx1 and x < bx2:
            col = _current

    if col % 2 == ((row) % 2):
        return row, col
    else:
        return None,None


def evaluate(board , player1, player2):

    temp_board = deepcopy(board)
    p2move = []

    try:

        if len(player1) <= 12:
            for _, pos in enumerate(player1):
                row, col = get_row_col(pos)
                if row != None and col != None:
                    p2move.append([row, col])
                else:
                    ILLEGAL_MOVE = True
                    print("ILLEGAL MOVE DETECTED")
                    sys.exit()


            for row in range(ROWS):
                for col in range(COLS):
                    if [row, col] in p2move:

                        piece_add = temp_board.get_piece(row, col)
                        if piece_add != 0 and piece_add.playername == PLAYER1:
                            temp_board.get_board()[row][col] = Piece(row, col, PLAYER1)
                        elif piece_add == 0:
                            temp_board.get_board()[row][col] = Piece(row, col, PLAYER1)

                    else:
                        piece = temp_board.get_piece(row, col)
                        if piece != 0 and piece.playername == PLAYER1:
                            temp_board.get_board()[piece.row][piece.col] = 0

        p2move = []
        if len(player2) <= 12:
            for _, pos in enumerate(player2):
                row, col = get_row_col(pos)
                if row != None and col != None:
                    p2move.append([row, col])
                else:
                    ILLEGAL_MOVE = True
                    print("ILLEGAL MOVE DETECTED")
                    sys.exit()


            for row in range(ROWS):
                for col in range(COLS):
                    if [row, col] in p2move:

                        piece_add = temp_board.get_piece(row, col)
                        if piece_add != 0 and piece_add.playername == PLAYER2:
                            temp_board.get_board()[row][col] = Piece(row, col, PLAYER2)
                        elif piece_add == 0:
                            temp_board.get_board()[row][col] = Piece(row, col, PLAYER2)

                    else:
                        piece = temp_board.get_piece(row, col)
                        if piece != 0 and piece.playername == PLAYER2:
                            temp_board.get_board()[piece.row][piece.col] = 0


            return temp_board
        else:
            print("Morethan 12 piece detected for player 2")
            return 0
    except Exception as e:
        print("Error occured : ", e)
        return 0

