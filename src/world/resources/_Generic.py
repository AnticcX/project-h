import pygame, random, math
from settings import *
from pygame.sprite import Group

class Generic(pygame.sprite.Sprite):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, asset) -> None:
        super().__init__()
        self.player = player
        
        self.original_image = pygame.transform.rotozoom(asset, 0, scale)
        self.image = pygame.transform.rotate(self.original_image, 0)
        
        self.rect = self.image.get_rect()
        
        self.coords = pygame.math.Vector2(pos)
        self.pos = self.get_position_on_screen()
        self.rect.center = self.pos
        
    def get_position_on_screen(self) -> tuple:
        player_coords = self.player.coords
        return pygame.math.Vector2((self.coords.x - player_coords.x, self.coords.y - player_coords.y))
        
    def collide(self, entity) -> bool:
        return math.sqrt(math.pow(self.pos.x - entity.pos.x, 2) + math.pow(self.pos.y - entity.pos.y, 2)) < (self.hitbox_radius + entity.hitbox_radius)
    
    def collision_dir(self, entity):
        dx = self.pos.x - entity.pos.x
        dy = self.pos.y - entity.pos.y
        dist = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))

        force = 1
        return (-force if dx > 0 else force, -force if dy > 0 else force)
    
    def update(self, dt):
        
        self.pos = self.get_position_on_screen()
        self.rect.center = self.pos
        
        # pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), self.pos, self.hitbox_radius, 1)