import pygame as pg
import sys
from resources import tutorial
from menus import main, pause, death, authors, win
from game_scenery.level import Level
from game_scenery.game_data import level_0, level_1
from utils import *

# Initializing PyGame
pg.init()

class Game():
    '''
    Class that represents the game engine
    
    '''
    def __init__(self) -> None:
        '''
        Game class' constructor.
        
        '''
        self.currentLevel = 0
        self.initScreen()
        self.initVariables()
        self.initMedia()

    def initVariables(self):
        '''
        Function that initializes the game variables.
        
        '''
        # Time variables
        self.clock = pg.time.Clock()
        self.startTime = 0
        self.timeSinceEnter = 0
        # Game variables
        self.start = False
        self.dead = True
        self.credits = False
        self.paused = False
        self.restart = False
        # Levels variables
        self.levels = [level_0, level_1]
        self.level = Level(self.levels[self.currentLevel], self.screen)
        self.maxLevel = 1

    def initScreen(self):
        '''
        Function that initializes the game window.
        
        '''
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    def initMedia(self):
        '''
        Function that initializes the game sound.
        
        '''
        pg.mixer.init()
        chan1 = pg.mixer.Channel(1)
        sound1 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/Fireside-Tales-MP3.mp3'))
        chan1.queue(sound1)
        chan1.set_volume(0.1)  
    
    def update(self):
        '''
        Function that updates the game.
        
        '''
        # Main menu logic
        if not self.start:
            print("menu inicial")
            self.currentLevel = 0
            self.start, self.credits = main(self.start, self.screen, pg.time,  self.credits)
            if self.credits:
                print("creditos")
                self.start, self.credits = authors(self.screen)
                self.level.resetLevel = False
            self.startTime = pg.time.get_ticks()

        self.timeSinceEnter = pg.time.get_ticks() - self.startTime
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
        if self.level.levelData == self.levels[0] and self.timeSinceEnter < 8000:
            tutorial(self.screen)
        # Check if level will reset
        if self.level.resetLevel == True:
            # Pause music
            pg.mixer.music.pause()
            # Check if the player advanced the level
            if self.level.advanceLevel == True:
                self.currentLevel += 1
                # Check if the player reached the final level
                if self.currentLevel == self.maxLevel + 1:
                    # Show win screen
                    self.start = win(self.start, self.screen, pg.time)
                    self.currentLevel = -1
                # Just initialize the next level
                else: 
                    self.initVariables()
                    self.start = True
            # If not, the player died     
            else:
                # Show death screen
                if self.dead == True:
                    self.start, self.restart, self.dead = death(self.start, self.screen, pg.time, self.restart, self.dead)
                # Initialize the level again
                else:
                    self.initVariables()
                    self.start = True
            # Restart game logic
            if self.restart == True:
                self.initVariables()
                self.start = True
            # Initialize game music
            self.initMedia()
        # Screen and time update
        pg.display.update()
        self.clock.tick(60)

    def play(self):
        '''
        Main function.
        
        '''
        # Update the game
        self.update()