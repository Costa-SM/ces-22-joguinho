import pygame as pg
from game_scenery.level import Level
from game_scenery.camera import CameraGroup
from utils import WIDTH, HEIGHT
from levels_data import *
from menus import main, pause

pg.init()

class Game():
    def __init__(self) -> None:
        self.initVariables()
        self.initWindow()
        self.initMedia()

    def initVariables(self):

        # Game screen
        self.screen = pg.display
        self.window = self.screen.set_mode((WIDTH,HEIGHT))
        self.time = pg.time
        self.start = False
        self.paused = False

        # Boolean game variables
        self.running = True

        # Sprite group commanded by camera
        self.camera = CameraGroup()

    def initMedia(self):
        pg.mixer.init()
        pg.mixer.music.load('media/Fireside-Tales-MP3.mp3')
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)

    def initWindow(self):
        self.screen.set_caption("Game")
        self.level = Level(level_map, self.window, self.camera)

    def update(self):
        # Quit Button
        if not self.start:
            self.start = main(self.start, self.screen, self.window, self.time)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.mixer.music.pause()
                    self.paused = True
                    self.paused = pause(self.paused, self.screen, self.window, self.time)

        self.camera.update(0.1) 
        self.time.Clock().tick(60)

    def render(self):
        self.window.fill(pg.Color('white'))
        self.level.run()
        self.screen.update()
        