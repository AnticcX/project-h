import pygame, math, random
from pygame.sprite import Group
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple) -> None:
        super().__init__()
        self.original_image = pygame.image.load("./src/assets/player.png").convert_alpha()
        self.original_image = pygame.transform.rotozoom(self.original_image, 0, 0.55)
        self.image = self.original_image
        
        self.rect = self.image.get_rect()
        self.rect.center = pygame.display.get_surface().get_rect().center
        
        self.pos = pygame.math.Vector2(pygame.display.get_surface().get_rect().center)
        self.coords = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2()
        self.max_speed = 3500
        self.speed = self.max_speed
        self.rotation = 0
        
        self.hitbox_radius = (self.rect.width/3.14) * 0.45
        self.id = random.randint(0, 10000000000000)
        
        self.camera_coords = pygame.math.Vector2(pos)
        self.main_player = None
        
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
        
        self.pos = self.get_position_on_screen()
        self.rect.center = self.pos
        
    def lerp(self, a, b, f) -> None:
        return a * (1.0 - f) + (b * f)
        
    def camera_follow(self, dt) -> None:
        self.camera_coords = self.lerp(self.camera_coords, self.coords, self.speed * dt * .01)
            
    def turn(self, mouse_pos):
        x, y = mouse_pos
        dx, dy = x - self.rect.centerx, y - self.rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) + 90
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.55, -self.rect.height * 0.55))
        self.rotation = angle
    
    def get_position_on_screen(self) -> tuple:
        player_coords = self.camera_coords
        if self.main_player:
            player_coords = self.main_player.coords
        return pygame.math.Vector2((self.coords.x - player_coords.x + SCREEN_WIDTH/2, self.coords.y - player_coords.y + SCREEN_HEIGHT/2))
    
    def _turn(self):
        self.image = pygame.transform.rotate(self.original_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)
        
    def update(self, dt):
        if not self.main_player:
            self.input()
            self.movement(dt)
            mouse_pos = pygame.mouse.get_pos()
            self.turn(mouse_pos)
            self.camera_follow(dt)
        else:
            self._turn()
            self.pos = self.get_position_on_screen()
            self.rect.center = self.pos
        # pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), self.pos, self.hitbox_radius, 1)