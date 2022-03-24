from game_scenery.tiles import Tile
from utils import TILE_SIZE

class Level:
    def __init__(self, level_data, surface, group):
        self.display_surface = surface
        self.group = group
        self.setup_level(level_data)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == 'X':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    tile = Tile((x, y), TILE_SIZE)
                    self.group.add(tile)

