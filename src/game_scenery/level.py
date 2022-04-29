import os
import pygame as pg
from game_scenery.tiles import Decoration, Tile, StaticTile, Crate, Potion
from game_entities.enemy import Enemy
from game_entities.fultano import Fultano
from resources import import_csv_layout, import_cut_graphics
from utils import SCREEN_HEIGHT, SCREEN_WIDTH, TILE_SIZE, BASE_PATH

class Level:
    '''
    Class that represents the game level.
    
    '''
    def __init__(self, level_data, surface):
        '''
        Level class' constructor.
        :param level_data: data to create the level layout and tiles
        :type level_data: .tmx file
        :param surface: surface to display the draw the level
        :type surface: pygame Surface
        
        '''
        # Level initialization
        self.level_data = level_data
        self.display_surface = surface
        # Level logic
        self.reset_level = False
        self.advance_level = False        
        # Layout moving speed
        self.world_shift = 0
        # Song initialization
        self.background_song = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/Fireside-Tales-MP3.mp3'))
        self.song_start_time = 0
        self.power_up_is_playing = False
        # Loading player
        self.player_layout = import_csv_layout(self.level_data['player'])
        self.player = pg.sprite.GroupSingle()
        self.goal = pg.sprite.GroupSingle()
        self.player_setup(self.player_layout)
        self.player_on_ground = False
        self.current_x = None
        self.void_fall = False        
        # Loading terrain
        self.terrain_layout = import_csv_layout(self.level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')
        # Loading decoration
        self.decoration_layout = import_csv_layout(self.level_data['bg_decoration'])
        self.decoration_sprites = self.create_tile_group(self.decoration_layout, 'bg_decoration')
        # Loading crates
        self.crate_layout = import_csv_layout(self.level_data['crates'])
        self.crate_sprites = self.create_tile_group(self.crate_layout, 'crates')
        # Loading skeletons
        self.skeleton_layout = import_csv_layout(self.level_data['skeleton'])
        self.skeleton_sprites = self.create_tile_group(self.skeleton_layout, 'skeleton')
        self.enemy_collidable_sprites = self.skeleton_sprites.sprites()
        # Loading constraints
        self.constraint_layout = import_csv_layout(self.level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(self.constraint_layout, 'constraints')
        # Loading potions
        self.potion_layout = import_csv_layout(self.level_data['potion'])
        self.potion_sprites = self.create_tile_group(self.potion_layout, 'potion')

    def create_tile_group(self, layout, type):
        '''
        Function that creates a group of tile sprites.
        :param layout: the layout tiles
        :type layout: list
        :param type: the layout tiles type
        :type type: int
        :rtype: pygame sprite group.
        
        '''
        sprite_group =  pg.sprite.Group()
        # Read the layout and add to the sprite group
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != '-1':
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE
                    # If it is terrain add to the sprite group
                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics(os.path.join(BASE_PATH, 'assets/world/terrain/terrain_tiles.png'))
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(TILE_SIZE, x, y, tile_surface)
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
                    sprite_group.add(sprite)        
        return sprite_group

    def player_setup(self, layout):
        '''
        Function that loads Fultano and goal sprites.
        :param layout: the layout tiles
        :type layout: list
        
        '''
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
                if val == '0':
                    sprite = Fultano((x, y))
                    self.player.add(sprite)
                if val == '1':
                    begin_surface = pg.image.load(os.path.join(BASE_PATH, 'assets/fultano/hat.png')).convert_alpha()
                    sprite = StaticTile(TILE_SIZE, x, y, begin_surface)
                    self.goal.add(sprite)                    

    def enemy_collision_reverse(self):
        '''
        Function that flips skeletons in case they collide
        
        '''
        for skeleton in self.skeleton_sprites.sprites():
            if pg.sprite.spritecollide(skeleton, self.constraint_sprites, False):
                skeleton.reverse()

    def horizontal_movement_collision(self):
        '''
        Function that detects player horizontal collisons.
        
        '''
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        # Checking collisions for each collidable sprite
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
        # Updating game logic variables
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def player_enemy_collision(self):
        '''
        Function that detects enemys collisons.
        
        '''
        player = self.player.sprite
        # Checking collisions for each collidable sprite 
        for sprite in self.enemy_collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if (player.rect.x - sprite.rect.x) > 0:
                    self.player.sprite.collision_side = -1
                else:
                    self.player.sprite.collision_side = 1
                # If Fultano is attacking an enemy
                if player.attacking == True:
                    chan2 = pg.mixer.Channel(2)
                    sound2 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/skeleton-dying.mp3'))
                    chan2.queue(sound2)
                    chan2.set_volume(0.1)
                    # Enemy die
                    sprite.die()
                    self.enemy_collidable_sprites.remove(sprite)
                # Update Fultano health and sprite
                if(player.count_hurted > 1.2 and player.wait_hurt):
                        player.health -= 1
                        player.wait_hurt = False
                elif player.blinking == False:
                    sprite.attack()                
                    player.blinking = True
                    player.wait_hurt = True
                    self.wrong_side = ((self.player.sprite.rect.x - sprite.rect.x > 0 and sprite.previous_speed < 0) or
                                        (sprite.rect.x - self.player.sprite.rect.x > 0 and sprite.previous_speed > 0))                    
                    if(self.wrong_side):
                        sprite.reverse()

    def vertical_movement_collision(self):
        '''
        Function that detects vertical player collisons.
        
        '''
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites()
        # Checking collisions for each collidable sprite  
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0: 
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        # Updating game logic variables
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        '''
        Function that adjusts player X coordinate due to world shift.
        
        '''
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < SCREEN_WIDTH / 2 and direction_x < 0:
            self.world_shift = 12 if self.power_up_is_playing else 8
            player.speed = 0
        elif player_x > SCREEN_WIDTH - (SCREEN_WIDTH / 2) and direction_x > 0:
            self.world_shift = -12 if self.power_up_is_playing else -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 12 if self.power_up_is_playing else 8
    
    def get_player_on_ground(self):
        '''
        Function that gets wheter the player is on ground.
        
        '''
        if self.player_on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def player_power_up(self):
        '''
        Function that detects potion collision.
        
        '''
        player = self.player.sprite
        if self.power_up_is_playing == False:
            player.power_up = False
        # Checking collisions for each collidable sprite 
        for sprite in self.potion_sprites:
            if sprite.rect.colliderect(player.rect):
                player.power_up = True
                player.health = 12
                pg.mixer.quit()
                pg.mixer.init()                
                chan1 = pg.mixer.Channel(1)
                sound1 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/Song-for-Denise.mp3'))
                chan1.queue(sound1)
                chan1.set_volume(0.3)
                self.song_start_time = pg.time.get_ticks()
                self.power_up_is_playing = True
                # Remove potion
                self.potion_sprites.remove(sprite)
    
    def reset_all_level(self):
        '''
        Function that resets the level.
        
        '''
        player = self.player.sprite
        # If the player falls
        if player.rect.bottom >= SCREEN_HEIGHT + 200:
            if (self.void_fall == False):
                pg.mixer.quit()
                pg.mixer.init()
                chan1 = pg.mixer.Channel(1)
                sound1 = pg.mixer.Sound(os.path.join(BASE_PATH, 'media/falling-dying.mp3'))
                chan1.queue(sound1)
                chan1.set_volume(0.1)
            self.void_fall = True
            if player.rect.bottom >= SCREEN_HEIGHT + 5000:
                self.reset_level = True
        # Else if the player dies
        elif player.health == 0:
            self.reset_level = True        
        # Else if goal is reached
        elif self.goal.sprite.rect.colliderect(self.player.sprite.rect):
            self.reset_level = True
            self.advance_level = True
        
    def run(self):
        '''
        Function that runs the level.

        '''
        # Run terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)        
        # Run decoration
        self.decoration_sprites.update(self.world_shift)
        self.decoration_sprites.draw(self.display_surface)
        # Run crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)
        # Run potions
        self.potion_sprites.update(self.world_shift)
        self.potion_sprites.draw(self.display_surface)
        # Run enemies
        self.skeleton_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        
        # Fix draw position
        for skeleton in self.skeleton_sprites:
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
                if(self.wrong_side):
                    skeleton.image = pg.transform.flip(skeleton.image, True, False)
            else:
                skeleton.rect.x -= 25
                skeleton.rect.y -= 15
        self.skeleton_sprites.draw(self.display_surface)
        for skeleton in self.skeleton_sprites:            
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
        self.horizontal_movement_collision()
        self.player_enemy_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.scroll_x()
        self.player_power_up()
        self.reset_all_level()
        # Fix draw position
        shift = 50 if self.player.sprite.power_up else 25
        self.player.sprite.rect.x -= shift
        self.player.draw(self.display_surface)
        self.player.sprite.rect.x += shift
        # Check song time
        if (pg.time.get_ticks() > self.song_start_time + 17000 and self.power_up_is_playing == True) or self.advance_level == True:
            pg.mixer.quit()
            pg.mixer.init()
            if self.advance_level == False:
                if self.player.sprite.health > 8:
                    self.player.sprite.health = 8                
                chan1 = pg.mixer.Channel(1)
                chan1.queue(self.background_song)
                chan1.set_volume(0.1)
                self.power_up_is_playing = False
                self.song_start_time = 0
                self.player.sprite.power_up = False
        # Update sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)
        self.player.sprite.health_sprites.update(0)
        self.player.sprite.health_sprites.draw(self.display_surface)
        self.player.sprite.health_sprites.empty()

        #Debug function
        #self.debug()
        
    def debug(self):
        '''
        Function that draws helpful debugging bounding rectangles.
        
        '''
        # Draw the player's rectangle
        pg.draw.rect(self.display_surface, pg.Color('red'), self.player.sprite.rect, width=4)
        # Draw the goal's rectangle
        pg.draw.rect(self.display_surface, pg.Color('red'), self.goal.sprite.rect, width=4)
        # Draw the skeleton's rectangles
        for skeleton in self.skeleton_sprites:
            pg.draw.rect(self.display_surface, pg.Color('red'), skeleton.rect, width=4)
