import pygame

from settings import Settings
import game_functions as gf

from board import Board
from player import Player
from ai_player import AI_Player


def run_game():
    # Initialize the game and create a screen object
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(game_settings.size)
    pygame.display.set_caption("Connect4 Game")

    # Create a board
    board = Board(game_settings)
    board.print_board()

    # Creat players
    player = Player(game_settings)
    ai_player = AI_Player(game_settings)

    board.draw_board(screen)

    # Start the main loop of the game
    while not game_settings.game_over:
        pygame.display.update()

        gf.check_event(game_settings, board, screen, player, ai_player)

        if game_settings.game_over:
            pygame.time.wait(3000)


run_game()


