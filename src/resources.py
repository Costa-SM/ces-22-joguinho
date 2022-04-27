import pygame as pg
import os
from csv import reader
from utils import TILE_SIZE, BASE_PATH

def importFolder(path):
    '''
    Function that imports files into a folder.
    :param path: the folder path
    :type path: string
    :rtype: list

    '''
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
    Function that imports .csv level layout.
    :param path: the .csv file path
    :type path: string
    :rtype: list

    '''
    terrainMap = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrainMap.append(list(row))
        return terrainMap

def importCutGraphics(path):
    '''
    Function that cuts tiles.
    :param path: the tile png path
    :type path: string
    :rtype: list

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
        '''
        Button constructor.
        
        '''
        super().__init__()
        # Button positions and size
        self.x = x
        self.y = y
        self.size = size
        # Button text and font
        self.text = text
        self.fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
        self.font = pg.font.Font(self.fontDir, 30)
        self.textCol = pg.Color('black')
        # Window variables
        self.window = window
        self.mousePos = pg.mouse.get_pos()
        # Button image
        if self.size == 'normal':   
            self.sprites = importFolder(os.path.join(BASE_PATH, 'assets/buttons/normal_buttons'))
        elif self.size == 'large':
            self.sprites = importFolder(os.path.join(BASE_PATH,'assets/buttons/large_buttons'))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center = (x,y))
        # Button logic
        self.clicked = False
        self.action = False

    def drawButton(self):
        '''
        Draws the button.
        :rtype: bool
        
        '''
        # Update parameters
        self.action = False
        self.rect.center = (self.x, self.y)
        self.mousePos = pg.mouse.get_pos()
        # Click logic
        if self.rect.collidepoint(self.mousePos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.image = self.sprites[1]
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                if self.rect.collidepoint(self.mousePos):
                    self.clicked = False
                    self.action = True
        # Drawing on the window
        buttonSprite = pg.sprite.Group()
        buttonSprite.add(self)
        buttonSprite.draw(self.window)
        textImg = self.font.render(self.text, True, self.textCol)
        textLen = textImg.get_width()
        self.window.blit(textImg, (self.x - self.rect.width/4 - textLen/6, self.y - self.rect.height/4))
        return self.action

def tutorial(window):
    '''
    Write the games' tutorial on the window.
    param: window: game window
    type window: pg.display
        
    '''
    # Set font and draw the text
    fontDir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    font = pg.font.Font(fontDir, 30)
    textCol = pg.Color('white')
    textImg = font.render("Welcome!", True, textCol)
    textLen = textImg.get_width()
    window.blit(textImg, (500 - textLen/2, 100))
    font = pg.font.Font(fontDir, 20)
    textImg = font.render("Use arrow keys to move yourself", True, textCol)
    textLen = textImg.get_width()
    window.blit(textImg, (500 - textLen/2, 150))
    textImg = font.render("Use C, F or V to attack", True, textCol)
    textLen = textImg.get_width()
    window.blit(textImg, (500 - textLen/2, 200))
    textImg = font.render("Go ahead and get to the end of each level to win", True, textCol)
    textLen = textImg.get_width()
    window.blit(textImg, (500 - textLen/2, 250))
 