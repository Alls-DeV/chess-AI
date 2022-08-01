from math import inf
from types import NoneType
from piece import Pawn, Rook, Knight, Bishop, Queen, King
from board import Board
from constants import *

'''
evaluate the score of the position counting the relative strength of the pieces on the board
'''
def evaluate(matrix):
    score = 0
    for y in range(8):
        for x in range(8):
            if matrix[y][x] != 0:
                if matrix[y][x].color == WHITE:
                    score += matrix[y][x].value + len(matrix[y][x].move_set)*0.01
                else:
                    score -= (matrix[y][x].value + len(matrix[y][x].move_set)*0.01)
                
                # adding to the score the values of the position of the pieces
                if type(matrix[y][x]) == Pawn:
                    score += pawnEvalWhite[y][x] if matrix[y][x].color == WHITE else -pawnEvalBlack[y][x]
                if type(matrix[y][x]) == Rook:
                    score += rookEvalWhite[y][x] if matrix[y][x].color == WHITE else -rookEvalBlack[y][x]
                if type(matrix[y][x]) == Knight:
                    score += knightEval[y][x] if matrix[y][x].color == WHITE else -knightEval[y][x]
                if type(matrix[y][x]) == Bishop:
                    score += bishopEvalWhite[y][x] if matrix[y][x].color == WHITE else -bishopEvalBlack[y][x]
                if type(matrix[y][x]) == Queen:
                    score += queenEval[y][x] if matrix[y][x].color == WHITE else -queenEval[y][x]
                if type(matrix[y][x]) == King:
                    score += kingEvalWhite[y][x] if matrix[y][x].color == WHITE else -kingEvalBlack[y][x]
    return score

''' 
Minimax algorithm with alpha-beta pruning determines the best move from the current board
'''
def minimax(matrix, depth, alpha, beta, maximizing_color):
    if depth == 0:
        return [NoneType, evaluate(matrix)]
    best_move = -1

    # max player's turn
    if maximizing_color == WHITE:
        max_eval = -inf

        moves = set()
        # adding in moves all the possible moves of each pieces
        for y in range(8):
            for x in range(8):
                if matrix[y][x] != 0 and matrix[y][x].color == WHITE:
                    for end in matrix[y][x].move_set:
                        moves.add(((y, x), end))

        # explore all the potential moves from this board
        for move in moves:
            if best_move == -1:
                best_move = move
            # create a copy of the board
            cpy = [row[:] for row in matrix]
            flag = make_move(cpy, move[0], move[1])
            
            # checkmate
            if flag == 1:
                return [move, inf]
            
            # draw
            elif flag == -1:
                current_eval = 0
            
            else:
                current_eval = minimax(cpy, depth - 1, alpha, beta, BLACK)[1]
            
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move

            # alpha beta optimization
            alpha = max (alpha, current_eval)
            if beta <= alpha:
                break

        return [best_move, max_eval]

    # min player's turn
    else:
        min_eval = inf

        moves = set()
        # adding in moves all the possible moves of each pieces
        for y in range(8):
            for x in range(8):
                if matrix[y][x] != 0 and matrix[y][x].color == BLACK:
                    for end in matrix[y][x].move_set:
                        moves.add(((y, x), end))

        # explore all the potential moves from this board
        for move in moves:
            if best_move == -1:
                best_move = move
            # create a copy of the board
            cpy = [row[:] for row in matrix]
            flag = make_move(cpy, move[0], move[1])

            # checkmate
            if flag == 1:
                return [move, -inf]
            
            # draw
            elif flag == -1:
                current_eval = 0
            
            else:
                current_eval = minimax(cpy, depth - 1, alpha, beta, WHITE)[1]
            
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            
            # alpha beta optimization
            beta = min (beta, current_eval)
            if beta <= alpha:
                break

        return [best_move, min_eval]

def make_move(matrix, start, end):
        piece = matrix[start[0]][start[1]]
        
        # update first move
        if type(piece) in {King, Pawn, Rook}:
            piece.first_move = False
        
        # castle
        if type(piece) == King and abs(start[1] - end[1]) == 2:
            # starting x of the rook
            start_rook = 0 if start[1] > end[1] else 7
            
            king = matrix[start[0]][start[1]]
            rook = matrix[start[0]][start_rook]
            
            # remove king and rook from the starting position
            matrix[start[0]][start[1]] = 0
            matrix[start[0]][start_rook] = 0

            end_rook = 3 if start[1] > end[1] else 5
            # set rook and king in the end position
            matrix[end[0]][end[1]] = king
            matrix[end[0]][end_rook] = rook

        # en passant
        elif (type(piece) == Pawn and matrix[end[0]][end[1]] == 0 and 
                abs(end[1] - start[1]) == 1):
            # remove the piece from the starting position
            matrix[start[0]][start[1]] = 0
            matrix[end[0]][end[1]] = piece
            matrix[start[0]][end[1]] = 0

        else:
            # remove the piece from the starting position
            matrix[start[0]][start[1]] = 0
                
            # pawn promotion
            if type(piece) == Pawn:
                if end[0] == 0 and piece.color == WHITE:
                    piece = Queen(WHITE, QUEEN_VALUE, pygame.image.load(os.path.join("assets/piece_set/alpha", "wQ.png")))
                if end[0] == 7 and piece.color == BLACK:
                    piece = Queen(BLACK, QUEEN_VALUE, pygame.image.load(os.path.join("assets/piece_set/alpha", "bQ.png")))

            matrix[end[0]][end[1]] = piece

        flag = 1
        turn = WHITE if piece.color == BLACK else BLACK

        for y in range(8):
            for x in range(8):
                piece = matrix[y][x]

                # update the possible moves only on the piece of the turn's color
                if piece != 0 and piece.color == turn:
                    piece.update_moves(matrix, (y, x))
                    
                    # castle
                    if type(piece) == King and piece.first_move:
                        # if king is in check can't castle
                        if Board.in_check(matrix, turn):
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
                    illegal_moves = set()
                    for move in piece.move_set:
                        tmp_matrix = [row[:] for row in matrix]
                        tmp_matrix[move[0]][move[1]] = tmp_matrix[y][x]
                        tmp_matrix[y][x] = 0
                        if Board.in_check(tmp_matrix, turn):
                            illegal_moves.add(move)
                    for move in illegal_moves:
                        piece.move_set.remove(move)

                    # if a piece can do to at least one move it isn't checkmate
                    if len(piece.move_set) > 0:
                        flag = 0
        # return 1 if is checkamte, -1 if is draw
        if flag:
            return 1 if Board.in_check(matrix, turn) else -1
        else:
            return 0