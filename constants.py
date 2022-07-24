import pygame, os

WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH//8

FPS = 30

WHITE = "w"
BLACK = "b"

NULL_POSITION = (-1, -1)

# array with the images of the king to select the piece theme
piece_folders = ["alpha", "anarcandy", "california", "companion", "dubrovny", "fantasy", "gioco", "horsey", "kosal", "pixel"]
KINGS = []
for folder in piece_folders:
    KINGS.append(pygame.image.load(os.path.join("assets/piece_set/" + folder, "wK.png")))
    KINGS[-1] = pygame.transform.scale(KINGS[-1], (SQUARE_SIZE, SQUARE_SIZE))


board_folders = ["green", "horsey", "maple2", "metal", "pink", "wood", "wood3", "blue2", "blue3", "canvas2", "grey", "maple", "marble", "olive", "purple", "wood2", "wood4"]
BOARDS = []
for folder in board_folders:
    BOARDS.append(pygame.image.load(os.path.join("assets/board_set/" + folder, folder+".thumbnail.jpg")))
    BOARDS[-1] = pygame.transform.scale(BOARDS[-1], (SQUARE_SIZE, SQUARE_SIZE))


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

SUN = ""
MOON = ""
VOLUME_ON = ""
VOLUME_OFF = ""