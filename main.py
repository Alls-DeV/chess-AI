import pygame, sys
from constants import *
from board import Board
from button import Button
from pygame import mixer

# initialize all imported pygame modules
pygame.init()

# define window and caption
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# necessary for capping the FPS
clock = pygame.time.Clock()

'''
update screen while playing
'''
def update_game_display(board : Board):
    SCREEN.blit(BACKGROUND_BOARD, (0, 0))
    board.draw(SCREEN)
    pygame.display.update()

def get_font(size : int):
    return pygame.font.Font("assets/font.otf", size)

def menu():
    while True:
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(WIDTH//8).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, HEIGHT/8))

        PLAY_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/8), text_input="PLAY", font=get_font(WIDTH//8),
                            base_color="#ffffff", hovering_color="Black")
        OPTIONS_BUTTON = Button((WIDTH/2, 2*HEIGHT/3+HEIGHT/8), text_input="OPTIONS", font=get_font(WIDTH//8),
                            base_color="#ffffff", hovering_color="Black")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    game()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    options()

        pygame.display.update()

def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BACKGROUND_OPTIONS, (0, 0))

        OPTIONS_TEXT = get_font(WIDTH//8).render("OPTIONS", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/8))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/8), 
                            text_input="BACK", font=get_font(WIDTH//8), base_color="Black", hovering_color="Dark Green")

        OPTIONS_BACK_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK_BUTTON.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    return

        pygame.display.update()

def game():
    # create instance of board class from board.py
    board = Board()
    
    while True:
        # every repetition of loop update the display
        update_game_display(board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # interaction if the player press on the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                board.click(position, SCREEN)

        if board.checkmate:
            break

        clock.tick(FPS)

    winner = "BLACK" if board.turn == WHITE else "WHITE"
    end_screen(winner)

def end_screen(winner : str):
    while True:
        END_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(BACKGROUND_END, (WIDTH/2-WIDTH*3/8, HEIGHT/6))

        END_TEXT = get_font(WIDTH//8).render(winner+" WIN", True, winner)
        END_RECT = END_TEXT.get_rect(center=(WIDTH/2, HEIGHT/6+WIDTH//8))

        SCREEN.blit(END_TEXT, END_RECT)

        REMATCH_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/5), 
                            text_input="REMATCH", font=get_font(WIDTH//8), base_color="Gray", hovering_color="Green")
        MAIN_MENU_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/2), 
                            text_input="MENU", font=get_font(WIDTH//8), base_color="Gray", hovering_color="Green")

        for button in [REMATCH_BUTTON, MAIN_MENU_BUTTON]:
            button.changeColor(END_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REMATCH_BUTTON.checkForInput(END_MOUSE_POS):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    game()
                if MAIN_MENU_BUTTON.checkForInput(END_MOUSE_POS):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    menu()

        pygame.display.update()

menu()