import math
import pygame
import game_functions as gf


class Player:
    def __init__(self, game_settings):
        self.game_settings = game_settings

    def move(self, board, screen):
        col = int(math.floor(self.game_settings.pos_x / self.game_settings.SQUARESIZE))

        if gf.is_valid_location(self.game_settings, board.game_board, col):
            # row = gf.get_next_open_row(self.game_settings, board.game_board, col)
            # gf.drop_piece(board.game_board, row, col, self.game_settings.PLAYER_PIECE)
            #
            # if gf.winning_move(self.game_settings, board.game_board, self.game_settings.PLAYER_PIECE):
            #     my_font = pygame.font.SysFont("monospace", 75)
            #     label = my_font.render("Player 1 wins!!", 1, self.game_settings.RED)
            #     screen.blit(label, (40, 10))
            #     self.game_settings.game_over = True
            #
            # self.game_settings.turn += 1
            # self.game_settings.turn = self.game_settings.turn % 2
            # board.print_board()
            # board.draw_board(screen)
            gf.detect_game_over(self.game_settings, board, screen, col, self.game_settings.PLAYER_PIECE)
