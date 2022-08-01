import pygame, os

WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH//8

FPS = 30

WHITE = "w"
BLACK = "b"

NULL_POSITION = (-1, -1)

# list with images of the kings of each set
piece_folders = ["alpha", "anarcandy", "california", "companion", "dubrovny", "fantasy", "gioco", "horsey", "kosal", "pixel"]
KINGS = []
for folder in piece_folders:
    KINGS.append(pygame.image.load(os.path.join("assets/piece_set/" + folder, "wK.png")))
    KINGS[-1] = pygame.transform.scale(KINGS[-1], (SQUARE_SIZE, SQUARE_SIZE))

# list with images of the preview of each chessboard
board_folders = ["green", "horsey", "maple2", "metal", "pink", "wood", "wood3", "blue2", "blue3", "canvas2", "grey", "maple", "marble", "olive", "purple", "wood2", "wood4"]
BOARDS = []
for folder in board_folders:
    BOARDS.append(pygame.image.load(os.path.join("assets/board_set/" + folder, folder+".thumbnail.jpg")))
    BOARDS[-1] = pygame.transform.scale(BOARDS[-1], (SQUARE_SIZE, SQUARE_SIZE))

# list with the possible highlight colors 
color_folders = ["green", "blue", "purple", "red", "yellow", "horsey", "null"]
SQUARES = []
CIRCLES = []
for folder in color_folders:
    SQUARES.append(pygame.image.load(os.path.join("assets/highlighters/" + folder, folder+"_square.png")))
    SQUARES[-1] = pygame.transform.scale(SQUARES[-1], (SQUARE_SIZE, SQUARE_SIZE))
    CIRCLES.append(pygame.image.load(os.path.join("assets/highlighters/" + folder, folder+"_circle.png")))
    CIRCLES[-1] = pygame.transform.scale(CIRCLES[-1], (SQUARE_SIZE, SQUARE_SIZE))

# background images
LIGHT_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "light.jpeg")), (WIDTH, HEIGHT))
DARK_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "dark.jpeg")), (WIDTH, HEIGHT))
LIGHT_END_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "light.jpeg")), (WIDTH*3/4, HEIGHT*3/4))
DARK_END_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "dark.jpeg")), (WIDTH*3/4, HEIGHT*3/4))

# icons for light and dark theme and for volume on and off
SUN = ""
MOON = ""
VOLUME_ON = ""
VOLUME_OFF = ""

# value of the pieces
PAWN_VALUE = 10
ROOK_VALUE = 50
KNIGHT_VALUE = 30
BISHOP_VALUE = 35
QUEEN_VALUE = 90
KING_VALUE = 1000

# value of the positions of the pieces
pawnEvalWhite = [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
        [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
        [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

pawnEvalBlack = [
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
        [0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0,  0.5],
        [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5],
        [0.0,  0.0,  0.0,  2.5,  2.5,  0.0,  0.0,  0.0],
        [0.5,  0.5,  1.0,  3.0,  3.0,  1.0,  0.5,  0.5],
        [1.0,  1.0,  2.0,  3.5,  3.5,  2.0,  1.0,  1.0],
        [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
        [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

knightEval = [
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-3.0,  0.0,  1.25,  1.5,  1.5,  1.25,  0.0, -3.0],
        [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
        [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
        [-3.0,  0.5,  1.25,  1.5,  1.5,  1.25,  0.5, -3.0],
        [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
        [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]]

bishopEvalWhite = [
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]

bishopEvalBlack = [
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [ -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
    [ -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
    [ -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
    [ -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
    [ -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]]

rookEvalWhite = [
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0]]

rookEvalBlack = [
    [  0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [ -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
    [  0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
    [  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]]

queenEval = [
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [ -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [  0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
    [ -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
    [ -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
    [ -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]]

kingEvalWhite = [
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [  2.0,  2.0, -1.0, -1.0, -1.0, -1.0,  2.0,  2.0],
    [  0.0,  6.0,  5.0,  0.0,  0.0,  1.0,  5.0,  2.0]]

kingEvalBlack = [
    [  0.0,  6.0,  5.0,  0.0,  0.0,  1.0,  5.0,  2.0],
    [  2.0,  2.0, -1.0, -1.0, -1.0, -1.0,  2.0,  2.0],
    [ -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [ -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [ -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0]]