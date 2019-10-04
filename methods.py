import math
import random
import time

class Methods:
    def __init__(self):
        self.valid_locations = []

########################################################################################################################
# minimax

    def mini_max(self, game, depth, maximizing_player):

        self.valid_locations = game.get_valid_locations()
        is_terminal = game.is_terminal_node()
        if depth == 0:
            return None, 0
        if is_terminal:
            if game.winning_move(game.AI_PIECE):
                print("AI wins: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", 10 + depth)
                return None, 10 + depth
            elif game.winning_move(game.PLAYER_PIECE):
                print("PLAYER wins: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", -depth - 10)
                return None, -depth - 10
            else:
                print("draw: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", 0)
                return None, 0  # Game is over, no more valid moves

        if maximizing_player:
            value = -math.inf
            best_loc = self.valid_locations[0]
            for valid_location in self.valid_locations:
                b_copy = game.Clone()
                b_copy.drop_piece(valid_location, b_copy.AI_PIECE)
                _, new_score = self.mini_max(b_copy, depth - 1, False)
                # print("maximizing_player: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", new_score)
                if new_score > value:
                    value = new_score
                    best_loc = valid_location
            return best_loc, value
        else:  # Minimizing player
            value = math.inf
            best_loc = self.valid_locations[0]
            for valid_location in self.valid_locations:
                b_copy = game.Clone()
                b_copy.drop_piece(valid_location, b_copy.PLAYER_PIECE)
                _, new_score = self.mini_max(b_copy, depth - 1, True)
                # print("minimizing_player: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", new_score)
                if new_score < value:
                    value = new_score
                    best_loc = valid_location
            return best_loc, value

