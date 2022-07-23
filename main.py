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

# index of the lists with the folders name for boards, pieces and highlighted colors in costants.py
# each index refers respectively to [board, piece, possible moves color, last move color]
index_folders = [0, 0, 0, 0]

'''
from the index_folders return the names of the folders
'''
def folders_name() -> tuple[str, str, str, str]:
    return (board_folders[index_folders[0]], piece_folders[index_folders[1]],
            color_folders[index_folders[2]], color_folders[index_folders[3]])

'''
from a size return the font resized
'''
def get_font(size : int):
    return pygame.font.Font("assets/font.otf", size)

def menu():
    pygame.display.set_caption("MENU")
    while True:
        SCREEN.blit(BACKGROUND_MENU, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # main menu caption
        MENU_TITLE = get_font(WIDTH//8).render("MAIN MENU", True, "#695123")
        MENU_RECT = MENU_TITLE.get_rect(center=(WIDTH/2, HEIGHT/8))
        SCREEN.blit(MENU_TITLE, MENU_RECT)

        # buttons for playing and change the settings
        PLAY_BUTTON, OPTIONS_BUTTON = Button.menu_buttons()

        # change the color of the buttons if mouse goes over them
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
    pygame.display.set_caption("OPTIONS")
    while True:
        SCREEN.blit(BACKGROUND_OPTIONS, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # list with all the buttons in the options screen
        buttons = []

        # CHANGE CHESSBOARD
        # caption
        BOARD_SETUP = get_font(WIDTH//20).render("BOARD SET", True, "White")
        BOARD_RECT = BOARD_SETUP.get_rect(center=(WIDTH/4, HEIGHT/8))
        SCREEN.blit(BOARD_SETUP, BOARD_RECT)
        # add to the screen the preview of the chessboard
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT/8-SQUARE_SIZE/2))
        # buttons for change the chessboard
        RIGHT_BOARD_BUTTON, LEFT_BOARD_BUTTON = Button.right_left_buttons(HEIGHT/8)
        buttons.append(RIGHT_BOARD_BUTTON)
        buttons.append(LEFT_BOARD_BUTTON)

        # CHANGE PIECES SET
        # caption
        PIECE_SETUP = get_font(WIDTH//20).render("PIECE SET", True, "White")
        PIECE_RECT = PIECE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*3/10))
        SCREEN.blit(PIECE_SETUP, PIECE_RECT)
        # add to the screen the king of the set selected
        SCREEN.blit(KINGS[index_folders[1]%len(KINGS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*3/10-SQUARE_SIZE/2))
        # buttons for change the pieces set
        RIGHT_PIECE_BUTTON, LEFT_PIECE_BUTTON = Button.right_left_buttons(HEIGHT*3/10)
        buttons.append(RIGHT_PIECE_BUTTON)
        buttons.append(LEFT_PIECE_BUTTON)

        # CHANGE THE HIGHLIGHTING COLOR FOR THE POSSIBLE MOVES
        # caption
        CIRCLE_SETUP = get_font(WIDTH//20).render("POSSIBLE MOVE", True, "White")
        CIRCLE_RECT = CIRCLE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*5/10))
        SCREEN.blit(CIRCLE_SETUP, CIRCLE_RECT)
        # add to the screen the chessboard preview and how the highlight circle appear on it
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*5/10-SQUARE_SIZE/2))
        SCREEN.blit(CIRCLES[index_folders[2]%len(CIRCLES)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*5/10-SQUARE_SIZE/2))
        # buttons for change color of the possible moves
        RIGHT_CIRCLE_BUTTON, LEFT_CIRCLE_BUTTON = Button.right_left_buttons(HEIGHT*5/10)
        buttons.append(RIGHT_CIRCLE_BUTTON)
        buttons.append(LEFT_CIRCLE_BUTTON)

        # CHANGE THE HIGHLIGHTINT COLOR FOR THE LAST MOVE
        # caption
        SQUARE_SETUP = get_font(WIDTH//20).render("LAST MOVE", True, "White")
        SQUARE_RECT = SQUARE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*7/10))
        SCREEN.blit(SQUARE_SETUP, SQUARE_RECT)
        # add to the screen the chessboard preview and how the highlight square appear on it
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*7/10-SQUARE_SIZE/2))
        SCREEN.blit(SQUARES[index_folders[3]%len(SQUARES)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*7/10-SQUARE_SIZE/2))
        # buttons for change color of last move
        RIGHT_SQUARE_BUTTON, LEFT_SQUARE_BUTTON = Button.right_left_buttons(HEIGHT*7/10)
        buttons.append(RIGHT_SQUARE_BUTTON)
        buttons.append(LEFT_SQUARE_BUTTON)

        # button for come back to the main menu
        BACK_BUTTON = Button((WIDTH/2, HEIGHT*9/10), "BACK", get_font(WIDTH//8), "White", "Dark Blue")
        buttons.append(BACK_BUTTON)

        # change the color of the buttons if mouse goes over them
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

                # pieces set
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

                # last move color
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
    # create a board giving the settings preferences like the pieces set, chessboard and colors for highlighting squares
    board = Board(folders_name())
    pygame.display.set_caption("CHESS")
    
    while True:
        board.draw(SCREEN)
        
        if board.checkmate:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                board.click(mouse_pos, SCREEN)


        clock.tick(FPS)
        pygame.display.update()

    winner = "BLACK" if board.turn == WHITE else "WHITE"
    end_screen(winner)

def end_screen(winner : str):
    while True:
        SCREEN.blit(BACKGROUND_END, (WIDTH/2-WIDTH*3/8, HEIGHT/6))
        mouse_pos = pygame.mouse.get_pos()

        # caption with the winner's color
        END_TITLE = get_font(WIDTH//8).render(winner+" WIN", True, winner)
        END_RECT = END_TITLE.get_rect(center=(WIDTH/2, HEIGHT/6+WIDTH//8))
        SCREEN.blit(END_TITLE, END_RECT)

        # buttons for rematch and come back to the main menu
        REMATCH_BUTTON, MAIN_MENU_BUTTON = Button.end_buttons()

        # change the color of the buttons if mouse goes over them
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