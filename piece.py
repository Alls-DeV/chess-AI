import pygame
import os
from constants import RECT, RED

wP = pygame.image.load(os.path.join("images", "wP.png"))
wR = pygame.image.load(os.path.join("images", "wR.png"))
wN = pygame.image.load(os.path.join("images", "wN.png"))
wB = pygame.image.load(os.path.join("images", "wB.png"))
wQ = pygame.image.load(os.path.join("images", "wQ.png"))
wK = pygame.image.load(os.path.join("images", "wK.png"))
bP = pygame.image.load(os.path.join("images", "bP.png"))
bR = pygame.image.load(os.path.join("images", "bR.png"))
bN = pygame.image.load(os.path.join("images", "bN.png"))
bB = pygame.image.load(os.path.join("images", "bB.png"))
bQ = pygame.image.load(os.path.join("images", "bQ.png"))
bK = pygame.image.load(os.path.join("images", "bK.png"))

white = [wP, wR, wN, wB, wQ, wK]
black = [bP, bR, bN, bB, bQ, bK]

for i in range(6):
    white[i] = pygame.transform.scale(white[i], (95, 95))
    black[i] = pygame.transform.scale(black[i], (95, 95))

class Piece:
    img = -1

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.selected = False

    def move(self):
        pass

    def isSelected(self):
        return self.selected

    def draw(self, win, board):
        if self.color == "w":
            drawThis = white[self.img]
        else:
            drawThis = black[self.img]

        x = round(RECT[0] + (self.column * (RECT[2]/8)))
        y = round(RECT[1] + (self.row * (RECT[3]/8)))
        
        if self.isSelected():
            pygame.draw.rect(win, RED, (x, y, 95, 95), 2)
            for possible_move in self.valid_moves(board):
                i = round(RECT[0] + (possible_move[1] * (RECT[2]/8)))
                j = round(RECT[1] + (possible_move[0] * (RECT[3]/8)))
                pygame.draw.circle(win, RED, (i+50, j+50), 15)

        win.blit(drawThis, (x, y))
    
    def isLegal(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8



class Pawn(Piece):
    img = 0

    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.first = True
        self.queen = False
    
    def valid_moves(self, board):
        y = self.row
        x = self.column
        sign = -1
        if self.color == "b":
            sign = 1

        moves = []
        
        if self.isLegal(x, y+sign) and board[y+sign][x] == 0:
            moves.append((y+sign, x))
            if self.first and board[y + 2*sign][x] == 0:
                moves.append((y + 2*sign, x))
        
        return moves

class Rook(Piece):
    img = 1
    def __init__(self, row, column, color):
        super().__init__(row, column, color)
        self.first = True

    def valid_moves(self, board):
        y = self.row
        x = self.column

        moves = []
        
        for i in range(y+1, 8):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[i][x] == 0:
                    moves.append((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        moves.append((i, x))
                    break

        for i in range(y-1, -1, -1):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[i][x] == 0:
                    moves.append((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        moves.append((i, x))
                    break
        
        for i in range(x+1, 8):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[y][i] == 0:
                    moves.append((y, i))
                else:
                    if board[y][i].color != board[y][x].color:
                        moves.append((y, i))
                    break
        
        for i in range(x-1, -1, -1):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[y][i] == 0:
                    moves.append((y, i))
                else:
                    if board[y][i].color != board[y][x].color:
                        moves.append((y, i))
                    break
        

        return moves

class Knight(Piece):
    img = 2

    def valid_moves(self, board):
        y = self.row
        x = self.column

        moves = []
        
        a = [-2, -1, 1, 2]
        for i in a:
            for j in a:
                if abs(i) != abs(j) and self.isLegal(x+j, y+i) and (board[y+i][x+j] == 0 or board[y+i][x+j].color != self.color):
                    moves.append((y+i, x+j))
        
        return moves

class Bishop(Piece):
    img = 3
    
    def valid_moves(self, board):
        y = self.row
        x = self.column

        moves = []
        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        for (sign1, sign2) in signs:
            for i in range(1, 8):
                a = y+i*sign1
                b = x+i*sign2
                if self.isLegal(a, b) == False:
                    break
                else:
                    if board[a][b] == 0:
                        moves.append((a, b))
                    else:
                        if board[a][b].color != board[y][x].color:
                            moves.append((a, b))
                        break

        return moves

class Queen(Piece):
    img = 4
 
    
    def valid_moves(self, board):
        y = self.row
        x = self.column

        moves = []
        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        for (sign1, sign2) in signs:
            for i in range(1, 8):
                a = y+i*sign1
                b = x+i*sign2
                if self.isLegal(a, b) == False:
                    break
                else:
                    if board[a][b] == 0:
                        moves.append((a, b))
                    else:
                        if board[a][b].color != board[y][x].color:
                            moves.append((a, b))
                        break

        for i in range(y+1, 8):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[i][x] == 0:
                    moves.append((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        moves.append((i, x))
                    break

        for i in range(y-1, -1, -1):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[i][x] == 0:
                    moves.append((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        moves.append((i, x))
                    break
        
        for i in range(x+1, 8):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[y][i] == 0:
                    moves.append((y, i))
                else:
                    if board[y][i].color != board[y][x].color:
                        moves.append((y, i))
                    break
        
        for i in range(x-1, -1, -1):
            if self.isLegal(x, i) == False:
                break
            else:
                if board[y][i] == 0:
                    moves.append((y, i))
                else:
                    if board[y][i].color != board[y][x].color:
                        moves.append((y, i))
                    break

        return moves

class King(Piece):
    img = 5
    
    def valid_moves(self, board):
        return []