"""
Board Creation and Manipulation
By: Abel Yohannes
Internship Project for jimma university
"""


import math
import pygame
from checkers.piece import Piece
from checkers.constants  import ROWS, COLS , PLAYER1 , PLAYER2 , WHITE
from checkers.constants import STACKWIDTH , STACKHIGHT , vid
from checkers.constants import CELLWIDTH , CELLHEIGHT , INITIALX , INITIALY
from util_image import StackFrame

class Board:
    def __init__(self):
        self.board = []
        self.player1_left = self.player2_left = 12
        self.player1_kings = self.player2_kings = 0
        self.create_board()

    def create_board(self):
        # Create 2D board for the system
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):

                #print(f"Working on row : {row} and col : {col}")

                if col % 2 == ((row) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PLAYER1))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PLAYER2))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

                #print("Position : " + self.get_board()[row][col].position)


    def draw_board(self , screen , images):

        for row in range(ROWS):
            for col in range(COLS):
                if col % 2 == ((row) % 2):

                    try:
                        if self.get_board()[row][col] != 0:
                            if self.get_board()[row][col].playername == PLAYER1:
                                if self.get_board()[row][col].king == True:
                                    cx, cy = self.get_board()[row][col].x, self.get_board()[row][col].y
                                    player_rect = images[7].get_rect(midleft=(cx, cy))
                                    screen.blit(images[7], player_rect)
                                else:
                                    cx, cy = self.get_board()[row][col].x, self.get_board()[row][col].y
                                    player_rect = images[6].get_rect(midleft=(cx, cy))
                                    screen.blit(images[6], player_rect)

                            elif self.get_board()[row][col].playername == PLAYER2:
                                if self.get_board()[row][col].king == True:
                                    cx, cy = self.get_board()[row][col].x, self.get_board()[row][col].y
                                    player_rect = images[9].get_rect(midleft=(cx, cy))
                                    screen.blit(images[9], player_rect)
                                else:
                                    cx, cy = self.get_board()[row][col].x, self.get_board()[row][col].y
                                    player_rect = images[8].get_rect(midleft=(cx, cy))
                                    screen.blit(images[8], player_rect)
                    except:
                        print("UNABLE TO DRAW A BOARD !")

    def evaluate(self):
        return self.player1_left - self.player2_left + (self.player1_left * 0.5 - self.player2_left * 0.5)

    def get_all_pieces(self, playername):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.playername == playername:
                    pieces.append(piece)
        return pieces

    def get_board(self):
        return self.board

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_code_position(self, row , cols):
        code = chr(65 + cols)
        code = code+ str(row)
        return code

    def get_position(self, code):
        rows = int(code[1])
        coln = int(ord(code[0])-65)

        return rows , coln

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.playername == PLAYER1:
                self.player1_kings += 1
            else:
                self.player2_kings += 1



    def winner(self):
        if self.player1_left == 0:
            return PLAYER1
        elif self.player2_left == 0:
            return PLAYER2
        
        return None

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.playername == PLAYER1:
                    self.player1_left -= 1
                else:
                    self.player2_left -= 1

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.playername == PLAYER2 or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.playername, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.playername, right))
        if piece.playername == PLAYER1 or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.playername, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.playername, right))

        return moves

    def _traverse_left(self, start, stop, step, playername, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, playername, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, playername, left + 1, skipped=last))
                break
            elif current.playername == playername:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, playername, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, playername, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, playername, right + 1, skipped=last))
                break
            elif current.playername == playername:
                break
            else:
                last = [current]

            right += 1

        return moves


    def draw(self, screen,images):
        screen.blit(images[4], (0, 0))
        ret, frame = vid.read()

        # Simulator
        image = StackFrame(frame)
        stack_rect = image.get_rect(midleft=(271, 335))
        screen.blit(image, stack_rect)

    def draw_square_line(self , screen):

        # Draw Line
        for i in range(ROWS+1):
            x = math.ceil(INITIALX + CELLWIDTH * i)
            y = math.ceil(INITIALY + CELLHEIGHT * i)

            #print(f"@ {i} x = {x} and y = {y}")

            pygame.draw.line(screen, WHITE , [INITIALX, y], [243, y], 1)
            pygame.draw.line(screen, WHITE , [x, 200], [x, 408], 1)

            row , col = self.get_row_col_from_mouse(63,350)


    def get_row_col_from_mouse(self, x , y):
        _current = 0
        row , col = 0 , 0

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


        return row , col





def main():
    board = Board()
    element = board.get_board()
    key = element[0][1]

    print(key)





if __name__ == "__main__":
    main()
