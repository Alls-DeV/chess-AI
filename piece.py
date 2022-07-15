import pygame, os
from constants import *


class Piece:
    # represent the index of the image in the list white/black
    img = -1

    
    def __init__(self, color):
        self.color = color
        self.move_set = set()

    
    def draw(self, screen, position):
        # assign the image
        draw_this = WHITE_IMAGE[self.img] if self.color == WHITE else BLACK_IMAGE[self.img]
        y, x = position[0]*SQUARE_SIZE, position[1]*SQUARE_SIZE
        screen.blit(draw_this, (x, y))
    

    '''
    check the validity of a move
    '''
    @staticmethod
    def est_legale(y, x):
        return 0 <= y < 8 and 0 <= x < 8


class Pawn(Piece):
    img = 0

    
    def __init__(self, color):
        super().__init__(color)

        # check if the pawn has moved
        self.first_move = True
    

    def update_moves(self, board, position):
        y, x = position[0], position[1]

        self.move_set = set()

        # white pawn go up while black go down, with sign I can control this
        sign = -1 if self.color == WHITE else 1
        
        # check for the movement
        if Piece.est_legale(y+sign, x) and board.matrix[y+sign][x] == 0:
            self.move_set.add((y+sign, x))
            if self.first_move and board.matrix[y + 2*sign][x] == 0:
                self.move_set.add((y + 2*sign, x))
        
        # check for the capture
        if Piece.est_legale(y+sign, x+1) and board.matrix[y+sign][x+1] != 0 and board.matrix[y+sign][x+1].color != board.matrix[y][x].color:
            self.move_set.add((y+sign, x+1))
        if Piece.est_legale(y+sign, x-1) and board.matrix[y+sign][x-1] != 0 and board.matrix[y+sign][x-1].color != board.matrix[y][x].color:
            self.move_set.add((y+sign, x-1))


class Rook(Piece):
    img = 1

    
    def __init__(self, color):
        super().__init__(color)

        # flag for check if this rook can castle
        self.first_move = True

    
    def update_moves(self, board, position):
        y, x = position[0], position[1]
        
        self.move_set = set()

        # vertical up moves
        for i in range(y+1, 8):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board.matrix[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board.matrix[i][x].color != board.matrix[y][x].color:
                        self.move_set.add((i, x))
                    break

        # vertical down moves
        for i in range(y-1, -1, -1):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board.matrix[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board.matrix[i][x].color != board.matrix[y][x].color:
                        self.move_set.add((i, x))
                    break

        # horizontal right moves
        for j in range(x+1, 8):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board.matrix[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board.matrix[y][j].color != board.matrix[y][x].color:
                        self.move_set.add((y, j))
                    break

        # horizontal left moves
        for j in range(x-1, -1, -1):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board.matrix[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board.matrix[y][j].color != board.matrix[y][x].color:
                        self.move_set.add((y, j))
                    break


class Knight(Piece):
    img = 2

    
    def update_moves(self, board, position):
        y, x = position[0], position[1]
        
        self.move_set = set()

        jump = [-2, -1, 1, 2]
        for i in jump:
            for j in jump:
                if abs(i) != abs(j) and Piece.est_legale(y+i, x+j) and (board.matrix[y+i][x+j] == 0 or board.matrix[y+i][x+j].color != self.color):
                    self.move_set.add((y+i, x+j))


class Bishop(Piece):
    img = 3
    
    
    def update_moves(self, board, position):
        y, x = position[0], position[1]

        self.move_set = set()

        # all the combination of the direction 
        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        
        for (sign_y, sign_x) in signs:
            for k in range(1, 8):
                a = y+k*sign_y
                b = x+k*sign_x
                if Piece.est_legale(a, b) == False:
                    break
                else:
                    if board.matrix[a][b] == 0:
                        self.move_set.add((a, b))
                    else:
                        if board.matrix[a][b].color != board.matrix[y][x].color:
                            self.move_set.add((a, b))
                        break


class Queen(Piece):
    img = 4
    
    
    def update_moves(self, board, position):
        y, x = position[0], position[1]

        self.move_set = set()

        # all the combination of the direction for the diagonal moves
        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]

        for (sign_y, sign_x) in signs:
            for i in range(1, 8):
                a = y+i*sign_y
                b = x+i*sign_x
                if Piece.est_legale(a, b) == False:
                    break
                else:
                    if board.matrix[a][b] == 0:
                        self.move_set.add((a, b))
                    else:
                        if board.matrix[a][b].color != board.matrix[y][x].color:
                            self.move_set.add((a, b))
                        break

        # vertical up moves
        for i in range(y+1, 8):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board.matrix[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board.matrix[i][x].color != board.matrix[y][x].color:
                        self.move_set.add((i, x))
                    break

        # vertical down moves
        for i in range(y-1, -1, -1):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board.matrix[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board.matrix[i][x].color != board.matrix[y][x].color:
                        self.move_set.add((i, x))
                    break
        
        # horizontal right moves
        for j in range(x+1, 8):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board.matrix[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board.matrix[y][j].color != board.matrix[y][x].color:
                        self.move_set.add((y, j))
                    break

        # horizontal left moves
        for j in range(x-1, -1, -1):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board.matrix[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board.matrix[y][j].color != board.matrix[y][x].color:
                        self.move_set.add((y, j))
                    break


class King(Piece):
    img = 5
    
    
    def __init__(self, color):
        super().__init__(color)

        # flag for check if king can castle
        self.first_move = True

    
    def update_moves(self, board, position):
        y, x = position[0], position[1]

        self.move_set = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and Piece.est_legale(y+i, x+j) and (board.matrix[y+i][x+j] == 0 or board.matrix[y+i][x+j].color != self.color):
                    self.move_set.add((y+i, x+j))
        
        if self.first_move == True:
            # short-castle
            if type(board.matrix[y][7]) == Rook and board.matrix[y][7].first_move:
                if board.matrix[y][6] == 0 and board.matrix[y][5] == 0:
                    self.move_set.add((y, 5))
                    self.move_set.add((y, 6))

            # long-castle
            if type(board.matrix[y][0]) == Rook and board.matrix[y][0].first_move:
                if board.matrix[y][1] == 0 and board.matrix[y][2] == 0 and board.matrix[y][3] == 0:
                    self.move_set.add((y, 2))
                    self.move_set.add((y, 3))