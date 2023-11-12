import pygame, random
from settings import *
from pygame.sprite import Group

class Generic(pygame.sprite.Sprite):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, rotation: float, rendered_group: Group, asset) -> None:
        super().__init__()
        self.player = player
        
        self.g_rendered = rendered_group
        
        self.original_image = pygame.transform.rotozoom(asset, 0, scale)
        self.image = pygame.transform.rotate(self.original_image, rotation)
        
        self.rect = self.image.get_rect()
        
        self.coords = pygame.math.Vector2(pos)
        
        self.g_rendered.add(self)
        
    def get_position_on_screen(self) -> tuple:
        player_coords = self.player.coords
        return pygame.math.Vector2((self.coords.x - player_coords.x, self.coords.y - player_coords.y))
        
    def update(self, dt):
        
        self.pos = self.get_position_on_screen()
        self.rect.center = self.pos