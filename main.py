import pygame
from constants import *
from board import Board

# initialize all imported pygame modules
pygame.init()

# define window and caption
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# necessary for capping the FPS
clock = pygame.time.Clock()


def update_display(board : Board):
    screen.blit(BACKGROUND, (0, 0))
    board.draw(screen)
    pygame.display.update()


'''
main program loop for the chess game
'''
def main():
    run = True

    # create instance of board class from board.py
    board = Board()
    
    while run:
        clock.tick(FPS)

        # every repetition of loop update the display
        update_display(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # break the game loop
                run = False
            
            # interaction if the player press on the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                board.click(position, screen)

        if board.checkmate:
            run = False

    # stop pygame
    pygame.quit()

if __name__ == "__main__":
    main()