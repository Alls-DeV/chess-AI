import pygame, os

WIDTH = 960
HEIGHT = 960
SQUARE_SIZE = WIDTH//8

FPS = 30

WHITE = "w"
BLACK = "b"

NULL_POSITION = (-1, -1)

board_directory = "assets/board_set"
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join(board_directory, "grey.jpg")), (WIDTH, HEIGHT))


# load images of pieces into two list

piece_directory = "assets/piece_set/california"
wP = pygame.image.load(os.path.join(piece_directory, "wP.png"))
wR = pygame.image.load(os.path.join(piece_directory, "wR.png"))
wN = pygame.image.load(os.path.join(piece_directory, "wN.png"))
wB = pygame.image.load(os.path.join(piece_directory, "wB.png"))
wQ = pygame.image.load(os.path.join(piece_directory, "wQ.png"))
wK = pygame.image.load(os.path.join(piece_directory, "wK.png"))
bP = pygame.image.load(os.path.join(piece_directory, "bP.png"))
bR = pygame.image.load(os.path.join(piece_directory, "bR.png"))
bN = pygame.image.load(os.path.join(piece_directory, "bN.png"))
bB = pygame.image.load(os.path.join(piece_directory, "bB.png"))
bQ = pygame.image.load(os.path.join(piece_directory, "bQ.png"))
bK = pygame.image.load(os.path.join(piece_directory, "bK.png"))

WHITE_IMAGE = [wP, wR, wN, wB, wQ, wK]
BLACK_IMAGE = [bP, bR, bN, bB, bQ, bK]

# resize pieces images
for i in range(6):
    WHITE_IMAGE[i] = pygame.transform.scale(WHITE_IMAGE[i], (SQUARE_SIZE, SQUARE_SIZE))
    BLACK_IMAGE[i] = pygame.transform.scale(BLACK_IMAGE[i], (SQUARE_SIZE, SQUARE_SIZE))


YELLOW_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "yellow_square.png")), (SQUARE_SIZE, SQUARE_SIZE))
GREEN_CIRCLE = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_circle.png")), (SQUARE_SIZE, SQUARE_SIZE))
GREEN_CIRCLE_NEG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "green_circle_neg.png")), (SQUARE_SIZE, SQUARE_SIZE))
RED_CIRCLE_NEG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "red_circle_neg.png")), (SQUARE_SIZE, SQUARE_SIZE))