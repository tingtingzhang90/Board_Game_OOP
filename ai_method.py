import math
import random
import game_functions as gf


# Minimax algorithm
def mini_max(game_settings, game_board, depth, maximizing_player):
    valid_locations = gf.get_valid_location(game_settings, game_board)
    is_terminal = gf.is_terminal_node(game_settings, game_board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if gf.winning_move(game_settings, game_board, game_settings.AI_PIECE):
                return None, 100000000000000
            elif gf.winning_move(game_settings, game_board, game_settings.PLAYER_PIECE):
                return None, -10000000000000
            else:
                return None, 0 # Game is over, no more valid moves
        else: # Depth is zero
            return None, gf.score_position(game_settings, game_board, game_settings.AI_PIECE)
    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = gf.get_next_open_row(game_settings, game_board, col)
            b_copy = game_board.copy()
            gf.drop_piece(b_copy, row, col, game_settings.AI_PIECE)
            _, new_score = mini_max(game_settings, b_copy, depth - 1, False)
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = gf.get_next_open_row(game_settings, game_board, col)
            b_copy = game_board.copy()
            gf.drop_piece(b_copy, row, col, game_settings.PLAYER_PIECE)
            _, new_score = mini_max(game_settings, b_copy, depth - 1, True)
            if new_score < value:
                value = new_score
                column = col
        return column, value


# # Alpha beta pruning
# def alpha_beta_pruning(game_settings, game_board, depth, alpha, beta, maximizing_player):
#     valid_locations = gf.get_valid_location(game_settings, game_board)
#     is_terminal = gf.is_terminal_node(game_settings, game_board)
#     if depth == 0 or is_terminal:
#         if is_terminal:
#             if gf.winning_move(game_settings, game_board, game_settings.AI_PIECE):
#                 return None, 100000000000000
#             elif gf.winning_move(game_settings, game_board, game_settings.PLAYER_PIECE):
#                 return None, -10000000000000
#             else:
#                 return None, 0 # Game is over, no more valid moves
#         else: # Depth is zero
#             return None, gf.score_position(game_settings, game_board, game_settings.AI_PIECE)
#     if maximizing_player:
#         value = -math.inf
#         column = random.choice(valid_locations)
#         for col in valid_locations:
#             row = gf.get_next_open_row(game_settings, game_board, col)
#             b_copy = game_board.copy()
#             gf.drop_piece(b_copy, row, col, game_settings.AI_PIECE)
#             _, new_score = alpha_beta_pruning(game_settings, b_copy, depth - 1, alpha, beta, False)
#             if new_score >= value:
#                 value = new_score
#                 column = col
#             alpha = max(alpha, value)
#             if alpha > beta:
#                 break
#         return column, value
#     else: # Minimizing player
#         value = math.inf
#         column = random.choice(valid_locations)
#         for col in valid_locations:
#             row = gf.get_next_open_row(game_settings, game_board, col)
#             b_copy = game_board.copy()
#             gf.drop_piece(b_copy, row, col, game_settings.PLAYER_PIECE)
#             _, new_score = alpha_beta_pruning(game_settings, b_copy, depth - 1, alpha, beta, True)
#             if new_score < value:
#                 value = new_score
#                 column = col
#             beta = min(beta, value)
#             if alpha >= beta:
#                 break
#         return column, value
