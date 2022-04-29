import pygame as pg
import sys
from resources import tutorial
from menus import main, pause, death, authors, win
from game_scenery.level import Level
from game_scenery.game_data import level_0, level_1, level_2
from utils import *

# Initialize PyGame
pg.init()

class Game():
    '''
    Class that represents the game engine.
    
    '''
    def __init__(self) -> None:
        '''
        Game class' constructor.
        
        '''
        self.current_level = 0
        self.initScreen()
        self.init_variables()
        self.init_media()

    def init_variables(self):
        '''
        Function that initializes the game variables.
        
        '''
        # Time variables
        self.clock = pg.time.Clock()
        self.start_time = 0
        self.time_since_enter = 0
        # Game variables
        self.start = False
        self.dead = True
        self.credits = False
        self.paused = False
        self.restart = False
        # Levels variables
        self.levels = [level_0, level_1, level_2]
        self.level = Level(self.levels[self.current_level], self.screen)
        self.max_level = 2
        # Background song
        self.background_song = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/Fireside-Tales-MP3.mp3'))

    def initScreen(self):
        '''
        Function that initializes the game window.
        
        '''
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def init_media(self):
        '''
        Function that initializes the game sound.
        
        '''
        pg.mixer.init()
        chan1 = pg.mixer.Channel(1)
        chan1.queue(self.background_song)
        chan1.set_volume(0.1)  
    
    def update(self):
        '''
        Function that updates the game.
        
        '''
        # Main menu logic
        if not self.start:
            if self.level.advance_level == False:
                self.current_level = 0
            else:
                self.current_level = -1
            self.start, self.credits = main(self.start, self.screen, pg.time,  self.credits)
            if self.credits:
                self.start, self.credits = authors(self.screen)
                self.level.reset_level = False
            self.start_time = pg.time.get_ticks()
        self.time_since_enter = pg.time.get_ticks() - self.start_time
        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Pause menu logic
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.mixer.music.pause()
                self.paused = True
                self.paused = pause(self.paused, self.screen, pg.time)
        # Set background     
        self.screen.blit(pg.image.load(ASSETS_DIR + '/background/background_3.jpg'), (0,0))
        # Load level      
        if self.start:
            self.level.run()
        # Set tutorial
        if self.level.level_data == self.levels[0] and self.time_since_enter < 8000:
            tutorial(self.screen)
        # Check if level will reset
        if self.level.reset_level == True:
            # Pause music
            pg.mixer.music.pause()
            # Check if the player advanced the level
            if self.level.advance_level == True:
                self.current_level += 1
                # Check if the player reached the final level
                if self.current_level == self.max_level + 1:
                    # Show win screen
                    self.start = win(self.start, self.screen, pg.time)
                # Just initialize the next level
                else: 
                    self.init_variables()
                    self.start = True
            # If not, the player died     
            else:
                # Show death screen
                if self.dead == True:
                    self.start, self.restart, self.dead = death(self.start, self.screen, pg.time, self.restart, self.dead)
                # Initialize the level again
                else:
                    self.init_variables()
                    self.start = True
            # Restart game logic
            if self.restart == True:
                self.init_variables()
                self.start = True
            # Initialize game music
            self.init_media()
        # Screen and time update
        pg.display.update()
        self.clock.tick(60)

    def play(self):
        '''
        Main function.
        
        '''
        # Update the game
        self.update()