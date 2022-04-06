import pygame as pg
import os
from csv import reader

from utils import TILE_SIZE, BASE_PATH

def importFolder(path):
    surfaceList = []

    for _, __, imageFiles in os.walk(path):
        imageFiles.sort()

        for image in imageFiles:
            fullPath = path + '/' + image
            imageSurf = pg.image.load(fullPath).convert_alpha()
            surfaceList.append(imageSurf)

    return surfaceList

def importCsvLayout(path):
    '''
    Function that imports our .csv level layout
    :param path: the .csv file path.
    :type levelData: string.
    :rtype: list.

    '''
    terrainMap = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrainMap.append(list(row))
        return terrainMap

def importCutGraphics(path):
    '''
    Function that cuts tiles
    :param path: the tile png path.
    :type levelData: string.
    :rtype: list.

    '''
    surface = pg.image.load(path).convert_alpha()
    tileNumX = int(surface.get_size()[0] / TILE_SIZE)
    tileNumY = int(surface.get_size()[1] / TILE_SIZE)

    # Create the cutted tiles list
    cutTiles = []
    for row in range(tileNumY):
        for col in range(tileNumX):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            newSurf = pg.Surface((TILE_SIZE, TILE_SIZE), flags = pg.SRCALPHA)
            newSurf.blit(surface, (0, 0), pg.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cutTiles.append(newSurf)

    return cutTiles

class Button(pg.sprite.Sprite):
    '''
    Class that represents a button.
    '''
    def __init__(self, x, y, text, window, size):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.window = window
        self.size = size
        self.fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
        self.font = pg.font.Font(self.fontDir, 30)
        self.text_col = pg.Color('black')
        
        self.mousePos = pg.mouse.get_pos()
        if self.size == 'normal':   
            self.sprites = importFolder(os.path.join(BASE_PATH, 'assets/buttons/normal_buttons'))
        elif self.size == 'large':
            self.sprites = importFolder(os.path.join(BASE_PATH,'assets/buttons/large_buttons'))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center = (x,y))

        self.clicked = False
        self.action = False

    def draw_button(self):

        self.action = False
        self.rect.center = (self.x, self.y)
        self.mousePos = pg.mouse.get_pos()
        if self.rect.collidepoint(self.mousePos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.image = self.sprites[1]
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                if self.rect.collidepoint(self.mousePos):
                    self.clicked = False
                    self.action = True
            #else:
            # Hover button behavior  
        buttonSprite = pg.sprite.Group()
        buttonSprite.add(self)
        buttonSprite.draw(self.window)
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.window.blit(text_img, (self.x - self.rect.width/4 - text_len/6, self.y - self.rect.height/4))

        return self.action