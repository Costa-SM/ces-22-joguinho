import pygame as pg
from game_entities.fultano import Fultano
from game_entities.monster import Monster
from game_scenery.camera import CameraGroup
from utils import WIDTH, HEIGHT, BLACK
from menus import main, pause

pg.init()

class Game():
    def __init__(self) -> None:
        self.initVariables()
        self.initWindow()

    def initVariables(self):

        # Game screen
        self.screen = pg.display
        self.window = self.screen.set_mode((WIDTH,HEIGHT))
        self.time = pg.time

        # Boolean game variables
        self.running = True
        self.start = False
        self.paused = False
        
        # Game instances
        self.fultano = Fultano(200, 600)
        self.monster = Monster(500, 600 - 85)

        # Creating sprite groups
        self.fultano = Fultano(200, 600)
        self.monster = Monster(500, 600 - 86)
        self.sprites = pg.sprite.Group()
        self.camera = CameraGroup()
        self.camera.add(self.fultano)
        self.sprites.add(self.monster)

    def initWindow(self):
        self.screen.set_caption("Game")

    def update(self):
        # Quit Button
        if not self.start:
            self.start = main(self.start, self.screen, self.window, self.time)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = True
                    self.paused = pause(self.paused, self.screen, self.window, self.time)

        self.sprites.update(0.1)
        self.camera.update(0.1) 
        self.time.Clock().tick(60)

    def render(self):
        self.window.fill(pg.Color('white'))
        self.camera.custom_draw(self.fultano)
        self.sprites.draw(self.window)   
        self.screen.update()
        

    