import os
import pygame as pg

from utils import ASSETS_DIR

def load_sprite(folder_name, scale = 1):
    '''
    Function that loads a sprite from a specified file, and returns both the
    image object, and the 
    :param folder_name: folder name of the entity that will be loaded.
    :type folder_name: string.
    :param scale: scale for the image.
    :type scale: float.
    :rtype: list, rect.
    
    '''
    # Get the full path name and load the image
    entity_folder = os.path.join(ASSETS_DIR, folder_name)
    animation_folders = os.listdir(entity_folder)

    # Set the list that will have all the animations for the entity
    animation_set = {}
    temp_key = animation_folders[0]

    # Load the frames into a list, and that list onto another list
    for folder in animation_folders:
        current_animation = []
        current_folder = os.path.join(entity_folder, folder)

        for file in os.listdir(current_folder):
            current_animation.append(pg.image.load(os.path.join(current_folder, file)).convert_alpha())
            last_index = len(current_animation) - 1
            
            # Scale the image
            size = current_animation[last_index].get_size()
            size = (size[0] * scale, size[1] * scale)
            current_animation[last_index] = pg.transform.scale(current_animation[last_index], size)

        animation_set[folder] = current_animation

    return animation_set, animation_set[temp_key][0].get_rect()

#def load_sound(file_name):

class Button(pg.sprite.Sprite):
    '''
    Class that represents a button.
    '''
    def __init__(self, x, y, text, window):
        super().__init__()
        self.x = x
        self.y = y
        self.text = text
        self.window = window

        self.font = pg.font.SysFont('Constantia', 30)
        self.text_col = pg.Color('black')
        
        self.mousePos = pg.mouse.get_pos()
        self.sprites, self.rect = load_sprite('buttons')
        self.image = self.sprites['default'][0]

        self.clicked = False
        self.action = False

    def draw_button(self):

        self.action = False
        self.rect.midbottom = (self.x, self.y)

        if self.rect.collidepoint(self.mousePos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.image = self.sprites['pressed'][0]
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                self.action = True
            #else:
            # Hover button behavior  

        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.window.blit(text_img, (self.x + int(self.rect.width/2) - int(text_len/2), self.y + 5))
        return self.action


