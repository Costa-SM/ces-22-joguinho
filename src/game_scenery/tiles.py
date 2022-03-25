import pygame as pg

class Tile(pg.sprite.Sprite):
    def __init__(self, pos, size, type):
        super().__init__()
        if type == '1':
            self.img = pg.image.load('assets/terrain/Tile (1).png').convert_alpha()
        elif type == '2':
            self.img = pg.image.load('assets/terrain/Tile (2).png').convert_alpha()
        elif type == '3':
            self.img = pg.image.load('assets/terrain/Tile (3).png').convert_alpha()
        elif type == '4':
            self.img = pg.image.load('assets/terrain/Tile (4).png').convert_alpha() 
        elif type == '5':
            self.img = pg.image.load('assets/terrain/Tile (5).png').convert_alpha()
        elif type == '6':
            self.img = pg.image.load('assets/terrain/Tile (6).png').convert_alpha() 
        elif type == '7':
            self.img = pg.image.load('assets/terrain/Tile (7).png').convert_alpha()
        elif type == '8':
            self.img = pg.image.load('assets/terrain/Tile (8).png').convert_alpha() 
        elif type == '9':
            self.img = pg.image.load('assets/terrain/Tile (9).png').convert_alpha()
        elif type == 'A':
            self.img = pg.image.load('assets/terrain/Tile (10).png').convert_alpha()
        elif type == 'B':
            self.img = pg.image.load('assets/terrain/Tile (11).png').convert_alpha()
        elif type == 'C':
            self.img = pg.image.load('assets/terrain/Tile (12).png').convert_alpha() 
        elif type == 'D':
            self.img = pg.image.load('assets/terrain/Tile (13).png').convert_alpha()
        elif type == 'E':
            self.img = pg.image.load('assets/terrain/Tile (14).png').convert_alpha() 
        elif type == 'F':
            self.img = pg.image.load('assets/terrain/Tile (15).png').convert_alpha()
        elif type == 'G':
            self.img = pg.image.load('assets/terrain/Tile (16).png').convert_alpha() 
            
        self.image = pg.transform.scale(self.img, (size, size))
        self.rect = self.image.get_rect(topleft = pos)