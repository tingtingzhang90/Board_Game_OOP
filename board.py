import numpy as np
import pygame


class Board:
    def __init__(self, game_settings):
        self.game_settings = game_settings
        self.game_board = []
        self.create_board()

    def create_board(self):
        self.game_board = np.zeros((self.game_settings.ROW_COUNT, self.game_settings.COLUMN_COUNT))

    def print_board(self):
        print(np.flip(self.game_board, 0))

    def draw_board(self, screen):
        for c in range(self.game_settings.COLUMN_COUNT):
            for r in range(self.game_settings.ROW_COUNT):
                pygame.draw.rect(screen, self.game_settings.BLUE, (c * self.game_settings.SQUARESIZE, r *
                                self.game_settings.SQUARESIZE + self.game_settings.SQUARESIZE,
                                self.game_settings.SQUARESIZE, self.game_settings.SQUARESIZE))
                pygame.draw.circle(screen, self.game_settings.BLACK, (int(c * self.game_settings.SQUARESIZE +
                                self.game_settings.SQUARESIZE / 2), int(r * self.game_settings.SQUARESIZE +
                                self.game_settings.SQUARESIZE + self.game_settings.SQUARESIZE /2)),
                                self.game_settings.RADIUS)

        for c in range(self.game_settings.COLUMN_COUNT):
            for r in range(self.game_settings.ROW_COUNT):
                if self.game_board[r][c] == 1:
                    pygame.draw.circle(screen, self.game_settings.RED, (int(c * self.game_settings.SQUARESIZE +
                                       self.game_settings.SQUARESIZE / 2), self.game_settings.height -
                                       int(r * self.game_settings.SQUARESIZE + self.game_settings.SQUARESIZE /2)),
                                       self.game_settings.RADIUS)
                elif self.game_board[r][c] == 2:
                    pygame.draw.circle(screen, self.game_settings.YELLOW, (int(c * self.game_settings.SQUARESIZE +
                                       self.game_settings.SQUARESIZE / 2), self.game_settings.height - int(r *
                                       self.game_settings.SQUARESIZE + self.game_settings.SQUARESIZE / 2)),
                                       self.game_settings.RADIUS)
        pygame.display.update()