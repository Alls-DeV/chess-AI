import pygame, sys
from math import inf
from constants import *
from board import Board
from button import Button
from pygame import mixer
from AI import minimax

# initialize all imported pygame modules
pygame.init()

# define window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

# necessary for capping the FPS
clock = pygame.time.Clock()

# index of the lists with the folders name for boards, pieces and highlighted colors in costants.py
# each index refers respectively to [board, piece, possible moves color, last move color]
index_folders = [0, 0, 0, 0]

# flag for check if the volume is on or off
volume_status = True

# flag for check if the light theme is active
light_theme = True

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
    global light_theme
    pygame.display.set_caption("MENU")
    while True:
        if light_theme:
            SCREEN.blit(LIGHT_BACKGROUND, (0, 0))
        else:
            SCREEN.blit(DARK_BACKGROUND, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # buttons for playing and change the settings
        PLAY_BUTTON, OPTIONS_BUTTON = Button.menu_buttons(light_theme)

        THEME_BUTTON = Button.theme_button(light_theme)

        # change the color of the buttons if mouse goes over them
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, THEME_BUTTON]:
            button.change_color(mouse_pos)
            button.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    select_mode()
                if OPTIONS_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    options()
                if THEME_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    light_theme = not light_theme

        pygame.display.update()

def options():
    pygame.display.set_caption("OPTIONS")
    global volume_status
    while True:
        if light_theme:
            SCREEN.blit(LIGHT_BACKGROUND, (0, 0))
        else:
            SCREEN.blit(DARK_BACKGROUND, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        text_color = "Black" if light_theme else "White"

        # list with all the buttons in the options screen
        buttons = []

        # CHANGE CHESSBOARD
        # caption
        BOARD_SETUP = get_font(WIDTH//20).render("BOARD SET", True, text_color)
        BOARD_RECT = BOARD_SETUP.get_rect(center=(WIDTH/4, HEIGHT/8))
        SCREEN.blit(BOARD_SETUP, BOARD_RECT)
        # add to the screen the preview of the chessboard
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT/8-SQUARE_SIZE/2))
        # buttons for change the chessboard
        RIGHT_BOARD_BUTTON, LEFT_BOARD_BUTTON = Button.right_left_buttons(HEIGHT/8, light_theme)
        buttons.append(RIGHT_BOARD_BUTTON)
        buttons.append(LEFT_BOARD_BUTTON)

        # CHANGE PIECES SET
        # caption
        PIECE_SETUP = get_font(WIDTH//20).render("PIECE SET", True, text_color)
        PIECE_RECT = PIECE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*3/10))
        SCREEN.blit(PIECE_SETUP, PIECE_RECT)
        # add to the screen the king of the set selected
        SCREEN.blit(KINGS[index_folders[1]%len(KINGS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*3/10-SQUARE_SIZE/2-HEIGHT/55))
        # buttons for change the pieces set
        RIGHT_PIECE_BUTTON, LEFT_PIECE_BUTTON = Button.right_left_buttons(HEIGHT*3/10, light_theme)
        buttons.append(RIGHT_PIECE_BUTTON)
        buttons.append(LEFT_PIECE_BUTTON)

        # CHANGE THE HIGHLIGHTING COLOR FOR THE POSSIBLE MOVES
        # caption
        CIRCLE_SETUP = get_font(WIDTH//20).render("POSSIBLE MOVE", True, text_color)
        CIRCLE_RECT = CIRCLE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*5/10))
        SCREEN.blit(CIRCLE_SETUP, CIRCLE_RECT)
        # add to the screen the chessboard preview and how the highlight circle appear on it
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*5/10-SQUARE_SIZE/2))
        SCREEN.blit(CIRCLES[index_folders[2]%len(CIRCLES)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*5/10-SQUARE_SIZE/2))
        # buttons for change color of the possible moves
        RIGHT_CIRCLE_BUTTON, LEFT_CIRCLE_BUTTON = Button.right_left_buttons(HEIGHT*5/10, light_theme)
        buttons.append(RIGHT_CIRCLE_BUTTON)
        buttons.append(LEFT_CIRCLE_BUTTON)

        # CHANGE THE HIGHLIGHTINT COLOR FOR THE LAST MOVE
        # caption
        SQUARE_SETUP = get_font(WIDTH//20).render("LAST MOVE", True, text_color)
        SQUARE_RECT = SQUARE_SETUP.get_rect(center=(WIDTH/4, HEIGHT*7/10))
        SCREEN.blit(SQUARE_SETUP, SQUARE_RECT)
        # add to the screen the chessboard preview and how the highlight square appear on it
        SCREEN.blit(BOARDS[index_folders[0]%len(BOARDS)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*7/10-SQUARE_SIZE/2))
        SCREEN.blit(SQUARES[index_folders[3]%len(SQUARES)], (WIDTH*3/4-SQUARE_SIZE/2, HEIGHT*7/10-SQUARE_SIZE/2))
        # buttons for change color of last move
        RIGHT_SQUARE_BUTTON, LEFT_SQUARE_BUTTON = Button.right_left_buttons(HEIGHT*7/10, light_theme)
        buttons.append(RIGHT_SQUARE_BUTTON)
        buttons.append(LEFT_SQUARE_BUTTON)

        # button to turn the volume on and off
        VOLUME_BUTTON = Button.volume_button(volume_status, light_theme)
        buttons.append(VOLUME_BUTTON)

        # button for come back to the main menu
        BACK_BUTTON = Button((WIDTH*3/4, HEIGHT*9/10), "BACK",
                    get_font(WIDTH//8), text_color, "#636f87" if light_theme else "#99c0ff")
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
                    if volume_status:
                        mixer.Sound("assets/sounds/move.mp3").play()
                    index_folders[0] += 1
                if LEFT_BOARD_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/move.mp3").play()
                    index_folders[0] -= 1

                # pieces set
                if RIGHT_PIECE_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/capture.mp3").play()
                    index_folders[1] += 1
                if LEFT_PIECE_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/capture.mp3").play()
                    index_folders[1] -= 1

                # possible moves color
                if RIGHT_CIRCLE_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[2] += 1
                if LEFT_CIRCLE_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[2] -= 1

                # last move color
                if RIGHT_SQUARE_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[3] += 1
                if LEFT_SQUARE_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/change.mp3").play()
                    index_folders[3] -= 1

                if VOLUME_BUTTON.check_for_input(mouse_pos):
                    volume_status = not volume_status
                    if volume_status:
                        if volume_status:
                            mixer.Sound("assets/sounds/select.mp3").play()

                if BACK_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    return

        pygame.display.update()

def select_mode():
    while True:
        if light_theme:
            SCREEN.blit(LIGHT_BACKGROUND, (0, 0))
        else:
            SCREEN.blit(DARK_BACKGROUND, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # buttons for playing against a friend or the computer
        FRIEND_BUTTON, COMPUTER_BUTTON = Button.play_buttons(light_theme)

        # button for come back to the main menu
        BACK_BUTTON = Button((WIDTH*3/4, HEIGHT*9/10), "BACK",
                    get_font(WIDTH//8), "Black" if light_theme else "White", "#636f87" if light_theme else "#99c0ff")

        # change the color of the buttons if mouse goes over them
        for button in [FRIEND_BUTTON, COMPUTER_BUTTON, BACK_BUTTON]:
            button.change_color(mouse_pos)
            button.draw(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if FRIEND_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    friend()
                if COMPUTER_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    computer()
                if BACK_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    return

        pygame.display.update()

'''
player vs player
'''
def friend():
    # create a board giving the settings preferences like the pieces set, chessboard and colors for highlighting squares
    board = Board(folders_name(), volume_status)
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

    winner = "BLACK WINS" if board.turn == WHITE else "WHITE WINS"
    # if the king isn't in check is draw
    if Board.in_check(board.matrix, board.turn) == False:
        winner = "DRAW"
    end_screen(winner)

'''
player vs AI
'''
def computer():
    # create a board giving the settings preferences like the pieces set, chessboard and colors for highlighting squares
    board = Board(folders_name(), volume_status)
    pygame.display.set_caption("CHESS")
    
    while True:
        board.draw(SCREEN)
        
        if board.checkmate:
            break

        if board.turn == BLACK:
            pygame.display.update()
            move = minimax(board.copy(), 3, -inf, inf, BLACK)[0]
            board.move(move[0], move[1], SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if board.turn == WHITE:
                    mouse_pos = pygame.mouse.get_pos()
                    board.click(mouse_pos, SCREEN)

        clock.tick(FPS)
        pygame.display.update()

    winner = "BLACK WINS" if board.turn == WHITE else "WHITE WINS"
    # if the king isn't in check is draw
    if Board.in_check(board.matrix, board.turn) == False:
        winner = "DRAW"
    end_screen(winner)

def end_screen(winner : str):
    while True:
        if light_theme:
            SCREEN.blit(LIGHT_END_BACKGROUND, (WIDTH/2-WIDTH*3/8, HEIGHT/6))
        else:
            SCREEN.blit(DARK_END_BACKGROUND, (WIDTH/2-WIDTH*3/8, HEIGHT/6))
        mouse_pos = pygame.mouse.get_pos()

        # caption with the winner
        END_TITLE = get_font(WIDTH//8).render(winner, True, "#000000" if light_theme else "#ffffff")
        END_RECT = END_TITLE.get_rect(center=(WIDTH/2, HEIGHT/6+WIDTH//8))
        SCREEN.blit(END_TITLE, END_RECT)

        # buttons for rematch and come back to the main menu
        REMATCH_BUTTON, MAIN_MENU_BUTTON = Button.end_buttons(light_theme)

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
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    select_mode()
                if MAIN_MENU_BUTTON.check_for_input(mouse_pos):
                    if volume_status:
                        mixer.Sound("assets/sounds/select.mp3").play()
                    menu()

        pygame.display.update()

menu()