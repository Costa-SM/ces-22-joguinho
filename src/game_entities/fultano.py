import pygame as pg
from game_scenery.tiles import StaticTile
from resources import importFolder
from utils import *

class Fultano(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.075
        self.image = self.animations['idle'][self.frame_index]
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft = pos)
        self.health = FULTANO_HEALTH
        self.healthSprites = pg.sprite.Group()

		# player movement
        self.direction = pg.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

		# player status
        self.status = 'idle'
        self.facing_right = True
        self.onGround = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.attacking = False
    def import_character_assets(self):
        character_path = 'assets/fultano/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'attack_1':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = importFolder(full_path)

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        image = pg.transform.scale(image, (100, 74))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pg.transform.flip(image,True,False)
            self.image = flipped_image

        # set the rect
        #if self.onGround and self.on_right:
        #    self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        #elif self.onGround and self.on_left:
        #    self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        #elif self.onGround:
        #    self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        #elif self.on_ceiling and self.on_right:
        #    self.rect = self.image.get_rect(topright = self.rect.topright)
        #elif self.on_ceiling and self.on_left:
        #    self.rect = self.image.get_rect(topleft = self.rect.topleft)
        #elif self.on_ceiling:
        #    self.rect = self.image.get_rect(midtop = self.rect.midtop)

        self.rect = pg.Rect(self.rect.x, self.rect.y, 50, self.image.get_rect().height)

        print(self.rect.x, self.rect.y)

    def get_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_RIGHT] and not self.attacking:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT] and not self.attacking:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pg.K_UP] and self.onGround:
            self.jump()

        if keys[pg.K_c] and self.onGround and self.direction.x == 0:
            self.attacking = True
        else:
            self.attacking = False

    def get_status(self):
        if self.attacking:
            self.status = 'attack_1'
        else:
            if self.direction.y < 0:
                self.status = 'jump'
            elif self.direction.y > 1:
                self.status = 'fall'
            else:
                if self.direction.x != 0:
                    self.status = 'run'
                else:
                    self.status = 'idle'

    def get_health(self):
        
        for heart in range(self.health):
            heartSurface = pg.image.load('assets/interface/heart.png').convert_alpha()
            sprite = StaticTile(TILE_SIZE, 25 + 30*heart, 20, heartSurface)
            self.healthSprites.add(sprite)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.get_health()
        self.animate()