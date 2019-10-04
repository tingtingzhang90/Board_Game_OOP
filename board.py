import pygame
import numpy as np
import random
import sys


class Board:
    def __init__(self, ROW_COUNT, COLUMN_COUNT):
        # Declaration of colors
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)
        self.BLUE = (0, 0, 255)  # RGB value
        self.BLACK = (0, 0, 0)

        self.depth = 0

        # Size of the board
        self.ROW_COUNT = ROW_COUNT
        self.COLUMN_COUNT = COLUMN_COUNT

        # Turns of Players
        self.PLAYER = 0
        self.AI = 1
        self.turn = random.randint(self.PLAYER, self.AI)
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2

        self.game_over = False

        self.EMPTY = 0

        self.WINDOW_LENGTH = 4

        self.SQUARESIZE = 100  # pixels

        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
        self.size = (self.width, self.height)

        self.RADIUS = int(self.SQUARESIZE / 2 - 5)

        self.pos_x = None
        self.pos_y = None

        self.board = []
        self.create_board()

########################################################################################################################
    def create_board(self):
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

########################################################################################################################
    def print_board(self):
        print(np.flip(self.board, 0))

########################################################################################################################
    def draw_board(self, screen):
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                pygame.draw.rect(screen, self.BLUE, (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE,
                                                     self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(screen, self.BLACK, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                                                        int(r * self.SQUARESIZE + self.SQUARESIZE +
                                                            self.SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, self.RED, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                                                          self.height - int(r * self.SQUARESIZE + self.SQUARESIZE / 2)),
                                       self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, self.YELLOW, (int(c * self.SQUARESIZE + self.SQUARESIZE / 2),
                                                             self.height - int(r * self.SQUARESIZE +
                                                                               self.SQUARESIZE / 2)), self.RADIUS)
        pygame.display.update()

########################################################################################################################
    def check_event(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                self.pos_x = event.pos[0]
                self.pos_y = event.pos[1]
                if self.turn == self.PLAYER:
                    pygame.draw.circle(screen, self.RED, (self.pos_x, int(self.SQUARESIZE / 2)), self.RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                # print(event.pos)

                if self.turn == self.PLAYER:
                    return self.turn

        if self.turn == self.AI and not self.game_over:
            return self.turn

########################################################################################################################
    def ij2h(self, row, col):
        return col * self.COLUMN_COUNT + row + 1

########################################################################################################################
    def h2ij(self, h):
        return (h - 1) % self.COLUMN_COUNT, (h - 1) // self.COLUMN_COUNT

########################################################################################################################
    def drop_piece(self, h, piece):
        row, col = self.h2ij(h)
        self.board[row][col] = piece
        self.depth += 1

########################################################################################################################
    def get_move(self, screen, h, piece):
        self.drop_piece(h, piece)
        if self.is_terminal_node():
            self.game_over = True

        self.print_board()
        self.draw_board(screen)

        self.turn += 1
        self.turn = self.turn % 2


########################################################################################################################
    def is_terminal_node(self):
        return self.winning_move(self.PLAYER_PIECE) or self.winning_move(self.AI_PIECE) or len(
            self.get_valid_locations()) == 0
