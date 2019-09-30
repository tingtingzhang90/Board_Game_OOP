import random


class Settings():
    """A class to store all the settings"""

    def __init__(self):
        # Declaration of colors
        self.BLUE = (0, 0, 255)  # RGB value
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        # Size of the board
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7

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

        self.RADIUS = int(self.SQUARESIZE / 2 - 5)

        self.size = (self.width, self.height)

        self.pos_x = 0
