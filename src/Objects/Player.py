import pygame, math
from settings import *
from pygame.sprite import Group

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, *groups: Group) -> None:
        super().__init__(*groups)
        self.original_image = pygame.image.load("./src/assets/player.png").convert_alpha()
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, 0.65)
        self.image = self.original_image
        
        self.rect = self.image.get_rect()
        self.rect.center = pygame.display.get_surface().get_rect().center
        
        self.pos = pygame.math.Vector2(pygame.display.get_surface().get_rect().center)
        self.coords = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.speed = 2000
        
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.75, -self.rect.height * 0.75))
        
    def input(self) -> None:
        key = pygame.key.get_pressed()
        up = key[pygame.K_w] or key[pygame.K_UP]
        down = key[pygame.K_s] or key[pygame.K_DOWN]
        left = key[pygame.K_a] or key[pygame.K_LEFT]
        right = key[pygame.K_d] or key[pygame.K_RIGHT]
        
        self.direction = pygame.math.Vector2(right - left, down - up)
        
    def movement(self, dt) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            
        self.coords.x += self.direction.x * self.speed * dt
        self.coords.y += self.direction.y * self.speed * dt
        
    def turn(self, mouse_pos):
        x, y = mouse_pos
        dx, dy = x - self.rect.centerx, y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) + 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.55, -self.rect.height * 0.55))
        
    def update(self, dt):
        self.input()
        self.movement(dt)
        mouse_pos = pygame.mouse.get_pos()
        self.turn(mouse_pos)