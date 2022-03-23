import pygame as pg
from game_entities.fultano import Fultano
from utils import WIDTH, HEIGHT, BLACK

pg.init()

class Game():
    def __init__(self) -> None:
        self.initVariables()
        self.initWindow()

    def initVariables(self):
        self.screen = pg.display
        self.window = self.screen.set_mode((WIDTH,HEIGHT))
        self.icon = pg.image
        self.time = pg.time
        self.running = True
        self.fultano = Fultano()
        self.sprites = pg.sprite.Group()
        self.sprites.add(self.fultano)

    def initWindow(self):
        self.screen.set_caption("Game")

        # Set the window color to white
        self.window.fill(pg.Color('white'))

        # Create surface for drawing objects
        self.surface = pg.Surface((WIDTH, HEIGHT))

    def update(self):
        # Quit Button
        self.fultano.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
        
        self.time.Clock().tick(60)

    def render(self):
        self.window.fill(pg.Color('white'))
        self.sprites.draw(self.window)
        self.screen.update()
        

    