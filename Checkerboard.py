"""
Main File : It start acb application
Pygame Window will Flash up
By: Abel Yohannes
Internship Project for jimma university
"""



import pygame , threading
import math
import time
from checkers.constants import logoset , WIDTH, HEIGHT , image_loader
from checkers.constants import CELLWIDTH , CELLHEIGHT , INITIALX , INITIALY , ROWS
from checkers.constants import REQUIRED_FRAME_FOR_GIVEN_TIME
from checkers.constants import PLAYER1 , PLAYER2
from checkers.game import Game
from acb_minimax.algorithm import minimax


FPS = 30

# Initialise PyGame.
pygame.init()


Starter = False
loading_finished = False
loading_progress = 0
loading_bar_width = 8


# Work
WORK = 5


screen = pygame.display.set_mode((WIDTH, HEIGHT))
images = image_loader()
font = pygame.font.Font('Fonts/Bahnschrift/BAHNSCHRIFT 12.TTF', 12)
pygame.display.set_caption('Checkers')

# Set image as icon
pygame.display.set_icon(logoset)


def get_row_col_from_mouse(pos):
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

    return row, col

def main():

    # Frame Counter
    frame_count = 0

    run = True
    clock = pygame.time.Clock()
    #Loading_Screen(screen, images)
    game = Game(screen)

    while run:
        clock.tick(FPS)


        if game.turn == PLAYER1:
            value, new_board = minimax(game.get_board(), 4, PLAYER1, game)
            game.ai_move(new_board)




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        if frame_count > REQUIRED_FRAME_FOR_GIVEN_TIME:
            frame_count = 0

        game.update(images, font, frame_count)

        frame_count += 1

    pygame.quit()


if __name__ == "__main__":
    main()
