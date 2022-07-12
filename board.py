import pygame
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from constants import *

class Board:
    def __init__(self):
        self.rows = 8
        self.columns = 8

        # create a board 8x8
        self.matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

        # place the pieces on the board
        for i in range(8):
            self.matrix[1][i] = Pawn(BLACK)
            self.matrix[6][i] = Pawn(WHITE)
        self.matrix[0][0] = Rook(BLACK)
        self.matrix[0][1] = Knight(BLACK)
        self.matrix[0][2] = Bishop(BLACK)
        self.matrix[0][3] = Queen(BLACK)
        self.matrix[0][4] = King(BLACK)
        self.matrix[0][5] = Bishop(BLACK)
        self.matrix[0][6] = Knight(BLACK)
        self.matrix[0][7] = Rook(BLACK)
        self.matrix[7][0] = Rook(WHITE)
        self.matrix[7][1] = Knight(WHITE)
        self.matrix[7][2] = Bishop(WHITE)
        self.matrix[7][3] = Queen(WHITE)
        self.matrix[7][4] = King(WHITE)
        self.matrix[7][5] = Bishop(WHITE)
        self.matrix[7][6] = Knight(WHITE)
        self.matrix[7][7] = Rook(WHITE)

        # flag to understand who has to move
        self.turn = WHITE

        # position of the selected piece
        self.selected_pos = NULL_POSITION

        self.last_move = NULL_POSITION

        #TODO scrivere meglio
        # set with all the position that are attacked from the opposite color of self.turn
        self.attacked = set()
    

    '''
    draw all the pieces on the screen
    '''
    def draw(self, screen):
        for y in range(self.rows):
            for x in range(self.columns):
                tmp = self.matrix[y][x]
                position = (y, x)
                if tmp:
                    tmp.draw(screen, position)
        # if a piece is selected show the possible moves
        if self.selected_pos != NULL_POSITION:
            y, x = self.selected_pos[0], self.selected_pos[1]
            selected_piece = self.matrix[y][x]
            pygame.draw.rect(screen, RED, (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

            for possible_move in selected_piece.move_set:
                pygame.draw.circle(screen, BLUE, (possible_move[1]*SQUARE_SIZE + SQUARE_SIZE/2, possible_move[0]*SQUARE_SIZE + SQUARE_SIZE/2), 15)
    
    
    '''
    update the possible moves of each piece on the board
    '''
    def update_moves(self):

        self.attacked_position()
        for y in range(self.rows):
            for x in range(self.columns):
                tmp = self.matrix[y][x]
                position = (y, x)
                if tmp:
                    tmp.valid_moves(self, position)


    '''
    add all the position attacked from the player with color opposite of the player that can move
    '''
    def attacked_position(self):

        color = self.turn

        # reset attacked
        self.attacked = set()

        for y in range(8):
            for x in range(8):
                if self.matrix[y][x] != 0 and color != self.matrix[y][x].color:

                    if type(self.matrix[y][x]) == Pawn:

                        sign = -1 if self.matrix[y][x].color == WHITE else 1

                        if Piece.est_legale(y+sign, x+1):
                            self.attacked.add((y+sign, x+1))
                        if Piece.est_legale(y+sign, x-1):
                            self.attacked.add((y+sign, x-1))


                    elif type(self.matrix[y][x]) == Rook:

                        # vertical up moves
                        for i in range(y+1, 8):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if self.matrix[i][x] == 0:
                                    self.attacked.add((i, x))
                                else:
                                    self.attacked.add((i, x))
                                    break

                        # vertical down moves
                        for i in range(y-1, -1, -1):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if self.matrix[i][x] == 0:
                                    self.attacked.add((i, x))
                                else:
                                    self.attacked.add((i, x))
                                    break
                        # TODO while for
                        # horizontal right moves
                        for j in range(x+1, 8):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if self.matrix[y][j] == 0:
                                    self.attacked.add((y, j))
                                else:
                                    self.attacked.add((y, j))
                                    break

                        # horizontal left moves
                        for j in range(x-1, -1, -1):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if self.matrix[y][j] == 0:
                                    self.attacked.add((y, j))
                                else:
                                    self.attacked.add((y, j))
                                    break


                    elif type(self.matrix[y][x]) == Knight:

                        jump = [-2, -1, 1, 2]
                        for i in jump:
                            for j in jump:
                                if abs(i) != abs(j) and Piece.est_legale(y+i, x+j):
                                    self.attacked.add((y+i, x+j))


                    elif type(self.matrix[y][x]) == Bishop:
                        
                        # all the combination of the direction 
                        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
                        
                        # TODO forse pure qui posso sostituire con un while
                        for (sign_y, sign_x) in signs:
                            for k in range(1, 8):
                                a = y+k*sign_y
                                b = x+k*sign_x
                                if Piece.est_legale(a, b) == False:
                                    break
                                else:
                                    if self.matrix[a][b] == 0:
                                        self.attacked.add((a, b))
                                    else:
                                        self.attacked.add((a, b))
                                        break


                    elif type(self.matrix[y][x]) == Queen:

                        # all the combination of the direction for the diagonal moves
                        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
                        
                        # TODO forse pure qui posso sostituire con un while
                        for (sign_y, sign_x) in signs:
                            for k in range(1, 8):
                                a = y+k*sign_y
                                b = x+k*sign_x
                                if Piece.est_legale(a, b) == False:
                                    break
                                else:
                                    if self.matrix[a][b] == 0:
                                        self.attacked.add((a, b))
                                    else:
                                        self.attacked.add((a, b))
                                        break
                        
                        # vertical up moves
                        for i in range(y+1, 8):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if self.matrix[i][x] == 0:
                                    self.attacked.add((i, x))
                                else:
                                    self.attacked.add((i, x))
                                    break

                        # vertical down moves
                        for i in range(y-1, -1, -1):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if self.matrix[i][x] == 0:
                                    self.attacked.add((i, x))
                                else:
                                    self.attacked.add((i, x))
                                    break
                        # TODO while for
                        # horizontal right moves
                        for j in range(x+1, 8):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if self.matrix[y][j] == 0:
                                    self.attacked.add((y, j))
                                else:
                                    self.attacked.add((y, j))
                                    break

                        # horizontal left moves
                        for j in range(x-1, -1, -1):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if self.matrix[y][j] == 0:
                                    self.attacked.add((y, j))
                                else:
                                    self.attacked.add((y, j))
                                    break


                    elif type(self.matrix[y][x]) == King:
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if (i != 0 or j != 0) and Piece.est_legale(y+i, x+j):
                                    # TODO controllare se puoi mettere not in
                                    self.attacked.add((y+i, x+j))

    '''
    manage the interaction with the mouse button, like selecting or move piece
    '''
    def click(self, position):
        y, x = position[1]//100, position[0]//100
        
        if self.matrix[y][x] != 0 and self.matrix[y][x].color == self.turn:
            self.selected_pos = (y, x)
        else:
            if self.selected_pos != NULL_POSITION and (y, x) in self.matrix[self.selected_pos[0]][self.selected_pos[1]].move_set:
                self.move((y, x))
            else:
                self.selected_pos = NULL_POSITION


    '''
    swap the color of the turn
    '''
    def change_turn(self):
        self.turn = WHITE if self.turn == BLACK else BLACK


    def move(self, end):
        self.change_turn()
        self.last_move = ((self.selected_pos[0], self.selected_pos[1]), (end[0], end[1]))
        
        piece = self.matrix[self.selected_pos[0]][self.selected_pos[1]]
        self.matrix[end[0]][end[1]] = piece
        self.matrix[self.selected_pos[0]][self.selected_pos[1]] = 0
        
        if(type(piece) in {King, Pawn, Rook}):
            piece.first = False

        self.update_moves()

        self.selected_pos = NULL_POSITION
        # nel caso mi serva sapere il pezzo che ho rimosso
        # removed = self.board[end[0]][end[1]]
        # return removed