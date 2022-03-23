import pygame as pg
import resources
from utils import *

class Monster(pg.sprite.Sprite):
  """
  Represents a monster
  """
  def __init__(self, pos_x, pos_y):
    """
    Creates a monster

    :param position: the position of the monster
    :type position: 2x1 int vector
    """
    super().__init__()
    self.sprites, self.rect = resources.load_sprite('skeleton', 2)
    self.current_state = 'ready'
    self.current_sprite = 0
    self.img = self.sprites[self.current_state][self.current_sprite]
    self.image = pg.transform.flip(self.img, 1, 0)

    self.rect.topleft = [pos_x, pos_y]

    self.speed = 0
    self.health = 30
    self.damage = 20

  def update(self, speed):
    self.current_sprite += speed

    if self.current_sprite >= len(self.sprites[self.current_state]):
      self.current_sprite = 0

    self.img = self.sprites[self.current_state][int(self.current_sprite)]
    self.image = pg.transform.flip(self.img, 1, 0)