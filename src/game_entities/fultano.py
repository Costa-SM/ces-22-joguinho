import pygame as pg
from game_scenery.tiles import StaticTile
from resources import importFolder
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
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.1
        self.image = self.animations['idle'][self.frameIndex]
        self.image = pg.transform.scale(self.image, (100, 74))
        self.rect = self.image.get_rect(topleft = pos)
        # Health variables
        self.health = FULTANO_HEALTH
        self.healthSprites = pg.sprite.Group()
        # Player physics
        self.lastStatus = None
        self.collisionSide = None
        self.direction = pg.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jumpSpeed = -16
		# Player logic and state
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeiling = False
        self.onLeft = False
        self.onRight = False
        self.attacking = False
        self.attackType = 'attack_1'
        # Player hurt
        self.timeHurted = 10
        self.blinking = False
        self.countHurted = 0
        self.waitHurt = False
        # Player power-up
        self.powerUp = False

    def importCharacterAssets(self):
        '''
        Function that imports fultano assets.

        '''
        characterPath = ASSETS_DIR + '/fultano/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[], 'attack_1':[], 'attack_2':[], 'attack_3':[]}

        for animation in self.animations.keys():
            fullPath = characterPath + animation
            self.animations[animation] = importFolder(fullPath)

    def animate(self):
        '''
        Function that animates Fultano.

        '''
        # Update frame
        if self.lastStatus != self.status:
            self.frameIndex = 0        
        animation = self.animations[self.status]
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        # Update image
        image = animation[int(self.frameIndex)]
        if self.powerUp == True:
            image = pg.transform.scale(image, (140, 74))
        else:
            image = pg.transform.scale(image, (100, 74))
        # If the player is taking damage
        if self.blinking == True:
            self.countHurted += 0.1
            if int(self.countHurted) % 2 == 1 and self.countHurted > 1.3 and not self.waitHurt:
                image = pg.Surface((100, 74), pg.SRCALPHA, 16)
        if int(self.countHurted) >= self.timeHurted:
            self.countHurted = 0
            self.blinking = False
        # If the image needs to be fliped
        if self.facingRight:
            self.image = image
        else:
            flippedImage = pg.transform.flip(image,True,False)
            self.image = flippedImage
        self.rect = pg.Rect(self.rect.x, self.rect.y, 50, self.image.get_rect().height)
        self.lastStatus = self.status

    def getInput(self):
        '''
        Function that get player keyboard input.

        '''
        keys = pg.key.get_pressed()
        # If Fultano has been damaged, ignore input and get pushed back
        if (self.collisionSide != None):
            if self.countHurted > 1.3 and self.countHurted < 1.8 and self.blinking:
                self.direction.x = -self.collisionSide
                if not self.onGround:
                    self.jump()                
                return            
            self.collisionSide = None
        # Key input logic
        if keys[pg.K_RIGHT] and not self.attacking:
            self.direction.x = 1
            self.facingRight = True
        elif keys[pg.K_LEFT] and not self.attacking:
            self.direction.x = -1
            self.facingRight = False
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
            if self.frameIndex == 0:
                self.attacking = False 

    def getStatus(self):
        '''
        Function get player status based on his attributes.

        '''
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

    def getHealth(self):
        '''
        Function that get player health.

        '''        
        for heart in range(int(self.health)):
            heartSurface = pg.image.load(os.path.join(BASE_PATH, 'assets/interface/heart.png')).convert_alpha()
            sprite = StaticTile(TILE_SIZE, 25 + 30*heart, 20, heartSurface)
            self.healthSprites.add(sprite)

    def applyGravity(self):
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
            self.direction.y = self.jumpSpeed

    def update(self):
        '''
        Function that updates Fultano.

        '''
        self.getInput()
        self.getStatus()
        self.getHealth()
        self.animate()