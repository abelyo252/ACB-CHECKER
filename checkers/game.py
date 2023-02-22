"""
Game : the flow of game engine control by this class
Turn , Vision , Window Update
By: Abel Yohannes
Internship Project for jimma university
"""




import pygame , threading
import math
from checkers.board import Board
from checkers.constants import PLAYER1 , PLAYER2
from checkers.constants import CELLWIDTH , CELLHEIGHT , INITIALX , INITIALY
from checkers.constants import GREEN
from checkers.timer import TimerController
import random
from Inference import Deep_Vision
import cv2
import time


class Game:

    # Basic Initialization
    def __init__(self, screen):
        self._init()
        self.vision = Deep_Vision()
        self.frame_try = cv2.imread("res/checker.jpg", cv2.IMREAD_COLOR)
        self.screen = screen
        self.starter = False


        self.finish = False
        self.loading_finished = False
        self.loading_progress = 0
        self.loading_bar_width = 8

        # Work
        self.WORK = 5

        self.loading_finished, self.loading_progress = False , 0

        # Thread
        threading.Thread(target=self.doWork).start()

    def doWork(self):
        # Do some math WORK amount times


        for i in range(self.WORK):
            time.sleep(2)
            self.loading_progress = i

        self.loading_finished = True
        self.starter = True


    def Loading_Screen(self , screen , images):
        if not self.loading_finished:
            loading_bar_width = self.loading_progress / self.WORK * 582
            loading_bar = pygame.transform.smoothscale(images[2], (int(loading_bar_width), 28))
            loading_bar_rect = loading_bar.get_rect(midleft=(208, 416))

            screen.blit(images[1], (0, 0))
            screen.blit(loading_bar, loading_bar_rect)
        else:
            time.sleep(5)









    def update(self , images , font , frame_count):
        if images is not None:
            if self.starter == False:
                self.Loading_Screen(self.screen, images)

            else:
                self.board.draw(self.screen, images)
                self.board.draw_board(self.screen, images)
                self.board.draw_square_line(self.screen)
                self.draw_valid_moves(self.valid_moves)

                # Time Controlling
                if self.get_turn() == PLAYER1:
                    pass
                    # self.finish = self.timer.clock_controller(self.screen, True , False , frame_count, font)
                else:
                    self.finish = self.timer.clock_controller(self.screen, False, True, frame_count, font)

                # Change Turn
                if self.finish:
                    game_inference_board = self.get_board()
                    temp_board = self.vision.detection_model(self.frame_try, game_inference_board)
                    self.board = temp_board

                    self.change_turn()
                    self.finish = False
        else:
            print("No Pre Image found")



        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = random.choice([PLAYER1]) # , PLAYER2
        self.timer = TimerController()
        self.valid_moves = {}

    def reset(self):
        self._init()

    def winner(self):
        return self.board.winner()

    # Define things

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.playername == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            x, y = math.ceil(INITIALX + CELLWIDTH * col), math.ceil(INITIALY + CELLHEIGHT * row)
            x = math.ceil(x + CELLWIDTH / 2)
            y = math.ceil(y + CELLHEIGHT / 2)
            pygame.draw.circle(self.screen, GREEN , [x, y], 4, 0)

    def get_turn(self):
        return self.turn

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == PLAYER1:
            self.turn = PLAYER2
        else:
            self.turn = PLAYER1

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()