import os
import pygame as pg
from utils import *
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
        self.pos = vec(100, 600)
        self.speed = vec(0, 0)
        
        # Sprite Loading
        self.sprites, self.rect = load_sprite('fultano',2)
        self.currentState = 'idle'
        self.currentSprite = 0
        self.image = self.sprites[self.currentState][self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]

        self.running = False
        self.attacking = False

    def update(self):
        '''
        Updates Fultano
        '''
        if not self.running:
            self.currentState = 'idle'
        if self.attacking:
            self.currentState = 'attack_1'

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
            self.currentState = 'run'
            self.running = True
            self.pos.y = self.pos.y - self.jumpHigh
        elif (key_input[pg.K_RIGHT]):
            print("direita")
            self.currentState = 'run'
            self.running = True
            self.pos.x = self.pos.x + self.stepLength
        elif (key_input[pg.K_DOWN]):
            print("baixo")
            self.currentState = 'run'
            self.running = True
            self.pos.y = self.pos.y + self.jumpHigh
        elif (key_input[pg.K_LEFT]):
            print("esquerda")
            self.currentState = 'run'
            self.running = True
            self.image = pg.transform.flip(self.image, 1, 0)
            self.pos.x = self.pos.x - self.stepLength
        elif key_input[pg.K_c]:
            self.attacking = True
            self.currentState = 'attack_1'
        else:
            self.attacking = False
            self.running = False
            


        self.rect.midbottom = self.pos

  #  def draw(self, window):
  #      '''
  #      Draws Fultano
  #      '''
  #      window.blit(self.surf, self.rect)
        