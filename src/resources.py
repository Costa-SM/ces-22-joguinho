import os
import pygame as pg

from utils import ASSETS_DIR

def load_sprite(file_name, colorkey = None, scale = 1):
    '''
    Function that loads a sprite from a specified file, and returns both the
    image object, and the 
    :param file_name: file name of the image that will be loaded.
    :type file_name: string.
    :param colorkey: 
    :type colorkey: float.
    :param scale: scale for the image.
    :type scale: float.
    
    '''
    # Get the full path name and load the image
    full_name = os.path.join(ASSETS_DIR, file_name)
    image = pg.image.load(full_name).convert()

    # Scale the image 
    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)

    return image, image.get_rect()


#def load_sound(file_name):

