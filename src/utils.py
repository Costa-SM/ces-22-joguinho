import os

# Level constants
TILE_SIZE = 50
VERTICAL_TILE_NUMBER = 12
# Screen constants
SCREEN_HEIGHT = VERTICAL_TILE_NUMBER * TILE_SIZE
SCREEN_WIDTH = 1000
# Game Constants
FULTANO_HEALTH = 8
# Paths
BASE_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir))
ASSETS_DIR = os.path.join(BASE_PATH, 'assets')