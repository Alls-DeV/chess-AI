import pygame
from typing import Union
from piece import Piece, Pawn, Rook, Knight, Bishop, Queen, King
from constants import *
from pygame import mixer

class Board:
    def __init__(self):
        self.rows = 8
        self.columns = 8

        # create a board 8x8
        self.matrix = [[0 for _ in range(self.columns)] for _ in range(self.rows)]

        # place the pieces on the board
        
        # pawn
        for i in range(8):
            self.matrix[1][i] = Pawn(BLACK)
            self.matrix[6][i] = Pawn(WHITE)
        # black pieces
        self.matrix[0][0] = Rook(BLACK)
        self.matrix[0][1] = Knight(BLACK)
        self.matrix[0][2] = Bishop(BLACK)
        self.matrix[0][3] = Queen(BLACK)
        self.matrix[0][4] = King(BLACK)
        self.matrix[0][5] = Bishop(BLACK)
        self.matrix[0][6] = Knight(BLACK)
        self.matrix[0][7] = Rook(BLACK)
        # white pieces
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

        self.moving = False

    '''
    draw all the pieces on the screen
    '''
    def draw(self, screen : pygame.Surface):

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
        if self.moving == False and Board.in_check(self.matrix, self.turn):
            for y in range(8):
                for x in range(8):
                    if (self.matrix[y][x] != 0 and self.matrix[y][x].color == self.turn and
                        type(self.matrix[y][x]) == King):
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
                    piece.update_moves(self.matrix, (y, x))
                    
                    # en passant
                    if (type(piece) == Pawn and self.last_move != NULL_POSITION and
                        type(self.matrix[self.last_move[1][0]][self.last_move[1][1]]) == Pawn and 
                        abs(self.last_move[1][0] - self.last_move[0][0]) == 2):

                            # white pawn go up while black go down, with sign I can control this
                            sign = -1 if self.matrix[y][x].color == WHITE else 1
                            
                            if (Piece.est_legale(y+sign, x+1) and
                                self.matrix[y+sign][x+1] == 0 and (y, x+1) == self.last_move[1]):
                                self.matrix[y][x].move_set.add((y+sign, x+1))
                            if (Piece.est_legale(y+sign, x-1) and 
                                self.matrix[y+sign][x-1] == 0 and (y, x-1) == self.last_move[1]):
                                self.matrix[y][x].move_set.add((y+sign, x-1))
                    
                    # castle
                    if type(piece) == King and piece.first_move:
                        # if king is in check can't castle
                        if Board.in_check(self.matrix, self.turn):
                            if (y, 5) in piece.move_set:
                                piece.move_set.remove((y, 5))
                            if (y, 6) in piece.move_set:
                                piece.move_set.remove((y, 6))
                            if (y, 2) in piece.move_set:
                                piece.move_set.remove((y, 2))
                            if (y, 3) in piece.move_set:
                                piece.move_set.remove((y, 3))

                        else:
                            # short-castle
                            if (y, 5) in piece.move_set and (y, 6) in piece.move_set:
                                piece.move_set.remove((y, 5))
                            else:
                                if (y, 5) in piece.move_set:
                                    piece.move_set.remove((y, 5))
                                if (y, 6) in piece.move_set:
                                    piece.move_set.remove((y, 6))

                            # long-castle
                            if (y, 2) in piece.move_set and (y, 3) in piece.move_set:
                                piece.move_set.remove((y, 3))
                            else:
                                if (y, 2) in piece.move_set:
                                    piece.move_set.remove((y, 2))
                                if (y, 3) in piece.move_set:
                                    piece.move_set.remove((y, 3))

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



                    # if there aren't possible moves, it is checkmate
                    if len(piece.move_set) > 0:
                        self.checkmate = False

    '''
    check if the king in the matrix is attacked
    '''
    @staticmethod
    def in_check(matrix, color : str):
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
    def attacked_positions(matrix : list[list[Union[Piece, int]]], color : str):

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
    def click(self, position : tuple[int, int], screen : pygame.Surface):
        y, x = position[1]//SQUARE_SIZE, position[0]//SQUARE_SIZE
        
        if (y, x) == self.selected_position:
            self.selected_position = NULL_POSITION
        elif self.matrix[y][x] != 0 and self.matrix[y][x].color == self.turn:
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
    def move(self, end : tuple[int, int], screen : pygame.Surface):
        # TODO rimuovere piece non e' necessario passarlo
        start = self.selected_position
        piece = self.matrix[start[0]][start[1]]
        
        # reset selected position
        self.selected_position = NULL_POSITION

        # update first move
        if type(piece) in {King, Pawn, Rook}:
            piece.first_move = False
        
        # castle
        if type(piece) == King and abs(start[1] - end[1]) == 2:
            self.castle(start, end, screen)

        # en passant
        elif (type(piece) == Pawn and self.matrix[end[0]][end[1]] == 0 and 
                abs(end[1] - start[1]) == 1):
            self.en_passant(start, end, screen, piece)

        else:
            self.animate_move(start, end, screen, piece)



        # update last move
        self.last_move = ((start[0], start[1]), (end[0], end[1]))
        self.change_turn()
        self.update_moves()

    def en_passant(self, start : tuple[int, int], end : tuple[int, int], screen : pygame.Surface, piece : Piece):
        self.moving = True

        # remove the piece from the starting position
        self.matrix[start[0]][start[1]] = 0
            
        y_distance = end[0] - start[0]
        x_distance = end[1] - start[1]

        # speed-up diagonal moves
        frames_per_square = 10 if (y_distance == 0 or x_distance == 0) else 5

        # max frame count possible is 50 otherwise the piece is too slow       
        frame_count = min( 50, (abs(y_distance) + abs(x_distance)) * frames_per_square)
        
        for frame in range(frame_count + 1):
            y, x = start[0] + y_distance*frame/frame_count, start[1] + x_distance*frame/frame_count
            
            screen.blit(BACKGROUND_BOARD, (0, 0))
            self.draw(screen)
            piece.draw(screen, (y, x))

            pygame.display.update()

        self.matrix[end[0]][end[1]] = piece
        self.matrix[start[0]][end[1]] = 0
        mixer.Sound("assets/sounds/capture.mp3").play()

        self.moving = False

    def castle(self, start_king : tuple[int, int], end_king : tuple[int, int], screen : pygame.Surface):
        start_rook = 0 if start_king[1] > end_king[1] else 7
        
        king = self.matrix[start_king[0]][start_king[1]]
        rook = self.matrix[start_king[0]][start_rook]
        
        # remove king and rook from the starting position
        self.matrix[start_king[0]][start_king[1]] = 0
        self.matrix[start_king[0]][start_rook] = 0

        # animation for castle

        end_rook = 3 if start_king[1] > end_king[1] else 5
        king_distance = end_king[1] - start_king[1]
        rook_distance = end_rook - start_rook
        frame_count = 20

        for frame in range(frame_count + 1):
            x_king = start_king[1] + king_distance*frame/frame_count
            x_rook = start_rook + rook_distance*frame/frame_count

            screen.blit(BACKGROUND_BOARD, (0, 0))
            self.draw(screen)
            king.draw(screen, (start_king[0], x_king))
            rook.draw(screen, (start_king[0], x_rook))

            pygame.display.update()
        
        # set piece in the end position
        self.matrix[end_king[0]][end_king[1]] = king
        self.matrix[end_king[0]][end_rook] = rook
        
        mixer.Sound("assets/sounds/move.mp3").play()

    '''
    animation for the movement of the piece
    '''
    def animate_move(self, start : tuple[int, int], end : tuple[int, int], screen : pygame.Surface, piece : Piece):
        self.moving = True

        # remove the piece from the starting position
        self.matrix[start[0]][start[1]] = 0
            
        y_distance = end[0] - start[0]
        x_distance = end[1] - start[1]

        # speed-up diagonal moves
        frames_per_square = 10 if (y_distance == 0 or x_distance == 0) else 5

        # max frame count possible is 50 otherwise the piece is too slow       
        frame_count = min( 50, (abs(y_distance) + abs(x_distance)) * frames_per_square)
        
        for frame in range(frame_count + 1):
            y, x = start[0] + y_distance*frame/frame_count, start[1] + x_distance*frame/frame_count
            
            screen.blit(BACKGROUND_BOARD, (0, 0))
            self.draw(screen)
            piece.draw(screen, (y, x))

            pygame.display.update()

        # pawn promotion
        if type(piece) == Pawn and ( (end[0] == 0 and piece.color == WHITE) or (end[0] == 7 and piece.color == BLACK) ):
            piece = Queen(piece.color)

        if self.matrix[end[0]][end[1]] == 0:
            mixer.Sound("assets/sounds/move.mp3").play()
        else:
            mixer.Sound("assets/sounds/capture.mp3").play()

        self.matrix[end[0]][end[1]] = piece

        self.moving = False