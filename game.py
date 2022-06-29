import pygame
import os
from piece import *
from constants import *
from board import Board

# 3:19:00
board = pygame.transform.scale(pygame.image.load(os.path.join("images", "board.png")), (800, 800))

def redraw_gameWindow():
    global win, chess_board


    win.blit(board, (0, 0))
    chess_board.draw(win)
    
    pygame.display.update()


def click(pos):
    if RECT[0] < pos[0] < RECT[0] + RECT[2] and RECT[1] < pos[1] < RECT[1] + RECT[3]:
        x = pos[0] - RECT[0]
        y = pos[1] - RECT[1]
        i = int(x // (RECT[2] / 8))
        j = int(y // (RECT[3] / 8))
        return i, j

    

def main():
    global chess_board
    chess_board = Board()
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        redraw_gameWindow()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                chess_board.update_moves(chess_board.board)
                x, y = click(pos)
                chess_board.select(x, y)
                



win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
main()