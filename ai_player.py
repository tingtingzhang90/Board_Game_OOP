import math
import pygame
import game_functions as gf
import ai_method as aim


class AI_Player:
    def __init__(self, game_settings):
        self.game_settings = game_settings

    def move(self, board, screen):
        # col, _ = aim.alpha_beta_pruning(self.game_settings, board.game_board, 4, -math.inf, math.inf, True)
        col, _ = aim.mini_max(self.game_settings, board.game_board, 2, True)

        if gf.is_valid_location(self.game_settings, board.game_board, col):
            pygame.time.wait(500)
            # row = gf.get_next_open_row(self.game_settings, board.game_board, col)
            # gf.drop_piece(board.game_board, row, col, self.game_settings.AI_PIECE)
            #
            # if gf.winning_move(self.game_settings, board.game_board, self.game_settings.AI_PIECE):
            #     my_font = pygame.font.SysFont("monospace", 75)
            #     label = my_font.render("AI wins!!", 2, self.game_settings.YELLOW)
            #     screen.blit(label, (40, 10))
            #     self.game_settings.game_over = True
            #
            # board.print_board()
            # board.draw_board(screen)
            #
            # self.game_settings.turn += 1
            # self.game_settings.turn = self.game_settings.turn % 2

            gf.detect_game_over(self.game_settings, board, screen, col, self.game_settings.AI_PIECE)
