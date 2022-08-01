import pygame
from abc import ABC, abstractmethod
from typing import Union
from constants import *


class Piece(ABC):
    def __init__(self, color : str, value : int, image : pygame.Surface):
        self.color = color
        self.image = image
        self.value = value
        self.move_set = set()

    '''
    update move_set with the possible move of the piece
    '''
    @abstractmethod
    def update_moves(self, board, position):
        pass

    def draw(self, screen : pygame.Surface, position : tuple[int, int]):
        # assign the image
        y, x = position[0]*SQUARE_SIZE, position[1]*SQUARE_SIZE
        screen.blit(self.image, (x, y))
    
    '''
    check the validity of a move
    '''
    @staticmethod
    def est_legale(y : int, x : int):
        return 0 <= y < 8 and 0 <= x < 8


class Pawn(Piece):
    def __init__(self, color : str, value : int, image : pygame.Surface):
        super().__init__(color, value, image)

        # check if the pawn has moved
        self.first_move = True

    def update_moves(self, board : list[list[Union[Piece,int]]], position : tuple[int, int]):
        y, x = position[0], position[1]

        self.move_set = set()

        # white pawn go up while black go down, with sign I can control this
        sign = -1 if self.color == WHITE else 1
        
        # check for the movement
        if Piece.est_legale(y+sign, x) and board[y+sign][x] == 0:
            self.move_set.add((y+sign, x))
            if self.first_move and board[y + 2*sign][x] == 0:
                self.move_set.add((y + 2*sign, x))
        
        # check for the capture
        if Piece.est_legale(y+sign, x+1) and board[y+sign][x+1] != 0 and board[y+sign][x+1].color != board[y][x].color:
            self.move_set.add((y+sign, x+1))
        if Piece.est_legale(y+sign, x-1) and board[y+sign][x-1] != 0 and board[y+sign][x-1].color != board[y][x].color:
            self.move_set.add((y+sign, x-1))


class Rook(Piece):
    def __init__(self, color : str, value : int, image : pygame.Surface):
        super().__init__(color, value, image)

        # flag for check if this rook can castle
        self.first_move = True
    
    def update_moves(self, board : list[list[Union[Piece,int]]], position : tuple[int, int]):
        y, x = position[0], position[1]
        
        self.move_set = set()

        # vertical up moves
        for i in range(y+1, 8):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        self.move_set.add((i, x))
                    break

        # vertical down moves
        for i in range(y-1, -1, -1):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        self.move_set.add((i, x))
                    break

        # horizontal right moves
        for j in range(x+1, 8):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board[y][j].color != board[y][x].color:
                        self.move_set.add((y, j))
                    break

        # horizontal left moves
        for j in range(x-1, -1, -1):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board[y][j].color != board[y][x].color:
                        self.move_set.add((y, j))
                    break


class Knight(Piece):
    def update_moves(self, board : list[list[Union[Piece,int]]], position : tuple[int, int]):
        y, x = position[0], position[1]
        
        self.move_set = set()

        jump = [-2, -1, 1, 2]
        for i in jump:
            for j in jump:
                if abs(i) != abs(j) and Piece.est_legale(y+i, x+j) and (board[y+i][x+j] == 0 or board[y+i][x+j].color != self.color):
                    self.move_set.add((y+i, x+j))


class Bishop(Piece):
    def update_moves(self, board : list[list[Union[Piece,int]]], position : tuple[int, int]):
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
                    if board[a][b] == 0:
                        self.move_set.add((a, b))
                    else:
                        if board[a][b].color != board[y][x].color:
                            self.move_set.add((a, b))
                        break


class Queen(Piece):
    def update_moves(self, board : list[list[Union[Piece,int]]], position : tuple[int, int]):
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
                    if board[a][b] == 0:
                        self.move_set.add((a, b))
                    else:
                        if board[a][b].color != board[y][x].color:
                            self.move_set.add((a, b))
                        break

        # vertical up moves
        for i in range(y+1, 8):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        self.move_set.add((i, x))
                    break

        # vertical down moves
        for i in range(y-1, -1, -1):
            if Piece.est_legale(i, x) == False:
                break
            else:
                if board[i][x] == 0:
                    self.move_set.add((i, x))
                else:
                    if board[i][x].color != board[y][x].color:
                        self.move_set.add((i, x))
                    break
        
        # horizontal right moves
        for j in range(x+1, 8):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board[y][j].color != board[y][x].color:
                        self.move_set.add((y, j))
                    break

        # horizontal left moves
        for j in range(x-1, -1, -1):
            if Piece.est_legale(y, j) == False:
                break
            else:
                if board[y][j] == 0:
                    self.move_set.add((y, j))
                else:
                    if board[y][j].color != board[y][x].color:
                        self.move_set.add((y, j))
                    break


class King(Piece):
    def __init__(self, color : str, value : int, image : pygame.Surface):
        super().__init__(color, value, image)

        # flag for check if king can castle
        self.first_move = True
    
    def update_moves(self, board : list[list[Union[Piece,int]]], position : tuple[int, int]):
        y, x = position[0], position[1]

        self.move_set = set()

        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and Piece.est_legale(y+i, x+j) and (board[y+i][x+j] == 0 or board[y+i][x+j].color != self.color):
                    self.move_set.add((y+i, x+j))
        
        if self.first_move == True:
            # short-castle
            if type(board[y][7]) == Rook and board[y][7].first_move:
                if board[y][6] == 0 and board[y][5] == 0:
                    self.move_set.add((y, 5))
                    self.move_set.add((y, 6))

            # long-castle
            if type(board[y][0]) == Rook and board[y][0].first_move:
                if board[y][1] == 0 and board[y][2] == 0 and board[y][3] == 0:
                    self.move_set.add((y, 2))
                    self.move_set.add((y, 3))