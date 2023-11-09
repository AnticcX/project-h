import pygame, random
from settings import *
from pygame.sprite import Group

class Generic(pygame.sprite.Sprite):
    def __init__(self, player: pygame.sprite.Sprite, pos: tuple, scale: float, rendered_group: Group, unrendered_group: Group, asset_path: str) -> None:
        super().__init__(rendered_group)
        self.player = player
        
        self.g_rendered = rendered_group
        self.g_unrendered = unrendered_group

        self.rendered: bool = True
        
        self.original_image = pygame.image.load(asset_path).convert_alpha()
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, scale)
        self.image = pygame.transform.rotate(self.original_image, random.choice([0, 90, 180, 270]))
        
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
        
    def update(self, events, dt):
        if not self.on_screen() and self.rendered:
            self.g_rendered.remove(self)
            self.g_unrendered.add(self)
            self.rendered = False
            return
        elif self.on_screen() and not self.rendered:
            self.g_rendered.add(self)
            self.g_unrendered.remove(self)
            self.rendered = True
            
        if not self.rendered: return
        
        self.pos = self.get_position_on_screen()
        self.rect.center = self.pos