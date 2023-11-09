import pygame, random
from settings import *
from pygame.sprite import Group

from Objects.resources._Generic import Generic

class ForestGold(Generic):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, rendered_group: Group, unrendered_group: Group) -> None:
        super().__init__(player, pos, scale, rendered_group,  unrendered_group, "./src/assets/forest_gold.png")
        self.image = pygame.transform.rotate(self.original_image, random.uniform(0, 360))