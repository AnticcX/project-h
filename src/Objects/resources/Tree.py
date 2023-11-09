import pygame, random
from settings import *
from pygame.sprite import Group

from Objects.resources._Generic import Generic

class Tree(Generic):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, rendered_group: Group, unrendered_group: Group) -> None:
        super().__init__(player, pos, scale, rendered_group,  unrendered_group, f"./src/assets/trees/{random.randint(0, 5)}.png")
        self.image = pygame.transform.rotate(self.original_image, random.choice([0, 90, 180, 270]))