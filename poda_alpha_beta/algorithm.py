import pygame
from copy import deepcopy
from checkers.constants import BLACK, WHITE
moves = []


def poda_alpha_beta(position, depth, alpha, beta, max_player, game, verbose=False):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = poda_alpha_beta(move, depth-1, alpha, beta, False, game, verbose)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                if verbose:
                    print(f"Podando en max player con beta={beta}, alpha={alpha}")
                break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, BLACK, game):
            evaluation = poda_alpha_beta(move, depth-1, alpha, beta, True, game, verbose)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                if verbose:
                    print(f"Podando en min player con beta={beta}, alpha={alpha}")
                break
        
        return minEval, best_move

def poda_alpha_beta1(position, depth, alpha, beta, max_player, game, verbose=False):
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves1(position, BLACK, game):
            evaluation = poda_alpha_beta1(move, depth-1, alpha, beta, False, game, verbose)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                if verbose:
                    print(f"Podando en max player con beta={beta}, alpha={alpha}")
                break
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves1(position, WHITE, game):
            evaluation = poda_alpha_beta1(move, depth-1, alpha, beta, True, game, verbose)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                if verbose:
                    print(f"Podando en min player con beta={beta}, alpha={alpha}")
                break
        
        return minEval, best_move


def guardar_lista_en_txt(lista, archivo):
    with open(archivo, "w") as f:
        for item in lista:
            f.write(str(item) + ",")


def reward(board, player_color):
    if board.winner() == player_color:
        return 1
    elif board.winner() == None:
        return 0
    else:
        return -1


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #descomentar para ver jugadas posibles
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves


def get_all_moves1(board, color, game):
    moves = []
    
    for piece in board.get_all_pieces(WHITE if color == BLACK else BLACK):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #descomentar para ver jugadas posibles
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
           
    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100)

