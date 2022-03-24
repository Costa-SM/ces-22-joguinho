from turtle import pos
import pygame as pg
from utils import *
from resources import *

class Fultano(pg.sprite.Sprite):
    '''
    Represents the main character, Fultano.
    '''
    def __init__(self, x_pos, y_pos, tiles_group):
        super().__init__()
        self.health = FULTANO_HEALTH
        self.dx = 0
        self.dy = 0
        self.stepLength = 5
        self.jumpHigh = 15
        self.running = False
        self.jumped = False
        self.attacking = False
        self.fultano_x_direction = 'right'
        self.times_jumped = 0
        self.max_jumps = 3
        self.initialPos = vec(x_pos, y_pos)
        self.oldPos = vec(x_pos, y_pos)
        self.pos = self.oldPos
        self.vel = vec(0, 0)
        self.tiles_group = tiles_group
        
        # Sprite Loading
        self.sprites, self.rect = load_sprite('fultano',2)
        self.currentState = 'idle'
        self.currentSprite = 0
        self.image = self.sprites[self.currentState][self.currentSprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.pos.x, self.pos.y]


    def update(self, speed):
        '''
        Updates Fultano
        '''
        if not self.running:
            self.currentState = 'idle'
        if self.attacking:
            self.currentState = 'attack_1'
        if self.jumped:
            self.currentState = 'jump'

        self.currentSprite = self.currentSprite + speed
        if self.currentSprite >= len(self.sprites[self.currentState]):
            self.currentSprite = 0

        self.image = self.sprites[self.currentState][int(self.currentSprite)]  

        if self.fultano_x_direction == 'left':
            self.image = pg.transform.flip(self.image, 1, 0) 
            
        self.updatePosition()
        
    def updatePosition(self):
        '''
        Moves Fultano
        '''
        self.oldPos = self.pos
        self.dx = 0
        self.dy = 0

        key_input = pg.key.get_pressed()
        if key_input[pg.K_UP] and self.jumped == False and self.times_jumped < self.max_jumps:
            self.currentState = 'jump'
            self.vel.y = -self.jumpHigh
            self.jumped = True
            self.times_jumped += 1
        if key_input[pg.K_UP] == False:
            self.jumped = False
        
        if key_input[pg.K_RIGHT]:
            self.currentState = 'run'
            self.running = True
            self.dx = self.stepLength
            self.fultano_x_direction = 'right'
        elif key_input[pg.K_LEFT]:
            self.currentState = 'run'
            self.running = True
            self.fultano_x_direction = 'left'
            self.dx = -self.stepLength
            if self.pos.x <= self.initialPos.x:
                self.pos.x = self.initialPos.x
        elif key_input[pg.K_c]:
            self.attacking = True
            self.currentState = 'attack_1'
        else:
            self.attacking = False
            self.running = False 

        # Horizontal movement

        self.pos.x += self.dx
        self.rect.left = self.pos.x
        
        # Check for collisions in x

        for sprite in self.tiles_group:
            if sprite.rect.colliderect(self.rect):
                if self.fultano_x_direction == 'left':
                    self.pos.x += self.stepLength
                    self.rect.left = sprite.rect.right
                elif self.fultano_x_direction == 'right':
                    self.pos.x -= self.stepLength
                    self.rect.right = sprite.rect.left

        # Vertical movement

        # Gravity

        self.vel.y += 1
        if self.vel.y > 10:
            self.vel.y = 10

        self.dy += self.vel.y
        
        # Checks if it hits the ground

        if self.pos.y + self.dy <= self.initialPos[1]:
            self.pos.y += self.dy
        else:
            self.times_jumped = 0
            self.pos.y = self.initialPos[1]
            self.vel.y = 0
        
        self.rect.bottom = self.pos.y

        for sprite in self.tiles_group:
            if sprite.rect.colliderect(self.rect):
                if self.vel.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.pos.y = self.rect.bottom
                    self.vel.y = 0
                elif self.vel.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.times_jumped = 0
                    self.pos.y = self.rect.bottom
                    self.vel.y = 0
        