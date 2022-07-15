import pygame, os
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from constants import *

class Board:
    def __init__(self):
        self.rows = 8
        self.columns = 8

        # create a board 8x8
        self.matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

        # place the pieces on the board
        
        # pawn
        # for i in range(8):
        #     self.matrix[1][i] = Pawn(BLACK)
        #     self.matrix[6][i] = Pawn(WHITE)
        # black piece
        self.matrix[0][0] = Rook(BLACK)
        self.matrix[0][1] = Knight(BLACK)
        self.matrix[0][2] = Bishop(BLACK)
        self.matrix[0][3] = Queen(BLACK)
        self.matrix[0][4] = King(BLACK)
        self.matrix[0][5] = Bishop(BLACK)
        self.matrix[0][6] = Knight(BLACK)
        self.matrix[0][7] = Rook(BLACK)
        # white piece
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
        self.selected_position = NULL_POSITION

        self.last_move = NULL_POSITION

        # calculate all the possible moves of each piece
        self.update_moves()

        self.checkmate = False


    '''
    draw all the pieces on the screen
    '''
    def draw(self, screen):

        # highlight last move
        if self.last_move != NULL_POSITION:
            screen.blit(YELLOW_SQUARE, (self.last_move[0][1]*SQUARE_SIZE, self.last_move[0][0]*SQUARE_SIZE))
            screen.blit(YELLOW_SQUARE, (self.last_move[1][1]*SQUARE_SIZE, self.last_move[1][0]*SQUARE_SIZE))
        
        # if a piece is selected show the possible moves
        if self.selected_position != NULL_POSITION:
            y, x = self.selected_position[0], self.selected_position[1]
            selected_piece = self.matrix[y][x]

            for possible_move in selected_piece.move_set:
                # use a negative circle for the capture
                if self.matrix[possible_move[0]][possible_move[1]]:
                    screen.blit(GREEN_CIRCLE_NEG, (possible_move[1]*SQUARE_SIZE, possible_move[0]*SQUARE_SIZE))

                # use a circle for the movement on an empty square
                else:
                    screen.blit(GREEN_CIRCLE, (possible_move[1]*SQUARE_SIZE, possible_move[0]*SQUARE_SIZE))

        # draw the piece
        for y in range(self.rows):
            for x in range(self.columns):
                tmp = self.matrix[y][x]
                position = (y, x)
                if tmp:
                    tmp.draw(screen, position)

        # highlight the king if it's in check 
        if Board.in_check(self.matrix, self.turn):
            for y in range(8):
                for x in range(8):
                    if self.matrix[y][x] != 0 and self.matrix[y][x].color == self.turn and type(self.matrix[y][x]) == King:
                        screen.blit(RED_CIRCLE_NEG, (x*SQUARE_SIZE, y*SQUARE_SIZE))


    '''
    update the possible moves of each piece on the board
    '''
    def update_moves(self):

        self.checkmate = True

        for y in range(self.rows):
            for x in range(self.columns):
                piece = self.matrix[y][x]
                if piece != 0 and piece.color == self.turn:
                    piece.update_moves(self, (y, x))
                    
                    # removes illegal moves that would put the king in check
                    removed_moves = set()
                    for move in piece.move_set:
                        tmp_matrix = [row[:] for row in self.matrix]
                        tmp_matrix[move[0]][move[1]] = tmp_matrix[y][x]
                        tmp_matrix[y][x] = 0
                        if Board.in_check(tmp_matrix, self.turn):
                            removed_moves.add(move)
                    
                    for move in removed_moves:
                        piece.move_set.remove(move)

                    if len(piece.move_set) > 0:
                        self.checkmate = False


    '''
    check if the king in the matrix is attacked
    '''
    @staticmethod
    def in_check(matrix, color):
        att = Board.attacked_positions(matrix, color)
        
        king_position = NULL_POSITION
        for y in range(8):
            for x in range(8):
                if matrix[y][x] != 0 and matrix[y][x].color == color and type(matrix[y][x]) == King:
                    king_position = (y, x)

        return king_position in att


    '''
    calculate all the square attacked from a player in matrix
    '''
    @staticmethod
    def attacked_positions(matrix, color):

        attacked = set()

        for y in range(8):
            for x in range(8):
                if matrix[y][x] != 0 and color != matrix[y][x].color:

                    if type(matrix[y][x]) == Pawn:

                        sign = -1 if matrix[y][x].color == WHITE else 1

                        if Piece.est_legale(y+sign, x+1):
                            attacked.add((y+sign, x+1))
                        if Piece.est_legale(y+sign, x-1):
                            attacked.add((y+sign, x-1))


                    elif type(matrix[y][x]) == Rook:

                        # vertical up moves
                        for i in range(y+1, 8):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if matrix[i][x] == 0:
                                    attacked.add((i, x))
                                else:
                                    attacked.add((i, x))
                                    break

                        # vertical down moves
                        for i in range(y-1, -1, -1):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if matrix[i][x] == 0:
                                    attacked.add((i, x))
                                else:
                                    attacked.add((i, x))
                                    break

                        # horizontal right moves
                        for j in range(x+1, 8):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if matrix[y][j] == 0:
                                    attacked.add((y, j))
                                else:
                                    attacked.add((y, j))
                                    break

                        # horizontal left moves
                        for j in range(x-1, -1, -1):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if matrix[y][j] == 0:
                                    attacked.add((y, j))
                                else:
                                    attacked.add((y, j))
                                    break


                    elif type(matrix[y][x]) == Knight:

                        jump = [-2, -1, 1, 2]
                        for i in jump:
                            for j in jump:
                                if abs(i) != abs(j) and Piece.est_legale(y+i, x+j):
                                    attacked.add((y+i, x+j))


                    elif type(matrix[y][x]) == Bishop:
                        
                        # all the combination of the direction 
                        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
                        
                        for (sign_y, sign_x) in signs:
                            for k in range(1, 8):
                                a = y+k*sign_y
                                b = x+k*sign_x
                                if Piece.est_legale(a, b) == False:
                                    break
                                else:
                                    if matrix[a][b] == 0:
                                        attacked.add((a, b))
                                    else:
                                        attacked.add((a, b))
                                        break


                    elif type(matrix[y][x]) == Queen:

                        # all the combination of the direction for the diagonal moves
                        signs = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
                        
                        for (sign_y, sign_x) in signs:
                            for k in range(1, 8):
                                a = y+k*sign_y
                                b = x+k*sign_x
                                if Piece.est_legale(a, b) == False:
                                    break
                                else:
                                    if matrix[a][b] == 0:
                                        attacked.add((a, b))
                                    else:
                                        attacked.add((a, b))
                                        break
                        
                        # vertical up moves
                        for i in range(y+1, 8):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if matrix[i][x] == 0:
                                    attacked.add((i, x))
                                else:
                                    attacked.add((i, x))
                                    break

                        # vertical down moves
                        for i in range(y-1, -1, -1):
                            if Piece.est_legale(i, x) == False:
                                break
                            else:
                                if matrix[i][x] == 0:
                                    attacked.add((i, x))
                                else:
                                    attacked.add((i, x))
                                    break

                        # horizontal right moves
                        for j in range(x+1, 8):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if matrix[y][j] == 0:
                                    attacked.add((y, j))
                                else:
                                    attacked.add((y, j))
                                    break

                        # horizontal left moves
                        for j in range(x-1, -1, -1):
                            if Piece.est_legale(y, j) == False:
                                break
                            else:
                                if matrix[y][j] == 0:
                                    attacked.add((y, j))
                                else:
                                    attacked.add((y, j))
                                    break

                    elif type(matrix[y][x]) == King:
                        for i in range(-1, 2):
                            for j in range(-1, 2):
                                if (i != 0 or j != 0) and Piece.est_legale(y+i, x+j):
                                    attacked.add((y+i, x+j))
        
        return attacked


    '''
    manage the interaction with the mouse button, like selecting or move piece
    '''
    def click(self, position, screen):
        y, x = position[1]//SQUARE_SIZE, position[0]//SQUARE_SIZE
        
        if self.matrix[y][x] != 0 and self.matrix[y][x].color == self.turn:
            self.selected_position = (y, x)
        else:
            if self.selected_position != NULL_POSITION and (y, x) in self.matrix[self.selected_position[0]][self.selected_position[1]].move_set:
                
                # self.animate_move(screen, piece, (y, x))
                self.move((y, x), screen)
            else:
                self.selected_position = NULL_POSITION


    '''
    swap the color of the turn
    '''
    def change_turn(self):
        self.turn = WHITE if self.turn == BLACK else BLACK


    '''
    move and capture
    '''
    def move(self, end, screen):
        start = self.selected_position
        piece = self.matrix[start[0]][start[1]]
        
        # remove the piece from the starting position
        self.matrix[start[0]][start[1]] = 0
        
        # reset selected position
        self.selected_position = NULL_POSITION

        # update first move
        if type(piece) in {King, Pawn, Rook}:
            piece.first_move = False

        self.animate_move(start, end, screen, piece)

        # pawn promotion
        if type(piece) == Pawn and ( (end[0] == 0 and piece.color == WHITE) or (end[0] == 7 and piece.color == BLACK) ):
            piece = Queen(piece.color)

        self.matrix[end[0]][end[1]] = piece

        # update last move
        self.last_move = ((start[0], start[1]), (end[0], end[1]))
        self.change_turn()
        self.update_moves()


    '''
    animation for the movement of the piece
    '''
    def animate_move(self, start, end, screen, piece):
        y_distance = end[0] - start[0]
        x_distance = end[1] - start[1]
        frames_per_square = 10
        frame_count = (abs(y_distance) + abs(x_distance)) * frames_per_square
        
        for frame in range(frame_count + 1):
            y, x = start[0] + y_distance*frame/frame_count, start[1] + x_distance*frame/frame_count
            
            screen.blit(BACKGROUND, (0, 0))
            self.draw(screen)
            piece.draw(screen, (y, x))

            pygame.display.update()