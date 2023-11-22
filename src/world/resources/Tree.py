import pygame, random
from settings import *
from pygame.sprite import Group

from world.resources._Generic import Generic

class Tree(Generic):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, asset) -> None:
        super().__init__(player, pos, random.uniform(.85, 1.65), asset)
        
        # self.image = pygame.transform.rotate(self.original_image, random.choice([0, 90, 180, 270]))
        self.hitbox_radius = (self.rect.width/4)
        