import copy
from board import Board
import pygame
import sys
import numpy as np


class TicTacToe(Board):
    def __init__(self):
        super().__init__(ROW_COUNT=3, COLUMN_COUNT=3)
        self.height = self.ROW_COUNT * self.SQUARESIZE
        self.size = (self.width, self.height)
        self.WINDOW_LENGTH = 3

########################################################################################################################
    def Clone(self):
        clone = TicTacToe()
        clone.board = copy.deepcopy(self.board)
        clone.turn = copy.deepcopy(self.turn)
        clone.depth = copy.deepcopy(self.depth)
        return clone

    def print_board(self):
        print(self.board)

########################################################################################################################
    def draw_board(self, screen):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(screen, self.BLUE, (c * self.SQUARESIZE, r * self.SQUARESIZE,
                                                     self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(screen, self.BLACK, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                                                        int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, self.RED, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                                                          int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, self.YELLOW, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                                                             int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)
        pygame.display.update()

########################################################################################################################
    def check_event(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                self.pos_x = event.pos[0]
                self.pos_y = event.pos[1]

            if event.type == pygame.MOUSEBUTTONDOWN:
                # print(event.pos)
                if self.turn == self.PLAYER:
                    return self.turn

        if self.turn == self.AI and not self.game_over:
            return self.turn

########################################################################################################################
    def is_valid_location(self, h):
        row, col = self.h2ij(h)
        return self.board[row][col] == 0

########################################################################################################################
    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 2):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece:
                    return True

        # Check vertical locations for win
        for r in range(self.ROW_COUNT - 2):
            for c in range(self.COLUMN_COUNT):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.COLUMN_COUNT - 2):
            for r in range(self.ROW_COUNT - 2):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and \
                        self.board[r + 2][c + 2] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.COLUMN_COUNT - 2):
            for r in range(2, self.ROW_COUNT):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and \
                        self.board[r - 2][c + 2] == piece:
                    return True

########################################################################################################################
    def get_valid_locations(self):
        valid_locations = []
        for row in range(self.ROW_COUNT):
            for col in range(self.COLUMN_COUNT):
                h = self.ij2h(row, col)
                if self.is_valid_location(h):
                    valid_locations.append(self.ij2h(row, col))
        return valid_locations

