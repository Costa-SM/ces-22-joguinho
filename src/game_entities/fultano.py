import pygame as pg
from game_scenery.tiles import StaticTile
from resources import importFolder
from utils import *

class Fultano(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(topleft = pos)
        self.health = FULTANO_HEALTH
        self.healthSprites = pg.sprite.Group()
        self.last_status = None
        self.collision_side = None

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
        self.attackType = 'attack_1'

        # Player hurt
        self.timeHurted = 10
        self.blinking = False
        self.countHurted = 0

    def import_character_assets(self):
        character_path = ASSETS_DIR + '/fultano/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'attack_1':[], 'attack_2':[], 'attack_3':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = importFolder(full_path)

    def animate(self):
        if self.last_status != self.status:
            self.frame_index = 0
        
        animation = self.animations[self.status]

        # loop over frame index 
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        image = pg.transform.scale(image, (100, 74))

        if self.blinking == True:
            self.countHurted += 0.1
            if int(self.countHurted) % 2 == 0:
                image = pg.Surface((100, 74), pg.SRCALPHA, 16)

        if int(self.countHurted) >= self.timeHurted:
            self.countHurted = 0
            self.blinking = False

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

        #print(self.rect.x, self.rect.y)
        self.last_status = self.status

    def get_input(self):
        keys = pg.key.get_pressed()

        # If Fultano has been damaged, ignore input and get pushed back
        if self.collision_side != None:
            if self.countHurted < 0.5 and self.blinking:
                self.direction.x = -self.collision_side

                if not self.onGround:
                    self.jump()
                
                return
            
            self.collision_side = None

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

        if (keys[pg.K_c] or keys[pg.K_f] or keys[pg.K_v]) and self.onGround and self.direction.x == 0:
            self.attacking = True
            if keys[pg.K_c]:
                self.attackType = 'attack_1'
            elif keys[pg.K_f]:
                self.attackType = 'attack_2'
            elif keys[pg.K_v]:
                self.attackType = 'attack_3'
        else:
            if self.frame_index == 0:
                self.attacking = False 

    def get_status(self):
        if self.attacking:
            self.status = self.attackType
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
        
        for heart in range(int(self.health)):
            heartSurface = pg.image.load(os.path.join(BASE_PATH, 'assets/interface/heart.png')).convert_alpha()
            sprite = StaticTile(TILE_SIZE, 25 + 30*heart, 20, heartSurface)
            self.healthSprites.add(sprite)

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.status != 'jump':
            self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        self.get_health()
        self.animate()