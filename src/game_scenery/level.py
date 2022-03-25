import pygame as pg
from tiles import Tile, StaticTile
from resources import importCsvLayout, importCutGraphics
from utils import TILE_SIZE

class Level:
    '''
    Class that represents the game level.
    
    '''
    def __init__(self, levelData, surface):
        '''
        Level class' constructor.
        :param levelData: data to create the level layout and tiles.
        :type levelData: .tmx file.
        :param surface: surface to display the draw the level.
        :type surface: pygame Surface.
        
        '''
        self.displaySurface = surface
        
        # Layout moving speed
        self.worldShift = 0
        
        # Terrain variables
        self.terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(self.terrainLayout, 'terrain')

    def createTileGroup(self, layout, type):
        '''
        Function that creates a group of tile sprites.
        :param layout: the tile's layout.
        :type layout: list.
        :param type: the tile's type.
        :type type: string.
        :rtype: pygame sprite group.
        
        '''
        spriteGroup =  pg.sprite.Group()

        # Read the layout and add to the sprite group
        for rowIndex, row in enumerate(layout):
            for colIndex, val in enumerate(row):
                if val != '-1':
                    x = colIndex * TILE_SIZE
                    y = rowIndex * TILE_SIZE

                    # Add terrain tiles to the sprite group
                    if type == 'terrain':
                        terrainTileList = importCutGraphics('TODO')
                        tileSurface = terrainTileList[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tileSurface)
                        spriteGroup.add(sprite)
        
        return spriteGroup

    def run(self):
        '''
        Function that runs the level.

        '''
        self.terrainSprites.draw(self.displaySurface)
        self.terrainSprites.update(self.worldShift)
        