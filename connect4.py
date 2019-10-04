import pygame
import copy
import sys
from board import Board


class Connect4(Board):
    def __init__(self):
        super().__init__(ROW_COUNT=6, COLUMN_COUNT=7)

########################################################################################################################
    def Clone(self):
        clone = Connect4()
        clone.board = copy.deepcopy(self.board)
        clone.turn = copy.deepcopy(self.turn)
        clone.depth = copy.deepcopy(self.depth)
        return clone

########################################################################################################################
    def is_valid_location(self, col):
        return self.board[self.ROW_COUNT - 1][col] == 0

########################################################################################################################
    def get_next_open_row(self, col):
        for r in range(self.ROW_COUNT):
            if self.board[r][col] == 0:
                return r

########################################################################################################################
    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece \
                        and self.board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece \
                        and self.board[r + 3][c] == piece:
                    return True

                    # Check positively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][c + 2] == piece \
                        and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][c + 2] == piece \
                        and self.board[r - 3][c + 3] == piece:
                    return True

########################################################################################################################
    def get_move(self, screen, h, piece):
        self.drop_piece(h, piece)
        if self.winning_move(piece):
            # my_font = pygame.font.SysFont("monospace", 75)
            # if piece == self.PLAYER_PIECE:
            #     label = my_font.render("Human wins!!", 1, self.RED)
            # elif piece == self.AI_PIECE:
            #     label = my_font.render("AI wins!!", 2, self.YELLOW)
            # screen.blit(label, (40, 10))
            self.game_over = True

        self.print_board()
        self.draw_board(screen)

        self.turn += 1
        self.turn = self.turn % 2

########################################################################################################################
    def get_valid_locations(self):
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(col):
                row = self.get_next_open_row(col)
                valid_locations.append(self.ij2h(row, col))
        return valid_locations

# ########################################################################################################################
#     def evaluate_window(self, window, piece):
#         score = 0
#         if piece == self.AI_PIECE:
#             opp_piece = self.PLAYER_PIECE
#         elif piece == self.PLAYER_PIECE:
#             opp_piece = self.AI_PIECE
#
#         if window.count(piece) == 4:
#             score += 10000
#         elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
#             score += 500
#         elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
#             score += 10
#
#         # if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
#         #    score -= 8000
#         return score
#
# ########################################################################################################################
#     def score_position(self, piece):
#         # print("score_position")
#         score = 0
#         # Score center column
#         center_array = [int(i) for i in list(self.board[:, self.COLUMN_COUNT // 2])]
#         center_count = center_array.count(piece)
#         score += center_count * 5
#
#         # Score horizontal
#         for r in range(self.ROW_COUNT):
#             row_array = [int(i) for i in list(self.board[r, :])]
#             for c in range(self.COLUMN_COUNT - 3):
#                 window = row_array[c: c + self.WINDOW_LENGTH]
#                 score += self.evaluate_window(window, piece)
#
#         # Score vertical
#         for c in range(self.COLUMN_COUNT):
#             col_array = [int(i) for i in list(self.board[:, c])]
#             for r in range(self.ROW_COUNT - 3):
#                 window = col_array[r: r + self.WINDOW_LENGTH]
#                 score += self.evaluate_window(window, piece)
#
#         # Score positive sloped diagonal
#         for r in range(self.ROW_COUNT - 3):
#             for c in range(self.COLUMN_COUNT - 3):
#                 window = [self.board[r + i][c + i] for i in range(self.WINDOW_LENGTH)]
#                 score += self.evaluate_window(window, piece)
#
#         # Score negative sloped diagonal
#         for r in range(self.ROW_COUNT - 3):
#             for c in range(self.COLUMN_COUNT - 3):
#                 window = [self.board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)]
#                 score += self.evaluate_window(window, piece)
#         return score
