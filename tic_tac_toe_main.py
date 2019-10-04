import pygame
import math
from tic_tac_toe import TicTacToe
from methods import Methods



def run_game():
    # Create a board
    game = TicTacToe()

    # Initialize the game and create a screen object
    pygame.init()
    screen = pygame.display.set_mode(game.size)
    pygame.display.set_caption("Tic Tac Toe")
    my_font = pygame.font.SysFont("monospace", 40)

    # Creat methods
    methods = Methods()

    # Print game board
    game.print_board()
    game.draw_board(screen)
    game.turn = 0

    # Start the main loop of the game
    while not game.game_over:
        pygame.display.update()

####################################### Tic Tac Toe ####################################################################
        turn = game.check_event(screen)
        if turn == game.PLAYER:
            row = int(math.floor(game.pos_y / game.SQUARESIZE))
            col = int(math.floor(game.pos_x / game.SQUARESIZE))
            h = game.ij2h(row, col)
            if game.is_valid_location(h):
                game.get_move(screen, h, game.PLAYER_PIECE)
        elif turn == game.AI:
            # best_loc, score = methods.mini_max(game, 0, True)
            best_loc, score = methods.alpha_beta_pruning(game, 7, -math.inf, math.inf, True)
            # best_loc, score = methods.monte_carlo(game, 2)
            game.get_move(screen, best_loc, game.AI_PIECE)
            print(best_loc, score)
########################################################################################################################

        if game.game_over:
            if game.winning_move(game.PLAYER_PIECE):
                label = my_font.render("Human wins!!", 1, game.RED)
                screen.blit(label, (50, 50))
                print("Human wins!!")
            elif game.winning_move(game.AI_PIECE):
                label = my_font.render("AI wins!!", 2, game.YELLOW)
                screen.blit(label, (50, 50))
                print("AI wins!!")
            else:
                label = my_font.render("It's a draw!!", 2, game.BLACK)
                screen.blit(label, (50, 50))
                print("It's a draw!!")

            pygame.display.update()
            pygame.time.wait(10000)


run_game()