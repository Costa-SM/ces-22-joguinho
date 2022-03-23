import os
import pygame as pg
from utils import vec
from resources import *

class Fultano(pg.sprite.Sprite):
    '''
    Represents the main character, Fultano.
    '''
    def __init__(self):
        super().__init__()
        self.health = 100
        self.stepLength = 5
        self.jumpHigh = 10
        self.pos = vec(100, 600-148)
        self.speed = vec(0, 0)

        # Sprite Loading
        self.sprites, self.rect = load_sprite('fultano')
        self.states = ['idle', 'jump', 'run', 'attack']
        self.currentState = 0
        self.currentSprite = 0
        self.image = self.sprites[self.currentState][self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]

        


    def update(self):
        '''
        Updates Fultano
        '''
        self.currentState = 0
        self.currentSprite = self.currentSprite + 0.1
        if self.currentSprite >= len(self.sprites[self.currentState]):
            self.currentSprite = 0        
        self.image = self.sprites[self.currentState][int(self.currentSprite)]
        self.updatePosition()


    def updatePosition(self):
        '''
        Moves Fultano
        '''
        key_input = pg.key.get_pressed()
        if (key_input[pg.K_UP]):
            print("cima")
            self.pos.y = self.pos.y - self.jumpHigh
        elif (key_input[pg.K_RIGHT]):
            print("direita")
            self.pos.x = self.pos.x + self.stepLength
        elif (key_input[pg.K_DOWN]):
            print("baixo")
            self.pos.y = self.pos.y + self.jumpHigh
        elif (key_input[pg.K_LEFT]):
            print("esquerda")
            self.pos.x = self.pos.x - self.stepLength

        self.rect.midbottom = self.pos

  #  def draw(self, window):
  #      '''
  #      Draws Fultano
  #      '''
  #      window.blit(self.surf, self.rect)
        