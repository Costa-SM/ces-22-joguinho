import pygame as pg

class CameraGroup(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()

        # ground
        ground_surface_aux = pg.image.load('assets/background/background_1.png')
        self.ground_surface = pg.transform.scale(ground_surface_aux, (2000, 600)).convert_alpha()
        self.ground_rect = self.ground_surface.get_rect(topleft = (0, 0))

        # camera offset
        self.offset = pg.math.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2

    def center_target_camera(self, target):
        self.offset.x = target.rect.left - 150

    def custom_draw(self, player):

        self.center_target_camera(player)

        # ground
        ground_offset = self.ground_rect.topleft - self.offset
        self.display_surface.blit(self.ground_surface, ground_offset)

        # dinamic sprites
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
        