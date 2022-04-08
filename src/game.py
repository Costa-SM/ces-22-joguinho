from textwrap import dedent
import pygame as pg
import sys
from menus import main, pause, death
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
        self.initMedia()

    def initVariables(self):
        '''
        Function that initializes the game variables.
        
        '''
        self.clock = pg.time.Clock()
        self.start = False
        self.paused = False
        self.restart = False
        self.level = Level(level_1, self.screen)

    def initScreen(self):
        '''
        Function that initializes the game window.
        
        '''
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def initMedia(self):
        pg.mixer.init()
        pg.mixer.music.load(os.path.join(BASE_PATH, 'media/Fireside-Tales-MP3.mp3'))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)
    
    def update(self):
        '''
        Function that updates the game.
        
        '''

        if not self.start:
            self.start = main(self.start, self.screen, pg.time)
        # Event handler.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.mixer.music.pause()
                self.paused = True
                self.paused = pause(self.paused, self.screen, pg.time)
        
        # Background     
        self.screen.blit(pg.image.load(ASSETS_DIR + '/background/background_3.jpg'), (0,0))
        
        # Level loading
        self.level.run()

        # Check if level will reset

        if self.level.resetLevel == True:
            pg.mixer.music.pause()
            self.start, self.restart = death(self.start, self.screen, pg.time, self.restart)
            if self.restart:
                self.initVariables()
                self.start = True
            else:
                self.initVariables()
            self.initMedia()

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