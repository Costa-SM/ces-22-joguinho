import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        if type == 'X':
            self.img = pg.image.load('assets/terrain/dark_grass.png').convert_alpha()
        if type == 'Y':
            self.img = pg.image.load('assets/terrain/dark_dirt.png').convert_alpha()    
        self.image = pg.transform.scale(self.img, (size, size))
        self.rect = self.image.get_rect(topleft = pos)