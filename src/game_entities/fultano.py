import os
from turtle import pos
import pygame as pg
from utils import *
from resources import *

class Fultano(pg.sprite.Sprite):
    '''
    Represents the main character, Fultano.
    '''
    def __init__(self):
        super().__init__()
        self.health = FULTANO_HEALTH
        self.dx = 0
        self.dy = 0
        self.stepLength = 5
        self.jumpHigh = 15
        self.oldPos = vec(100,600)
        self.pos = vec(100, 600)
        self.vel = vec(0, 0)
        
        # Sprite Loading
        self.sprites, self.rect = load_sprite('fultano',2)
        self.currentState = 'idle'
        self.currentSprite = 0
        self.image = self.sprites[self.currentState][self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]

        self.running = False
        self.jumped = False
        self.attacking = False

    def update(self):
        '''
        Updates Fultano
        '''
        if not self.running:
            self.currentState = 'idle'
        if self.attacking:
            self.currentState = 'attack_1'
        if self.jumped:
            self.currentState = 'jump'

        self.currentSprite = self.currentSprite + 0.1
        if self.currentSprite >= len(self.sprites[self.currentState]):
            self.currentSprite = 0        
        self.image = self.sprites[self.currentState][int(self.currentSprite)]
        self.updatePosition()
        
    def updatePosition(self):
        '''
        Moves Fultano
        '''
        self.oldPos = self.pos
        self.dx = 0
        self.dy = 0
        key_input = pg.key.get_pressed()
        if key_input[pg.K_UP] and self.jumped == False:
            self.currentState = 'jump'
            self.vel.y = -self.jumpHigh
            self.jumped = True
        if key_input[pg.K_UP] == False:
            self.jumped = False
        
        if key_input[pg.K_RIGHT]:
            self.currentState = 'run'
            self.running = True
            self.pos.x = self.pos.x + self.stepLength
        elif key_input[pg.K_LEFT]:
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

        self.vel.y += 1
        if self.vel.y > 10:
            self.vel.y = 10

        self.dy += self.vel.y

        self.pos.x += self.dx
        if self.pos.y + self.dy <= HEIGHT:
            self.pos.y += self.dy   
        if self.rect.bottom > HEIGHT:
            self.pos.y = HEIGHT
        self.rect.midbottom = self.pos

  #  def draw(self, window):
  #      '''
  #      Draws Fultano
  #      '''
  #      window.blit(self.surf, self.rect)
        