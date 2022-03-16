import os

from numpy import append

WIDTH = 800 # Screen's width
HEIGHT = 600 # Screen's height
BLACK = (0,0,0) # Black color

BASE_PATH = os.path.abspath(os.path.join(os.path.abspath(os.path.join(__file__, os.pardir)), os.pardir))
ASSETS_DIR = os.path.join(BASE_PATH, 'assets')