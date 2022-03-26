import pygame as pg
import sys
from game_scenery.level import Level
from game_scenery.game_data import level_1
from utils import *

pg.init()

class Game():
    '''
    Class that represents the game engine.
    
    '''

    def __init__(self) -> None:
        '''
        Game class' constructor.
        
        '''
        self.initScreen()
        self.initVariables()

    def initVariables(self):
        '''
        Function that initializes the game variables.
        
        '''
        self.clock = pg.time.Clock()
        self.level = Level(level_1, self.screen)

    def initScreen(self):
        '''
        Function that initializes the game window.
        
        '''
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    
    def update(self):
        '''
        Function that updates the game.
        
        '''
        # Event handler.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        
        # Background
        self.screen.fill('grey')
        
        # Level loading
        self.level.run()

        # Screen update
        pg.display.update()
        self.clock.tick(60)

    def render(self):
        '''
        Function that renders the game images on the screen.
        
        '''  
        pass

    def play(self):
        '''
        Main function.
        
        '''
        self.update()
        self.render()