import pygame as pg
from game_scenery.tiles import StaticTile
from resources import import_folder
from utils import *

class Fultano(pg.sprite.Sprite):
    '''
    Class that represents Fultano.
    
    '''
    def __init__(self, pos):
        '''
        Fultano class' constructor.
        :param pos: Fultano position
        :type pos: tuple
        
        '''
        super().__init__()
        # Sprite initialization
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations['idle'][self.frame_index]
        self.image = pg.transform.scale(self.image, (100, 74))
        self.rect = self.image.get_rect(topleft = pos)
        # Health variables
        self.health = FULTANO_HEALTH
        self.health_sprites = pg.sprite.Group()
        # Player physics
        self.last_status = None
        self.collision_side = None
        self.direction = pg.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
		# Player logic and state
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.attacking = False
        self.attack_type = 'attack_1'
        # Player hurt
        self.time_hurted = 10
        self.blinking = False
        self.count_hurted = 0
        self.wait_hurt = False
        # Player power-up
        self.power_up = False

    def import_character_assets(self):
        '''
        Function that imports fultano assets.

        '''
        character_path = ASSETS_DIR + '/fultano/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'attack_1':[], 'attack_2':[], 'attack_3':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        '''
        Function that animates Fultano.

        '''
        # Update frame
        if self.last_status != self.status:
            self.frame_index = 0        
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        # Update image
        image = animation[int(self.frame_index)]
        if self.power_up == True:
            image = pg.transform.scale(image, (140, 74))
        else:
            image = pg.transform.scale(image, (100, 74))
        
        # If the player is taking damage
        if self.blinking == True:
            self.count_hurted += 0.1
            if int(self.count_hurted) % 2 == 1 and self.count_hurted > 1.3 and not self.wait_hurt:
                image = pg.Surface((100, 74), pg.SRCALPHA, 16)
        
        if int(self.count_hurted) >= self.time_hurted:
            self.count_hurted = 0
            self.blinking = False
        
        # If the image needs to be flipped
        if self.facing_right:
            self.image = image
        else:
            self.image = pg.transform.flip(image,True,False)
        self.rect = pg.Rect(self.rect.x, self.rect.y, 50, self.image.get_rect().height)
        self.last_status = self.status

    def get_input(self):
        '''
        Function that get player keyboard input.

        '''
        keys = pg.key.get_pressed()
        # If Fultano has been damaged, ignore input and get pushed back
        if (self.collision_side != None):
            if self.count_hurted > 1.3 and self.count_hurted < 1.8 and self.blinking:
                self.direction.x = -self.collision_side
                if not self.on_ground:
                    self.jump()
                return
            self.collision_side = None
        
        # Key input logic
        if keys[pg.K_RIGHT] and not self.attacking:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pg.K_LEFT] and not self.attacking:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pg.K_UP] and self.on_ground and not self.attacking:
            self.jump()
        if (keys[pg.K_c] or keys[pg.K_f] or keys[pg.K_v]) and self.on_ground and self.direction.x == 0:
            self.attacking = True
            if keys[pg.K_c]:
                self.attack_type = 'attack_1'
            elif keys[pg.K_f]:
                self.attack_type = 'attack_2'
            elif keys[pg.K_v]:
                self.attack_type = 'attack_3'
        else:
            if self.frame_index == 0:
                self.attacking = False 

    def get_status(self):
        '''
        Function get player status based on his attributes.

        '''
        if self.attacking:
            self.status = self.attack_type
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
        '''
        Function that get player health.

        '''
        for heart in range(int(self.health)):
            heartSurface = pg.image.load(os.path.join(BASE_PATH, 'assets/interface/heart.png')).convert_alpha()
            sprite = StaticTile(TILE_SIZE, 25 + 30*heart, 20, heartSurface)
            self.health_sprites.add(sprite)

    def apply_gravity(self):
        '''
        Function that apllies gravity in the player

        '''
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        '''
        Jump function.

        '''
        if self.status != 'jump':
            self.direction.y = self.jump_speed

    def update(self):
        '''
        Function that updates Fultano.

        '''
        self.get_input()
        self.get_status()
        self.get_health()
        self.animate()