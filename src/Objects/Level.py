import pygame
from settings import * 
from Objects.Player import Player

class Level():
    def __init__(self) -> None:
        self.window = pygame.display.get_surface()
        self.sprites = pygame.sprite.Group()
        
        self.setup()
    
    def setup(self) -> None:
        self.player = Player(self.window.get_rect().center, self.sprites)
    
    def run(self, dt) -> None:
        self.window.fill((13, 79, 53))
        self.sprites.draw(self.window)
        self.sprites.update(dt)