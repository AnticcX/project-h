import pygame, random
from settings import *
from pygame.sprite import Group

from Objects.resources._Generic import Generic

class ForestGold(Generic):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, rotation: float, rendered_group: Group, asset) -> None:
        super().__init__(player, pos, scale, rotation, rendered_group, asset)