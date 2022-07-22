import pygame, sys
from constants import *
from board import Board
from button import Button
from pygame import mixer

# initialize all imported pygame modules
pygame.init()

# define window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# necessary for capping the FPS
clock = pygame.time.Clock()

index_folders = [0, 0, 0, 0]

def folders_name() -> tuple[str, str, str, str]:
    return (board_directories[index_folders[0]], piece_directories[index_folders[1]],
            color_directories[index_folders[2]], color_directories[index_folders[3]])

def get_font(size : int):
    return pygame.font.Font("assets/font.otf", size)

def menu():
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        MENU_TITLE = get_font(WIDTH//8).render("MAIN MENU", True, "#695123")
        MENU_RECT = MENU_TITLE.get_rect(center=(WIDTH/2, HEIGHT/8))

        PLAY_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/8), text_input="PLAY", font=get_font(WIDTH//8),
                            base_color="#000000", hovering_color="Dark Blue")
        OPTIONS_BUTTON = Button((WIDTH/2, 2*HEIGHT/3+HEIGHT/8), text_input="OPTIONS", font=get_font(WIDTH//8),
                            base_color="#000000", hovering_color="Dark Blue")

        SCREEN.blit(MENU_TITLE, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON]:
            button.change_color(mouse_pos)
            button.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    game()
                if OPTIONS_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    options()

        pygame.display.update()

def options():
    pygame.display.set_caption("Option")

    while True:
        SCREEN.blit(BACKGROUND_OPTIONS, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        buttons = []

        BOARD_SETUP = get_font(WIDTH//20).render("BOARD SET", True, "White")
        BOARD_RECT = BOARD_SETUP.get_rect(center=(WIDTH/4, HEIGHT/8))
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT/8-SQUARE_SIZE/2))
        RIGHT_BOARD_BUTTON = Button((WIDTH*3/4+SQUARE_SIZE, HEIGHT/8), 
                            text_input=">", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        LEFT_BOARD_BUTTON = Button((WIDTH*3/4-SQUARE_SIZE, HEIGHT/8), 
                            text_input="<", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        buttons.append(RIGHT_BOARD_BUTTON)
        buttons.append(LEFT_BOARD_BUTTON)


        PIECE_SETUP = get_font(WIDTH//20).render("PIECE SET", True, "White")
        PIECE_RECT = PIECE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*3/10))
        SCREEN.blit(KINGS[index_folders[1]%len(KINGS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*3/10-SQUARE_SIZE/2))
        RIGHT_PIECE_BUTTON = Button((WIDTH*3/4+SQUARE_SIZE, HEIGHT*3/10), 
                            text_input=">", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        LEFT_PIECE_BUTTON = Button((WIDTH*3/4-SQUARE_SIZE, HEIGHT*3/10), 
                            text_input="<", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        buttons.append(RIGHT_PIECE_BUTTON)
        buttons.append(LEFT_PIECE_BUTTON)


        CIRCLE_SETUP = get_font(WIDTH//20).render("POSSIBLE MOVE", True, "White")
        CIRCLE_RECT = CIRCLE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*5/10))
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*5/10-SQUARE_SIZE/2))
        SCREEN.blit(CIRCLES[index_folders[2]%len(CIRCLES)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*5/10-SQUARE_SIZE/2))
        RIGHT_CIRCLE_BUTTON = Button((WIDTH*3/4+SQUARE_SIZE, HEIGHT*5/10), 
                            text_input=">", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        LEFT_CIRCLE_BUTTON = Button((WIDTH*3/4-SQUARE_SIZE, HEIGHT*5/10), 
                            text_input="<", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        buttons.append(RIGHT_CIRCLE_BUTTON)
        buttons.append(LEFT_CIRCLE_BUTTON)


        SQUARE_SETUP = get_font(WIDTH//20).render("LAST MOVE", True, "White")
        SQUARE_RECT = SQUARE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*7/10))
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*7/10-SQUARE_SIZE/2))
        SCREEN.blit(SQUARES[index_folders[3]%len(SQUARES)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*7/10-SQUARE_SIZE/2))
        RIGHT_SQUARE_BUTTON = Button((WIDTH*3/4+SQUARE_SIZE, HEIGHT*7/10), 
                            text_input=">", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        LEFT_SQUARE_BUTTON = Button((WIDTH*3/4-SQUARE_SIZE, HEIGHT*7/10), 
                            text_input="<", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        buttons.append(RIGHT_SQUARE_BUTTON)
        buttons.append(LEFT_SQUARE_BUTTON)


        BACK_BUTTON = Button((WIDTH/2, HEIGHT*9/10), 
                            text_input="BACK", font=get_font(WIDTH//8), base_color="White", hovering_color="Dark Blue")
        buttons.append(BACK_BUTTON)


        SCREEN.blit(SQUARE_SETUP, SQUARE_RECT)
        SCREEN.blit(CIRCLE_SETUP, CIRCLE_RECT)
        SCREEN.blit(PIECE_SETUP, PIECE_RECT)
        SCREEN.blit(BOARD_SETUP, BOARD_RECT)

        for button in buttons:
            button.change_color(mouse_pos)
            button.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # board set
                if RIGHT_BOARD_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/move.mp3").play()
                    index_folders[0] += 1
                if LEFT_BOARD_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/move.mp3").play()
                    index_folders[0] -= 1

                # piece set
                if RIGHT_PIECE_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/capture.mp3").play()
                    index_folders[1] += 1
                if LEFT_PIECE_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/capture.mp3").play()
                    index_folders[1] -= 1

                # possible moves color
                if RIGHT_CIRCLE_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[2] += 1
                if LEFT_CIRCLE_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[2] -= 1

                # last move highlight color
                if RIGHT_SQUARE_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[3] += 1
                if LEFT_SQUARE_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[3] -= 1

                if BACK_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    return

        pygame.display.update()

def game():
    # create instance of board class from board.py
    board = Board(folders_name())
    pygame.display.set_caption("Chess")
    
    while True:
        # every repetition of loop update the display
        board.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # interaction if the player press on the board
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board.click(mouse_pos, SCREEN)

        if board.checkmate:
            break

        clock.tick(FPS)
        pygame.display.update()

    winner = "BLACK" if board.turn == WHITE else "WHITE"
    end_screen(winner)

def end_screen(winner : str):
    while True:
        mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(BACKGROUND_END, (WIDTH/2-WIDTH*3/8, HEIGHT/6))

        END_TITLE = get_font(WIDTH//8).render(winner+" WIN", True, winner)
        END_RECT = END_TITLE.get_rect(center=(WIDTH/2, HEIGHT/6+WIDTH//8))

        SCREEN.blit(END_TITLE, END_RECT)

        REMATCH_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/5), 
                            text_input="REMATCH", font=get_font(WIDTH//8), base_color="Gray", hovering_color="Green")
        MAIN_MENU_BUTTON = Button((WIDTH/2, HEIGHT/3+HEIGHT/2), 
                            text_input="MENU", font=get_font(WIDTH//8), base_color="Gray", hovering_color="Green")

        for button in [REMATCH_BUTTON, MAIN_MENU_BUTTON]:
            button.change_color(mouse_pos)
            button.draw(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REMATCH_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    game()
                if MAIN_MENU_BUTTON.check_for_input(mouse_pos):
                    mixer.Sound("assets/sounds/select.mp3").play()
                    menu()

        pygame.display.update()

menu()