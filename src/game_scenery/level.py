import os
import pygame as pg
from game_scenery.tiles import Decoration, Tile, StaticTile, Crate, Potion
from game_entities.enemy import Enemy
from game_entities.fultano import Fultano
from resources import importCsvLayout, importCutGraphics
from utils import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, BASE_PATH

class Level:
    '''
    Class that represents the game level.
    
    '''
    def __init__(self, levelData, surface):
        '''
        Level class' constructor.
        :param levelData: data to create the level layout and tiles
        :type levelData: .tmx file
        :param surface: surface to display the draw the level
        :type surface: pygame Surface
        
        '''
        # Level initialization
        self.levelData = levelData
        self.displaySurface = surface
        # Level logic
        self.resetLevel = False
        self.advanceLevel = False        
        # Layout moving speed
        self.worldShift = 0
        # Song initialization
        self.backgroundSong = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/Fireside-Tales-MP3.mp3'))
        self.songStartTime = 0
        self.powerUpIsPlaying = False
        # Loading player
        self.playerLayout = importCsvLayout(self.levelData['player'])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.playerSetup(self.playerLayout)
        self.playerOnGround = False
        self.currentX = None
        self.voidFall = False        
        # Loading terrain
        self.terrainLayout = importCsvLayout(self.levelData['terrain'])
        self.terrainSprites = self.createTileGroup(self.terrainLayout, 'terrain')
        # Loading decoration
        self.decorationLayout = importCsvLayout(self.levelData['bg_decoration'])
        self.decorationSprites = self.createTileGroup(self.decorationLayout, 'bg_decoration')
        # Loading crates
        self.crateLayout = importCsvLayout(self.levelData['crates'])
        self.crateSprites = self.createTileGroup(self.crateLayout, 'crates')
        # Loading skeletons
        self.skeletonLayout = importCsvLayout(self.levelData['skeleton'])
        self.skeletonSprites = self.createTileGroup(self.skeletonLayout, 'skeleton')
        self.enemyCollidableSprites = self.skeletonSprites.sprites()
        # Loading constraints
        self.constraintLayout = importCsvLayout(self.levelData['constraints'])
        self.constraintSprites = self.createTileGroup(self.constraintLayout, 'constraints')
        # Loading potions
        self.potionLayout = importCsvLayout(self.levelData['potion'])
        self.potionSprites = self.createTileGroup(self.potionLayout, 'potion')

    def createTileGroup(self, layout, type):
        '''
        Function that creates a group of tile sprites.
        :param layout: the layout tiles
        :type layout: list
        :param type: the layout tiles type
        :type type: int
        :rtype: pygame sprite group.
        
        '''
        spriteGroup =  pg.sprite.Group()
        # Read the layout and add to the sprite group
        for rowIndex, row in enumerate(layout):
            for colIndex, val in enumerate(row):
                if val != '-1':
                    x = colIndex * TILE_SIZE
                    y = rowIndex * TILE_SIZE
                    # If it is terrain add to the sprite group
                    if type == 'terrain':
                        terrainTileList = importCutGraphics(os.path.join(BASE_PATH, 'assets/world/terrain/terrain_tiles.png'))
                        tileSurface = terrainTileList[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tileSurface)
                    # else create tile
                    if type == 'bg_decoration':
                        sprite = Decoration(TILE_SIZE, x, y, val)
                    if type == 'crates':
                        sprite = Crate(TILE_SIZE, x, y)
                    if type == 'skeleton':
                        sprite = Enemy(TILE_SIZE, x, y)
                    if type == 'constraints':
                        sprite = Tile(TILE_SIZE, x, y)
                    if type == 'potion':
                        sprite = Potion(TILE_SIZE, x, y)
                    spriteGroup.add(sprite)        
        return spriteGroup

    def playerSetup(self, layout):
        '''
        Function that loads Fultano and goal sprites.
        :param layout: the layout tiles
        :type layout: list
        
        '''
        for rowIndex, row in enumerate(layout):
            for colIndex, val in enumerate(row):
                x = colIndex * TILE_SIZE
                y = rowIndex * TILE_SIZE
                if val == '0':
                    sprite = Fultano((x, y))
                    self.player.add(sprite)
                if val == '1':
                    beginSurface = pg.image.load(os.path.join(BASE_PATH, 'assets/fultano/hat.png')).convert_alpha()
                    sprite = StaticTile(TILE_SIZE, x, y, beginSurface)
                    self.goal.add(sprite)                    

    def enemyCollisionReverse(self):
        '''
        Function that flips skeletons in case they collide
        
        '''
        for skeleton in self.skeletonSprites.sprites():
            if pg.sprite.spritecollide(skeleton, self.constraintSprites, False):
                skeleton.reverse()

    def horizontalMovementCollision(self):
        '''
        Function that detects player horizontal collisons.
        
        '''
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidableSprites = self.terrainSprites.sprites() + self.crateSprites.sprites()
        # Checking collisions for each collidable sprite
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    player.onLeft = True
                    self.currentX = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.onRight = True
                    self.currentX = player.rect.right
        # Updating game logic variables
        if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
            player.onLeft = False
        if player.onRight and (player.rect.right > self.currentX or player.direction.x <= 0):
            player.onRight = False

    def playerEnemyCollision(self):
        '''
        Function that detects enemys collisons.
        
        '''
        player = self.player.sprite
        # Checking collisions for each collidable sprite 
        for sprite in self.enemyCollidableSprites:
            if sprite.rect.colliderect(player.rect):
                if (player.rect.x - sprite.rect.x) > 0:
                    self.player.sprite.collisionSide = -1
                else:
                    self.player.sprite.collisionSide = 1
                # If Fultano is attacking an enemy
                if player.attacking == True:
                    chan2 = pg.mixer.Channel(2)
                    sound2 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/skeleton-dying.mp3'))
                    chan2.queue(sound2)
                    chan2.set_volume(0.1)
                    # Enemy die
                    sprite.die()
                    self.enemyCollidableSprites.remove(sprite)
                # Update Fultano health and sprite
                if(player.countHurted > 1.2 and player.waitHurt):
                        player.health -= 1
                        player.waitHurt = False
                elif player.blinking == False:
                    sprite.attack()                
                    player.blinking = True
                    player.waitHurt = True
                    self.wrongSide = ((self.player.sprite.rect.x - sprite.rect.x > 0 and sprite.previous_speed < 0) or
                                        (sprite.rect.x - self.player.sprite.rect.x > 0 and sprite.previous_speed > 0))                    
                    if(self.wrongSide):
                        sprite.reverse()

    def verticalMovementCollision(self):
        '''
        Function that detects vertical player collisons.
        
        '''
        player = self.player.sprite
        player.applyGravity()
        collidableSprites = self.terrainSprites.sprites() + self.crateSprites.sprites()
        # Checking collisions for each collidable sprite  
        for sprite in collidableSprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.onCeiling = True
        # Updating game logic variables
        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.onCeiling and player.direction.y > 0.1:
            player.onCeiling = False

    def scrollX(self):
        '''
        Function that adjusts player X coordinate due to world shift.
        
        '''
        player = self.player.sprite
        playerX = player.rect.centerx
        directionX = player.direction.x
        if playerX < SCREEN_WIDTH / 2 and directionX < 0:
            self.worldShift = 12 if self.powerUpIsPlaying else 8
            player.speed = 0
        elif playerX > SCREEN_WIDTH - (SCREEN_WIDTH / 2) and directionX > 0:
            self.worldShift = -12 if self.powerUpIsPlaying else -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 12 if self.powerUpIsPlaying else 8
    
    def getPlayerOnGround(self):
        '''
        Function that gets wheter the player is on ground.
        
        '''
        if self.playerOnGround:
            self.playerOnGround = True
        else:
            self.playerOnGround = False

    def playerPowerUp(self):
        '''
        Function that detects potion collision.
        
        '''
        player = self.player.sprite
        if self.powerUpIsPlaying == False:
            player.powerUp = False
        # Checking collisions for each collidable sprite 
        for sprite in self.potionSprites:
            if sprite.rect.colliderect(player.rect):
                player.powerUp = True
                player.health = 12
                pg.mixer.quit()
                pg.mixer.init()                
                chan1 = pg.mixer.Channel(1)
                sound1 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/Song-for-Denise.mp3'))
                chan1.queue(sound1)
                chan1.set_volume(0.3)
                self.songStartTime = pg.time.get_ticks()
                self.powerUpIsPlaying = True
                # Remove potion
                self.potionSprites.remove(sprite)
    
    def resetAllLevel(self):
        '''
        Function that resets the level.
        
        '''
        player = self.player.sprite
        # If the player falls
        if player.rect.bottom >= SCREEN_HEIGHT + 200:
            if (self.voidFall == False):
                pg.mixer.quit()
                pg.mixer.init()
                chan1 = pg.mixer.Channel(1)
                sound1 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/falling-dying.mp3'))
                chan1.queue(sound1)
                chan1.set_volume(0.1)
            self.voidFall = True
            if player.rect.bottom >= SCREEN_HEIGHT + 5000:
                self.resetLevel = True
        # Else if the player dies
        elif player.health == 0:
            self.resetLevel = True        
        # Else if goal is reached
        elif self.goal.sprite.rect.colliderect(self.player.sprite.rect):
            self.resetLevel = True
            self.advanceLevel = True
        
    def run(self):
        '''
        Function that runs the level.

        '''
        # Run terrain
        self.terrainSprites.update(self.worldShift)
        self.terrainSprites.draw(self.displaySurface)        
        # Run decoration
        self.decorationSprites.update(self.worldShift)
        self.decorationSprites.draw(self.displaySurface)
        # Run crates
        self.crateSprites.update(self.worldShift)
        self.crateSprites.draw(self.displaySurface)
        # Run potions
        self.potionSprites.update(self.worldShift)
        self.potionSprites.draw(self.displaySurface)
        # Run enemies
        self.skeletonSprites.update(self.worldShift)
        self.constraintSprites.update(self.worldShift)
        self.enemyCollisionReverse()
        
        # Fix draw position
        for skeleton in self.skeletonSprites:
            if skeleton.dying:
                skeleton.rect.y -= 14
                continue
            
            elif (skeleton.attacking == True):
                if skeleton.previous_speed < 0:
                    skeleton.rect.x -= 90
                    skeleton.rect.y -= 50
                else:
                    skeleton.rect.x -= 60
                    skeleton.rect.y -= 50
                if(self.wrongSide):
                    skeleton.image = pg.transform.flip(skeleton.image, True, False)
            else:
                skeleton.rect.x -= 25
                skeleton.rect.y -= 15
        self.skeletonSprites.draw(self.displaySurface)
        for skeleton in self.skeletonSprites:            
            if skeleton.dying:
                skeleton.rect.y += 14
                continue
            
            elif skeleton.attacking == True:
                if skeleton.previous_speed < 0:
                    skeleton.rect.x += 90
                    skeleton.rect.y += 50
                else:
                    skeleton.rect.x += 60
                    skeleton.rect.y += 50
            else:
                skeleton.rect.x += 25
                skeleton.rect.y += 15
        
        # Run player
        self.player.update()
        self.horizontalMovementCollision()
        self.playerEnemyCollision()
        self.getPlayerOnGround()
        self.verticalMovementCollision()
        self.scrollX()
        self.playerPowerUp()
        self.resetAllLevel()
        # Fix draw position
        shift = 50 if self.player.sprite.powerUp else 25
        self.player.sprite.rect.x -= shift
        self.player.draw(self.displaySurface)
        self.player.sprite.rect.x += shift
        # Check song time
        if (pg.time.get_ticks() > self.songStartTime + 17000 and self.powerUpIsPlaying == True) or self.advanceLevel == True:
            pg.mixer.quit()
            pg.mixer.init()
            if self.advanceLevel == False:
                if self.player.sprite.health > 8:
                    self.player.sprite.health = 8                
                chan1 = pg.mixer.Channel(1)
                chan1.queue(self.backgroundSong)
                chan1.set_volume(0.1)
                self.powerUpIsPlaying = False
                self.songStartTime = 0
                self.player.sprite.powerUp = False
        # Update sprites
        self.goal.update(self.worldShift)
        self.goal.draw(self.displaySurface)
        self.player.sprite.healthSprites.update(0)
        self.player.sprite.healthSprites.draw(self.displaySurface)
        self.player.sprite.healthSprites.empty()

        #Debug function
        #self.debug()
        
    def debug(self):
        '''
        Function that draws helpful debugging bounding rectangles.
        
        '''
        # Draw the player's rectangle
        pg.draw.rect(self.displaySurface, pg.Color('red'), self.player.sprite.rect, width=4)
        # Draw the goal's rectangle
        pg.draw.rect(self.displaySurface, pg.Color('red'), self.goal.sprite.rect, width=4)
        # Draw the skeleton's rectangles
        for skeleton in self.skeletonSprites:
            pg.draw.rect(self.displaySurface, pg.Color('red'), skeleton.rect, width=4)
