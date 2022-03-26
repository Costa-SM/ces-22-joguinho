import pygame as pg
from game_scenery.tiles import Decoration, Tile, StaticTile, AnimatedTile, Crate
from game_entities.enemy import Enemy
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
        self.worldShift = -5
        
        # Terrain variables
        self.terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(self.terrainLayout, 'terrain')

        # Decoration variables
        self.decorationLayout = importCsvLayout(levelData['bg_decoration'])
        self.decorationSprites = self.createTileGroup(self.decorationLayout, 'bg_decoration')

        # Crates
        self.crateLayout = importCsvLayout(levelData['crates'])
        self.crateSprites = self.createTileGroup(self.crateLayout, 'crates')

        # Skeletons
        self.skeletonLayout = importCsvLayout(levelData['skeleton'])
        self.skeletonSprites = self.createTileGroup(self.skeletonLayout, 'skeleton')

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
                        terrainTileList = importCutGraphics('assets/world/terrain/terrain_tiles.png')
                        tileSurface = terrainTileList[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tileSurface)
                        

                    if type == 'bg_decoration':
                        sprite = Decoration(TILE_SIZE, x, y, val)

                    # Crates
                    if type == 'crates':
                        sprite = Crate(TILE_SIZE, x, y)

                    if type == 'skeleton':
                        sprite = Enemy(TILE_SIZE, x, y)

                    spriteGroup.add(sprite)                       
        
        return spriteGroup

    def run(self):
        '''
        Function that runs the level.

        '''
        # Run terrain
        self.terrainSprites.update(self.worldShift)
        self.terrainSprites.draw(self.displaySurface)
        
        # Run decoration
        self.decorationSprites.update(self.worldShift)
        self.decorationSprites.draw(self.displaySurface)        

        # Run crates
        self.crateSprites.update(self.worldShift)
        self.crateSprites.draw(self.displaySurface)

        # Run enemies
        self.skeletonSprites.update(self.worldShift)
        self.skeletonSprites.draw(self.displaySurface)

        