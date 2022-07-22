import pygame, os

WIDTH = 800
HEIGHT = 800
SQUARE_SIZE = WIDTH//8

FPS = 30

WHITE = "w"
BLACK = "b"

NULL_POSITION = (-1, -1)

# array with the images of the king to select the piece theme
piece_directories = ["alpha", "anarcandy", "california", "companion", "dubrovny", "fantasy", "gioco", "horsey", "kosal", "pixel"]
KINGS = []
for folder in piece_directories:
    KINGS.append(pygame.image.load(os.path.join("assets/piece_set/" + folder, "wK.png")))
    KINGS[-1] = pygame.transform.scale(KINGS[-1], (SQUARE_SIZE, SQUARE_SIZE))


board_directories = ["blue-marble", "green", "horsey", "maple2", "metal", "pink", "wood", "wood3", "blue2", "blue3", "canvas2", "grey", "maple", "marble", "olive", "purple", "wood2", "wood4"]
BOARDS = []
for folder in board_directories:
    BOARDS.append(pygame.image.load(os.path.join("assets/board_set/" + folder, folder+".thumbnail.jpg")))
    BOARDS[-1] = pygame.transform.scale(BOARDS[-1], (SQUARE_SIZE, SQUARE_SIZE))


color_directories = ["green", "blue", "purple", "red", "yellow"]
SQUARES = []
CIRCLES = []
for folder in color_directories:
    SQUARES.append(pygame.image.load(os.path.join("assets/highlighters/" + folder, folder+"_square.png")))
    SQUARES[-1] = pygame.transform.scale(SQUARES[-1], (SQUARE_SIZE, SQUARE_SIZE))
    CIRCLES.append(pygame.image.load(os.path.join("assets/highlighters/" + folder, folder+"_circle.png")))
    CIRCLES[-1] = pygame.transform.scale(CIRCLES[-1], (SQUARE_SIZE, SQUARE_SIZE))

# background images
BACKGROUND_MENU = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "menu.jpeg")), (WIDTH, HEIGHT))
BACKGROUND_OPTIONS = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "options.jpeg")), (WIDTH, HEIGHT))
BACKGROUND_END = pygame.transform.scale(pygame.image.load(os.path.join("assets/backgrounds", "end.jpeg")), (WIDTH*3/4, HEIGHT*3/4))