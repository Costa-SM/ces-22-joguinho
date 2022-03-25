import pygame as pg
from os import walk
from csv import reader

from utils import TILE_SIZE

def importFolder(path):
    surfaceList = []

    for _, __, imageFiles in walk(path):
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
    for row in range(tileNumX):
        for col in range(tileNumY):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            newSurf = pg.Surface((TILE_SIZE, TILE_SIZE))
            newSurf.blit(surface, (0, 0), pg.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cutTiles.append(newSurf)

    return cutTiles