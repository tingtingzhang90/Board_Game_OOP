import pygame
import sys
import random


def check_event(game_settings, board, screen, player, ai_player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, game_settings.BLACK, (0, 0, game_settings.width, game_settings.SQUARESIZE))
            game_settings.pos_x = event.pos[0]
            if game_settings.turn == game_settings.PLAYER:
                pygame.draw.circle(screen, game_settings.RED, (game_settings.pos_x, int(game_settings.SQUARESIZE / 2)),
                                   game_settings.RADIUS)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, game_settings.BLACK, (0, 0, game_settings.width, game_settings.SQUARESIZE))
            # print(event.pos)

            if game_settings.turn == game_settings.PLAYER:
                player.move(board, screen)

    if game_settings.turn == game_settings.AI and not game_settings.game_over:
        ai_player.move(board, screen)


def drop_piece(game_board, row, col, piece):
    game_board[row][col] = piece


def is_valid_location(game_settings, game_board, col):
    return game_board[game_settings.ROW_COUNT - 1][col] == 0


def get_next_open_row(game_settings, game_board, col):
    for r in range(game_settings.ROW_COUNT):
        if game_board[r][col] == 0:
            return r


def winning_move(game_settings, game_board, piece):
    # Check horizontal locations for win
    for c in range(game_settings.COLUMN_COUNT - 3):
        for r in range(game_settings.ROW_COUNT):
            if game_board[r][c] == piece and game_board[r][c+1] == piece and game_board[r][c + 2] == piece \
                    and game_board[r][c + 3] == piece:
                return True

    # Check verticl locations for win
    for r in range(game_settings.ROW_COUNT - 3):
        for c in range(game_settings.COLUMN_COUNT):
            if game_board[r][c] == piece and game_board[r + 1][c] == piece and game_board[r + 2][c] == piece \
                    and game_board[r + 3][c] == piece:
                return True

                # Check positively sloped diaganols
    for c in range(game_settings.COLUMN_COUNT -3):
        for r in range(game_settings.ROW_COUNT - 3):
            if game_board[r][c] == piece and game_board[r + 1][c + 1] == piece and game_board[r + 2][c + 2] == piece \
                    and game_board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(game_settings.COLUMN_COUNT - 3):
        for r in range(3, game_settings.ROW_COUNT):
            if game_board[r][c] == piece and game_board[r - 1][c + 1] == piece and game_board[r - 2][c + 2] == piece \
                    and game_board[r - 3][c + 3] == piece:
                return True


def get_valid_location(game_settings, game_board):
    valid_locations = []
    for col in range(game_settings.COLUMN_COUNT):
        if is_valid_location(game_settings, game_board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_movie(game_settings, game_board, piece):
    best_score = 0
    valid_locations = get_valid_location(game_settings, game_board)
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(game_settings, game_board, col)
        temp_board = game_board.copy()

        drop_piece(temp_board, row, col, piece)
        score = score_position(game_settings, temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col


def evaluate_window(game_settings, window, piece):
    score = 0
    opp_piece = game_settings.PLAYER_PIECE
    if piece == game_settings.PLAYER_PIECE:
        opp_piece = game_settings.AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(game_settings.EMPTY) == 1:
        score += 10
    elif window.count(piece) == 2 and window.count(game_settings.EMPTY) == 2:
        score += 5

    if window.count(opp_piece) == 3 and window.count(game_settings.EMPTY) == 1:
        score -= 80
    return score


def score_position(game_settings, game_board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(game_board[:, game_settings.COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 6

    # Score horizontal
    for r in range(game_settings.ROW_COUNT):
        row_array =[int(i) for i in list(game_board[r, :])]
        for c in range(game_settings.COLUMN_COUNT - 3):
            window = row_array[c: c + game_settings.WINDOW_LENGTH]
            score += evaluate_window(game_settings, window, piece)
    # Score vertical
    for c in range(game_settings.COLUMN_COUNT):
        col_array = [int(i) for i in list(game_board[:, c])]
        for r in range(game_settings.ROW_COUNT - 3):
            window = col_array[r : r + game_settings.WINDOW_LENGTH]
            score += evaluate_window(game_settings, window, piece)

    # Score positive sloped diagonal
    for r in range(game_settings.ROW_COUNT - 3):
        for c in range(game_settings.COLUMN_COUNT - 3):
            window = [game_board[r + i][c + i] for i in range(game_settings.WINDOW_LENGTH)]
            score += evaluate_window(game_settings, window, piece)

    # Score negative sloped diagonal
    for r in range(game_settings.ROW_COUNT - 3):
        for c in range(game_settings.COLUMN_COUNT - 3):
            window = [game_board[r + 3 - i][c + i] for i in range(game_settings.WINDOW_LENGTH)]
            score += evaluate_window(game_settings, window, piece)
    return score


def is_terminal_node(game_settings, game_board):
    return winning_move(game_settings, game_board, game_settings.PLAYER_PIECE) \
           or winning_move(game_settings, game_board, game_settings.AI_PIECE) \
           or len(get_valid_location(game_settings, game_board)) == 0


def detect_game_over(game_settings, board, screen, col, piece):
    row = get_next_open_row(game_settings, board.game_board, col)
    drop_piece(board.game_board, row, col, piece)

    my_font = pygame.font.SysFont("monospace", 75)

    if winning_move(game_settings, board.game_board, piece):
        if piece == game_settings.PLAYER_PIECE:
            label = my_font.render("Player 1 wins!!", 1, game_settings.RED)
        elif piece == game_settings.AI_PIECE:
            label = my_font.render("AI wins!!", 2, game_settings.YELLOW)
        else:
            label = my_font.render("It's a draw!!")
        screen.blit(label, (40, 10))

        game_settings.game_over = True

    board.print_board()
    board.draw_board(screen)

    game_settings.turn += 1
    game_settings.turn = game_settings.turn % 2


