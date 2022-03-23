import pygame as pg
from game_entities.fultano import Fultano
from game_entities.monster import Monster
from utils import WIDTH, HEIGHT, BLACK

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
        self.fultano = Fultano()
        self.monster = Monster(500, 600 - 85)
        self.sprites = pg.sprite.Group()
        self.sprites.add(self.fultano)
        self.sprites.add(self.monster)

    def initWindow(self):
        self.screen.set_caption("Game")

    def update(self):
        # Quit Button
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False

        self.sprites.update(0.1)        
        self.time.Clock().tick(60)

    def render(self):
        self.window.fill(pg.Color('white'))
        self.sprites.draw(self.window)
        self.screen.update()
        

    