########################################################################################################################
# alpha-beta-pruning

    def alpha_beta_pruning(self, game, depth, alpha, beta, maximizing_player):
        self.valid_locations = game.get_valid_locations()
        is_terminal = game.is_terminal_node()
        if depth == 0:
            return None, 0
        if is_terminal:
            if game.winning_move(game.AI_PIECE):
                print("AI wins: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", 10 + depth)
                return None, 10 + depth
            elif game.winning_move(game.PLAYER_PIECE):
                print("PLAYER wins: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", -depth - 10)
                return None, -depth - 10
            else:
                print("draw: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", 0)
                return None, 0  # Game is over, no more valid moves

        if maximizing_player:
            value = -math.inf
            best_loc = self.valid_locations[0]
            for valid_location in self.valid_locations:
                b_copy = game.Clone()
                b_copy.drop_piece(valid_location, b_copy.AI_PIECE)
                _, new_score = self.alpha_beta_pruning(b_copy, depth - 1, alpha, beta, False)
                # print("maximizing_player: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", new_score)
                if new_score > value:
                    value = new_score
                    best_loc = valid_location
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return best_loc, value
        else:  # Minimizing player
            value = math.inf
            best_loc = self.valid_locations[0]
            for valid_location in self.valid_locations:
                b_copy = game.Clone()
                b_copy.drop_piece(valid_location, b_copy.PLAYER_PIECE)
                _, new_score = self.alpha_beta_pruning(b_copy, depth - 1, alpha, beta, True)
                # print("minimizing_player: ", "depth = ", depth, ", is_terminal = ", is_terminal, ", new_score = ", new_score)
                if new_score < value:
                    value = new_score
                    bets_loc = valid_location
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return bets_loc, value

    ########################################################################################################################
    # monte carlo

    def monte_carlo(self, game, max_time):
        reward = 20
        start_time = time.process_time()
        self.valid_locations = game.get_valid_locations()
        print("valid locations: ", self.valid_locations)
        scores = [0] * len(self.valid_locations)
        # print("Initial scores: ", scores)
        imax = len(self.valid_locations)
        print("imax = ", imax)
        i = -1
        k = 0
        elapsed_time = time.process_time() - start_time
        while elapsed_time <= max_time:
            # print("============================================================")
            k += 1
            # print("k = ", k)
            i += 1
            if i == imax:
                i = 0
            # print("i = ", i)
            board_copy = game.Clone()
            current_location = self.valid_locations[i]
            board_copy.drop_piece(current_location, board_copy.AI_PIECE)
            #board_copy.print_board()
            board_copy.turn += 1
            board_copy.turn = board_copy.turn % 2
            #print("board_copy.turn = ", board_copy.turn)
            is_terminal = board_copy.is_terminal_node()
            # print(is_terminal)
            while not is_terminal:
                valid_locations = board_copy.get_valid_locations()
                #print(valid_locations)
                valid_location = random.choice(valid_locations)
                #print(valid_location)
                if board_copy.turn == board_copy.AI:
                    board_copy.drop_piece(valid_location, board_copy.AI_PIECE)
                    #print("AI: board_copy.turn = ", board_copy.turn)
                else:
                    board_copy.drop_piece(valid_location, board_copy.PLAYER_PIECE)
                    #print("HM: board_copy.turn = ", board_copy.turn)
                #board_copy.print_board()
                board_copy.turn += 1
                board_copy.turn = board_copy.turn % 2
                is_terminal = board_copy.is_terminal_node()
                #print(is_terminal)
            if board_copy.winning_move(game.AI_PIECE):
                scores[i] += (reward - board_copy.depth)
                # scores[i] += reward
            elif board_copy.winning_move(game.PLAYER_PIECE):
                scores[i] -= (reward + board_copy.depth)
                # scores[i] -= reward
            elapsed_time = time.process_time() - start_time
        print("Final scores: ", scores)
        print("Depth: ", board_copy.depth)
        probability = [x / (k * reward) for x in scores]
        print("Probability: ", probability)
        max_index = scores.index(max(scores))
        #print("max_index: ", max_index)
        # max_index = np.where(scores == np.max(scores))
        if type(max_index) is not int:
            max_index = random.choice(max_index)
        print("AI made a decision in %.2f seconds after playing %d games" % (elapsed_time, k))
        best_loc = self.valid_locations[max_index]
        print("Best AI move: ", best_loc)
        return best_loc, scores[max_index]


    # # monte carlo
    #
    # def monte_carlo(self, game, max_time):
    #     reward = 100
    #     start_time = time.process_time()
    #     self.valid_locations = game.get_valid_locations()
    #     scores = [0] * len(self.valid_locations)
    #     # print("Initial scores: ", scores)
    #     imax = len(self.valid_locations)
    #     # print("imax = ", imax)
    #     i = -1
    #     k = 0
    #     # print("game.turn = ", game.turn)
    #     elapsed_time = time.process_time() - start_time
    #     while elapsed_time <= max_time:
    #         # print("============================================================")
    #         k += 1
    #         # print("k = ", k)
    #         i += 1
    #         if i == imax:
    #             i = 0
    #         # print("i = ", i)
    #         board_copy = game.Clone()
    #         column = self.valid_locations[i]
    #         row = board_copy.get_next_open_row(column)
    #         board_copy.drop_piece(row, column, board_copy.AI_PIECE)
    #         #board_copy.print_board()
    #         board_copy.turn += 1
    #         board_copy.turn = board_copy.turn % 2
    #         #print("board_copy.turn = ", board_copy.turn)
    #         is_terminal = board_copy.is_terminal_node()
    #         # print(is_terminal)
    #         while not is_terminal:
    #             valid_locations = board_copy.get_valid_locations()
    #             #print(valid_locations)
    #             valid_location = random.choice(valid_locations)
    #             #print(valid_location)
    #             column = valid_location
    #             row = board_copy.get_next_open_row(column)
    #             if board_copy.turn == board_copy.AI:
    #                 board_copy.drop_piece(row, column, board_copy.AI_PIECE)
    #                 #print("AI: board_copy.turn = ", board_copy.turn)
    #             else:
    #                 board_copy.drop_piece(row, column, board_copy.PLAYER_PIECE)
    #                 #print("HM: board_copy.turn = ", board_copy.turn)
    #             #board_copy.print_board()
    #             board_copy.turn += 1
    #             board_copy.turn = board_copy.turn % 2
    #             is_terminal = board_copy.is_terminal_node()
    #             #print(is_terminal)
    #         if board_copy.winning_move(game.AI_PIECE):
    #             scores[i] += (reward - board_copy.depth)
    #         elif board_copy.winning_move(game.PLAYER_PIECE):
    #             scores[i] -= (reward + board_copy.depth)
    #         elapsed_time = time.process_time() - start_time
    #
    #     print("Final scores: ", scores)
    #     probability = [x / (k * reward) for x in scores]
    #     print("Probability: ", probability)
    #     max_index = scores.index(max(scores))
    #     #print("max_index: ", max_index)
    #     # max_index = np.where(scores == np.max(scores))
    #     if type(max_index) is not int:
    #         max_index = random.choice(max_index)
    #     print("Best AI move: ", max_index)
    #     print("AI made a decision in %.2f seconds after playing %d games" % (elapsed_time, k))
    #     best_column = self.valid_locations[max_index]
    #     best_row = game.get_next_open_row(best_column)
    #     return best_row, best_column