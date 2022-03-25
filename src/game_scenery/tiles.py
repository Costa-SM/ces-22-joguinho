from importlib import resources
import pygame as pg
from  resources import importFolder

class Tile(pg.sprite.Sprite):
    '''
    Class that represents a tile.
    
    '''
    def __init__(self, size, x, y):
        '''
        Tile class' constructor.
        :param size: tile size.
        :type size: int.
        :param x: tile x coordinate.
        :type x: int.
        :param y: tile y coordinate.
        :type y: int.
        
        '''
        super().__init__()
        self.image = pg.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, shift):
        '''
        Function that updates the tile's position.
        :param shift: shift lenght.
        :type size: int.
        '''
        self.rect.x += shift

class StaticTile(Tile):
    '''
    Class that represents a static tile.
    
    '''
    def __init__(self, size, x, y, surface):
        '''
        StaticTile class' constructor.
        :param size: tile size.
        :type size: int.
        :param x: tile x coordinate.
        :type x: int.
        :param y: tile y coordinate.
        :type y: int.
        :param surface: tile surface.
        :type surface: pygame surface.
        
        '''
        super().__init__(size, x, y)
        self.image = surface

class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = importFolder(path)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

    def animate(self):
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0 
        self.image = self.frames[int(self.frameIndex)]

    def update(self, shift):
        self.animate()
        self.rect.x += shift