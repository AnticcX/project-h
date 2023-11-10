import pygame, random
from settings import *
from pygame.sprite import Group

class Generic(pygame.sprite.Sprite):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, rotation: float, rendered_group: Group, asset) -> None:
        super().__init__(rendered_group)
        self.player = player
        
        self.g_rendered = rendered_group

        self.rendered: bool = True
        
        self.original_image = pygame.transform.rotozoom(asset, 0, scale)
        self.image = pygame.transform.rotate(self.original_image, rotation)
        
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.coords = pygame.math.Vector2(pos)
        self.pos = self.get_position_on_screen()
        
    def get_position_on_screen(self) -> tuple:
        player_coords = self.player.coords
        return pygame.math.Vector2((self.coords.x - player_coords.x, self.coords.y - player_coords.y))
        
    def on_screen(self):
        x, y = self.get_position_on_screen()
        screen_error_x, screen_error_y = UNRENDER_BOUND_X + (self.rect.width / 2), UNRENDER_BOUND_Y + (self.rect.height / 2)
        
        if (x >= 0 - screen_error_x and x <= SCREEN_WIDTH + screen_error_x) and (y >= 0 - screen_error_y and y <= SCREEN_HEIGHT + screen_error_y): return True
        else: return False
        
    def update(self, dt):
        if not self.on_screen() and self.rendered:
            self.kill()
            return 
        
        self.pos = self.get_position_on_screen()
        self.rect.center = self.pos