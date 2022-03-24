import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.img = pg.image.load('assets/terrain/grass.png').convert_alpha()
        self.image = pg.transform.scale(self.img, (size, size))
        self.rect = self.image.get_rect(topleft = pos)