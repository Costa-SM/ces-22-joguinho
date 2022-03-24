import pygame as pg
from game_scenery.tiles import Tile
from utils import TILE_SIZE
from game_entities.fultano import Fultano
from game_entities.monster import Monster

class Level:
    def __init__(self, level_data, surface, group):
        self.tiles = pg.sprite.Group()
        self.display_surface = surface
        self.group = group
        self.setup_level(level_data)
        self.fultano = Fultano(200, 600 - TILE_SIZE, self.tiles)
        self.monster = Monster(500, 600 - 86 - TILE_SIZE)
        self.group.add(self.fultano)
        self.group.add(self.monster)

    def setup_level(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col == 'X':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    tile = Tile((x, y), TILE_SIZE)
                    self.group.add(tile)
                    self.tiles.add(tile)

    def run(self):
        self.group.custom_draw(self.fultano)
