import pygame as pg
from game_entities.fultano import Fultano
from game_entities.monster import Monster
from game_scenery.camera import CameraGroup
from utils import WIDTH, HEIGHT

pg.init()

class Game():
    def __init__(self) -> None:
        self.initVariables()
        self.initWindow()

    def initVariables(self):
        self.screen = pg.display
        self.window = self.screen.set_mode((WIDTH,HEIGHT))
        self.time = pg.time
        self.running = True
        self.fultano = Fultano(200, 600)
        self.monster = Monster(500, 600 - 86)
        self.camera = CameraGroup()
        self.camera.add(self.fultano)
        self.camera.add(self.monster)

    def initWindow(self):
        self.screen.set_caption("Game")

    def update(self):
        # Quit Button
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        self.camera.update(0.1) 
        self.time.Clock().tick(60)

    def render(self):
        self.window.fill(pg.Color('white'))
        self.camera.custom_draw(self.fultano)  
        self.screen.update()
        

    