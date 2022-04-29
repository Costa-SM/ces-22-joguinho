import pygame as pg
import os
from csv import reader
from utils import TILE_SIZE, BASE_PATH

def import_folder(path):
    '''
    Function that imports files into a folder.
    :param path: the folder path
    :type path: string
    :rtype: list

    '''
    surface_list = []
    for _, __, image_files in os.walk(path):
        image_files.sort()
        for image in image_files:
            full_path = path + '/' + image
            image_surf = pg.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def import_csv_layout(path):
    '''
    Function that imports .csv level layout.
    :param path: the .csv file path
    :type path: string
    :rtype: list

    '''
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter = ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path):
    '''
    Function that cuts tiles.
    :param path: the tile png path
    :type path: string
    :rtype: list

    '''
    surface = pg.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILE_SIZE)
    tile_num_y = int(surface.get_size()[1] / TILE_SIZE)
    # Create the cutted tiles list
    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILE_SIZE
            y = row * TILE_SIZE
            new_surf = pg.Surface((TILE_SIZE, TILE_SIZE), flags = pg.SRCALPHA)
            new_surf.blit(surface, (0, 0), pg.Rect(x, y, TILE_SIZE, TILE_SIZE))
            cut_tiles.append(new_surf)
    return cut_tiles

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
        self.font_dir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
        self.font = pg.font.Font(self.font_dir, 30)
        self.text_col = pg.Color('black')
        # Window variables
        self.window = window
        self.mouse_pos = pg.mouse.get_pos()
        # Button image
        if self.size == 'normal':   
            self.sprites = import_folder(os.path.join(BASE_PATH, 'assets/buttons/normal_buttons'))
        elif self.size == 'large':
            self.sprites = import_folder(os.path.join(BASE_PATH,'assets/buttons/large_buttons'))
        self.image = self.sprites[0]
        self.rect = self.image.get_rect(center = (x,y))
        # Button logic
        self.clicked = False
        self.action = False

    def draw_button(self):
        '''
        Draws the button.
        :rtype: bool
        
        '''
        # Update parameters
        self.action = False
        self.rect.center = (self.x, self.y)
        self.mouse_pos = pg.mouse.get_pos()
        # Click logic
        if self.rect.collidepoint(self.mouse_pos):
            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.image = self.sprites[1]
            elif pg.mouse.get_pressed()[0] == 0 and self.clicked == True:
                if self.rect.collidepoint(self.mouse_pos):
                    self.clicked = False
                    self.action = True
        # Drawing on the window
        button_sprite = pg.sprite.Group()
        button_sprite.add(self)
        button_sprite.draw(self.window)
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.window.blit(text_img, (self.x - self.rect.width/4 - text_len/6, self.y - self.rect.height/4))
        return self.action

def tutorial(window):
    '''
    Write the games' tutorial on the window.
    param: window: game window
    type window: pg.display
        
    '''
    # Set font and draw the text
    font_dir = os.path.join(BASE_PATH, 'fonts/manaspc.ttf')
    font = pg.font.Font(font_dir, 30)
    text_col = pg.Color('white')
    text_img = font.render("Welcome!", True, text_col)
    text_len = text_img.get_width()
    window.blit(text_img, (500 - text_len/2, 100))
    font = pg.font.Font(font_dir, 20)
    text_img = font.render("Use arrow keys to move yourself", True, text_col)
    text_len = text_img.get_width()
    window.blit(text_img, (500 - text_len/2, 150))
    text_img = font.render("Use C, F or V to attack", True, text_col)
    text_len = text_img.get_width()
    window.blit(text_img, (500 - text_len/2, 200))
    text_img = font.render("Go ahead and get to the end of each level to win", True, text_col)
    text_len = text_img.get_width()
    window.blit(text_img, (500 - text_len/2, 250))
 