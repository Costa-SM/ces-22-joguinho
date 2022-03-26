import pygame as pg
from game_scenery.tiles import AnimatedTile

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, 'assets/skeleton/run')
     #   self.rect.y += size - self.image.get_size()[1]