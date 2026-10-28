#Creating a fruit.
#Storing its position.
#Defining its appearance.

import random
import settings



class Fruit:
    def __init__(self, occupied_positions):
        self.position = self.random_position(occupied_positions) #looks to see if a position is already taken up

    def random_position(self, occupied_positions):
        columns = settings.WINDOW_WIDTH // settings.CELL_SIZE
        rows = settings.PLAY_AREA_HEIGHT // settings.CELL_SIZE

        first_playable_row = settings.MARGIN_HEIGHT // settings.CELL_SIZE #stops the fruit from spawning in the margin
        available_positions = []

        for row in range(first_playable_row, first_playable_row + rows):
            for column in range(columns):
                position = (column, row)

                if position not in occupied_positions:
                    available_positions.append(position)

        if not available_positions:
            return None

        return random.choice(available_positions)

    def respawn(self, occupied_positions):
        self.position = self.random_position(occupied_positions)