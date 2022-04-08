import os
import pygame as pg
from game_scenery.tiles import Decoration, Tile, StaticTile, Crate
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
        :param levelData: data to create the level layout and tiles.
        :type levelData: .tmx file.
        :param surface: surface to display the draw the level.
        :type surface: pygame Surface.
        
        '''
        self.displaySurface = surface

        self.resetLevel = False
        
        # Layout moving speed
        self.worldShift = 0

        # Player
        self.playerLayout = importCsvLayout(levelData['player'])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.playerSetup(self.playerLayout)
        self.playerOnGround = False
        self.current_x = None
        
        # Terrain variables
        self.terrainLayout = importCsvLayout(levelData['terrain'])
        self.terrainSprites = self.createTileGroup(self.terrainLayout, 'terrain')

        # Decoration variables
        self.decorationLayout = importCsvLayout(levelData['bg_decoration'])
        self.decorationSprites = self.createTileGroup(self.decorationLayout, 'bg_decoration')

        # Crates
        self.crateLayout = importCsvLayout(levelData['crates'])
        self.crateSprites = self.createTileGroup(self.crateLayout, 'crates')

        # Skeletons
        self.skeletonLayout = importCsvLayout(levelData['skeleton'])
        self.skeletonSprites = self.createTileGroup(self.skeletonLayout, 'skeleton')
        self.enemy_collidable_sprites = self.skeletonSprites.sprites()

        # Constraint
        self.constraintLayout = importCsvLayout(levelData['constraints'])
        self.constraintSprites = self.createTileGroup(self.constraintLayout, 'constraints')

    def createTileGroup(self, layout, type):
        '''
        Function that creates a group of tile sprites.
        :param layout: the tile's layout.sprites = self.skeletonSprites.sprites()
        :rtype: pygame sprite group.
        
        '''
        spriteGroup =  pg.sprite.Group()

        # Read the layout and add to the sprite group
        for rowIndex, row in enumerate(layout):
            for colIndex, val in enumerate(row):
                if val != '-1':
                    x = colIndex * TILE_SIZE
                    y = rowIndex * TILE_SIZE

                    # Add terrain tiles to the sprite group
                    if type == 'terrain':
                        terrainTileList = importCutGraphics(os.path.join(BASE_PATH, 'assets/world/terrain/terrain_tiles.png'))
                        tileSurface = terrainTileList[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tileSurface)
                        

                    if type == 'bg_decoration':
                        sprite = Decoration(TILE_SIZE, x, y, val)

                    # Crates
                    if type == 'crates':
                        sprite = Crate(TILE_SIZE, x, y)

                    if type == 'skeleton':
                        sprite = Enemy(TILE_SIZE, x, y)

                    if type == 'constraints':
                        sprite = Tile(TILE_SIZE, x, y)

                    spriteGroup.add(sprite)                       
        
        return spriteGroup

    def playerSetup(self, layout):
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
                    

    def enemy_collision_reverse(self):
        for skeleton in self.skeletonSprites.sprites():
            if pg.sprite.spritecollide(skeleton, self.constraintSprites, False):
                skeleton.reverse()

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrainSprites.sprites() + self.crateSprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0: 
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def player_enemy_collision(self):
        player = self.player.sprite

        for sprite in self.enemy_collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if (player.rect.x - sprite.rect.x) > 0:
                    self.player.sprite.collision_side = -1
                else:
                    self.player.sprite.collision_side = 1

                if player.attacking == True:
                    sprite.die()
                    self.enemy_collidable_sprites.remove(sprite)
                    
                elif player.blinking == False:
                    player.health -= 1
                    print('Damage taken')
                    player.blinking = True

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrainSprites.sprites() + self.crateSprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.onGround = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.onGround and player.direction.y < 0 or player.direction.y > 1:
            player.onGround = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < SCREEN_WIDTH / 2 and direction_x < 0:
            self.worldShift = 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 2) and direction_x > 0:
            self.worldShift = -8
            player.speed = 0
        else:
            self.worldShift = 0
            player.speed = 8
    
    def get_player_onGround(self):
        if self.playerOnGround:
            self.playerOnGround = True
        else:
            self.playerOnGround = False
    
    def resetAllLevel(self):
        player = self.player.sprite
        if player.rect.bottom >= SCREEN_HEIGHT + 200:
            self.resetLevel = True
        elif player.health == 0:
            self.resetLevel = True
        
        # When the goal is reached, go back to the menu
        elif self.goal.sprite.rect.colliderect(self.player.sprite.rect):
            self.resetLevel = True
        
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

        # Run enemies
        self.skeletonSprites.update(self.worldShift)
        self.constraintSprites.update(self.worldShift)
        self.enemy_collision_reverse()

        # Hack to fix draw position
        for skeleton in self.skeletonSprites:
            skeleton.rect.x -= 25
            skeleton.rect.y -= 15

        self.skeletonSprites.draw(self.displaySurface)

        for skeleton in self.skeletonSprites:
            skeleton.rect.x += 25
            skeleton.rect.y += 15

        # Run player
        self.player.update()
        self.horizontal_movement_collision()
        self.player_enemy_collision()
        self.get_player_onGround()
        self.vertical_movement_collision()
        self.scroll_x()
        self.resetAllLevel()

        self.player.sprite.rect.x -= 25
        self.player.draw(self.displaySurface)
        self.player.sprite.rect.x += 25
        
        self.goal.update(self.worldShift)
        self.goal.draw(self.displaySurface)
        self.player.sprite.healthSprites.update(0)
        self.player.sprite.healthSprites.draw(self.displaySurface)
        self.player.sprite.healthSprites.empty()

        #Debug function
        #self.debug()
        
    def debug(self):
        # Helpful debug drawings

        # Draw the player's rectangle
        pg.draw.rect(self.displaySurface, pg.Color('red'), self.player.sprite.rect, width=4)

        # Draw the goal's rectangle
        pg.draw.rect(self.displaySurface, pg.Color('red'), self.goal.sprite.rect, width=4)

        # Draw the skeleton's rectangles
        for skeleton in self.skeletonSprites:
            pg.draw.rect(self.displaySurface, pg.Color('red'), skeleton.rect, width=4)
