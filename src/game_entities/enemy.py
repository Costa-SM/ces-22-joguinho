import os
import pygame as pg
from game_scenery.tiles import AnimatedTile
from random import randint
from utils import BASE_PATH

class Enemy(AnimatedTile):
    '''
    Class that represents an enemy.
    
    '''
    def __init__(self, size, x, y):
        '''
        Enemy class' constructor.
        :param size: enemy size
        :type size: int
        :param x: enemy x coordinate
        :type x: int
        :param y: enemy y coordinate
        :type y: int
        
        '''
        super().__init__(size, x, y, os.path.join(BASE_PATH, 'assets/skeleton/walk'))
        # Set enemy position and speed
        self.rect.y += size - self.image.get_size()[1] + self.image.get_size()[1] / 8
        self.speed = randint(1, 2)
        self.rect.height = self.image.get_rect().height - 20
        self.rect.y += 15
        self.previous_speed = self.speed
        # Enemy logic
        self.died = False
        self.dying = False
        self.attacking = False
        self.original_y = self.rect.y
    
    def move(self):
        '''
        Function that moves the enemy.

        '''
        self.rect.x += self.speed
        
    def reverse_image(self):
        '''
        Function that reverses the enemy image

        '''
        if self.speed < 0:
            self.image = pg.transform.flip(self.image, True, False)
    
    def reverse(self):
        '''
        Function that reverses the enemy velocity

        '''
        self.speed *= -1
        self.previous_speed *= -1

    def attack(self):
        '''
        Function for enemy to attack

        '''
        # Check if the skeleton is dead before doing anything else
        if self.died or self.dying:
            return

        # Change sprite and speed
        flip = True if self.speed < 0 else False
        self.change_state(os.path.join(BASE_PATH, 'assets/skeleton/attack2'), flip, (200, 130))
        self.previous_speed = self.speed
        self.speed = 0
        # Change state
        self.attacking = True
    
    def die(self):
        '''
        Function for enemy to die

        '''
        # Change sprite and speed
        flip = True if self.speed < 0 else False
        self.speed = 0
        self.change_state(os.path.join(BASE_PATH, 'assets/skeleton/dead_near'), flip, (100, 96))
        
        # Change state
        self.dying = True
    
    def update(self, shift):
        '''
        Function that updates the enemy

        '''
        self.rect.x += shift
        # State handler
        if (self.dying == True) and (int(self.frame_index) == len(self.frames) - 1):
            self.died = True
        if (not self.dying) and (self.attacking == True) and (int(self.frame_index) == len(self.frames) - 1):
            self.attacking = False
            self.speed = self.previous_speed
            flip = False
            self.change_state(os.path.join(BASE_PATH, 'assets/skeleton/walk'), flip, (100, 96))
        if (not self.died):
            self.animate()
            self.move()
            self.reverse_image()