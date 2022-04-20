import os

TILE_SIZE = 50
VERTICAL_TILE_NUMBER = 12

SCREEN_HEIGHT = VERTICAL_TILE_NUMBER * TILE_SIZE
SCREEN_WIDTH = 1000

FULTANO_HEALTH = 50

BASE_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir))
ASSETS_DIR = os.path.join(BASE_PATH, 'assets')