import os
import pygame as pg
from game_scenery.tiles import AnimatedTile
from random import randint
from utils import BASE_PATH

class Enemy(AnimatedTile):
    def __init__(self, size, x, y):
        super().__init__(size, x, y, os.path.join(BASE_PATH, 'assets/skeleton/walk'))
        # TODO: refactor this and implement image resize
        self.rect.y += size - self.image.get_size()[1] + self.image.get_size()[1] / 8
        self.speed = randint(1, 2)

        self.rect.height = self.image.get_rect().height - 20
        self.rect.y += 15

        self.died = False
        self.dying = False
    
    def move(self):
        self.rect.x += self.speed
        
    def reverse_image(self):
        if self.speed < 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        self.speed *= -1
    
    def die(self):
        flip = True if self.speed < 0 else False
        self.speed = 0
        self.changeState(os.path.join(BASE_PATH, 'assets/skeleton/dead_near'), flip)
        self.dying = True
    
    def update(self, shift):
        self.rect.x += shift

        if self.dying == True and int(self.frameIndex) == len(self.frames) - 1:
            self.died = True
        if self.died == False:
            self.animate()
            self.move()
            self.reverse_image()