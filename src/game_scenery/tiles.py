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
        self.image = pg.transform.scale(self.image, (100, 96))

    def animate(self):
        self.frameIndex += 0.15
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0 
        self.image = self.frames[int(self.frameIndex)]
        self.image = pg.transform.scale(self.image, (100, 96))

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pg.image.load('assets/world/terrain/Crate.png').convert_alpha())

class Decoration(StaticTile):
    def __init__(self, size, x, y, type):
        if type == '0':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Bone (1).png').convert_alpha())
        elif type == '1':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Bone (2).png').convert_alpha())
        elif type == '2':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Bone (3).png').convert_alpha())
        elif type == '3':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Bone (4).png').convert_alpha())
        elif type == '4':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Bush (1).png').convert_alpha())
        elif type == '5':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Bush (2).png').convert_alpha())
        elif type == '6':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/DeadBush.png').convert_alpha())
        elif type == '7':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Sign.png').convert_alpha())
        elif type == '8':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Skeleton.png').convert_alpha())
        elif type == '9':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/TombStone (1).png').convert_alpha())
        elif type == '10':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/TombStone (2).png').convert_alpha())
        elif type == '11':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/Tree.png').convert_alpha())
        elif type == '12':
            super().__init__(size, x, y, pg.image.load('assets/world/decoration/ArrowSign.png').convert_alpha())
        
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))

        