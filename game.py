import pygame
from utils import WIDTH, HEIGHT, BLACK

pygame.init()

class Game():
    def __init__(self) -> None:
        self.initVariables()
        self.initWindow()

    def initVariables(self):
        self.screen = pygame.display
        self.window = self.screen.set_mode((WIDTH,HEIGHT))
        self.icon = pygame.image
        self.time = pygame.time
        self.running = True

    def initWindow(self):
        self.screen.set_caption("Game")
      #  self.icon.load('icon.png')
      #  self.screen.set_icon(self.icon)
        self.window.fill(BLACK)

    def update(self):
        # Quit Button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        self.time.Clock().tick(60)

    def render(self):
        self.screen.flip()


    