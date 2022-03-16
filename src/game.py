from turtle import width
import pygame
from utils import WIDTH, HEIGHT, BLACK

import rohan

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

        # Set the window color to white
        self.window.fill(pygame.Color('white'))

        # Create surface for drawing objects
        self.surface = pygame.Surface((WIDTH, HEIGHT))

    def update(self):
        # Quit Button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        self.time.Clock().tick(60)

    def render(self):
        self.screen.flip()
        

    