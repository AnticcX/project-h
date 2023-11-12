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
        self.max_speed = 400
        self.speed = self.max_speed
        
        self.hitbox_radius = (self.rect.width/3.14) * 0.65
        self.hitbox = self.rect.copy().inflate((-self.rect.width*0.75, -self.rect.height * 0.75))
        self.collided = False
        
    def collide(self, chunks, dt) -> None:
        for chunk in chunks.values():
            for sprite in chunk.resources_rendered:
                if sprite.collide(self):
                    direction = pygame.math.Vector2(sprite.collision_dir(self))
                    repulsion_speed = self.max_speed * 0.85
                    
                    self.coords.x += direction.x * repulsion_speed  * dt
                    self.coords.y += direction.y * repulsion_speed * dt
                    self.collided = True
                    div_velocity = self.speed * 15
                    self.speed -= self.max_speed/(div_velocity if div_velocity > 0 else 1)
                    if self.speed <= repulsion_speed: self.speed = repulsion_speed
                    return
        else:
            self.collided = False
            self.speed = self.max_speed
        
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
        # pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), self.pos, self.hitbox_radius, 1)