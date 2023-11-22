import pygame, random
from settings import *
from pygame.sprite import Group

from world.resources._Generic import Generic

class ForestStone(Generic):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, asset) -> None:
        super().__init__(player, pos, scale, asset)
        
        self.hitbox_radius = (self.rect.width/2) - 15 * scale