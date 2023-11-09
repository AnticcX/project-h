import pygame, random
from settings import * 
from Objects.Player import Player
from Objects.resources.Tree import Tree
from Objects.resources.ForestGold import ForestGold
from Objects.resources.ForestStone import ForestStone

class Level():
    def __init__(self) -> None:
        self.window = pygame.display.get_surface()
        self.title = pygame.font.SysFont("freesans", 48)
        self.debug_font = pygame.font.SysFont("freesans", 16)

        self.user_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.stone_sprites = pygame.sprite.Group()
        
        # Index determines layer. Ex. 0 = top layer, 1 = next layer, etc.
        self.resource_sprites = [self.tree_sprites, self.stone_sprites]
        self.unrendered_sprites = pygame.sprite.Group()
        
        self.foliage: list = []
        
        self.events = {}
        self.movement_dir = pygame.math.Vector2()
        
        self.setup()
    
    def setup(self) -> None:
        img = self.title.render('Loading game..', True, (255, 255, 255))
        img_rect = img.get_rect()
        img_center = (self.window.get_rect().centerx - (img_rect.width / 2), self.window.get_rect().centery - img_rect.height / 2)
        self.window.blit(img, img_center)
        pygame.display.update()
        
        self.player = Player((0,0), self.user_sprites)
        self.add_resources(Tree, self.tree_sprites, 1000)
        self.add_resources(ForestStone, self.stone_sprites, 1000)
        self.add_resources(ForestGold, self.stone_sprites, 500)

    
    def add_resources(self, Resource: pygame.sprite.Sprite, Group: pygame.sprite.Group, number: int, scale_interval: tuple = (1, 1)) -> None:
        scale_int_lower, scale_int_upper = scale_interval
        
        for _ in range(number): 
            x, y = random.randint(-MAP_WIDTH/2, MAP_WIDTH/2), random.randint(-MAP_WIDTH/2, MAP_HEIGHT/2)
            self.foliage.append(Resource(
                                self.player,
                                (x, y), 
                                random.uniform(scale_int_lower, scale_int_upper), 
                                Group, 
                                self.unrendered_sprites
                                ))
    
    def run(self, dt) -> None:
        if self.movement_dir != [0, 0] and not ("player_movement" in self.events):
            self.events["player_movement"] = {"movement_dir": self.movement_dir, "player_speed": self.player.speed}
        elif "player_movement" in self.events: del self.events["player_movement"]
        
        self.window.fill(DAY_BACKGROUND)
        
        self.user_sprites.draw(self.window)
        self.user_sprites.update(dt)
        
        # Draw resources
        for resource_sprite in self.resource_sprites:
            resource_sprite.draw(self.window)
            resource_sprite.update(self.events, dt)
        
        self.unrendered_sprites.update(self.events, dt)
        
        resources_rendered = sum([len(list(i)) for i in self.resource_sprites])
        img = self.debug_font.render(f'Resources Sprites Rendered: {resources_rendered}', True, (255, 255, 255))
        self.window.blit(img, (10, 10 + img.get_rect().height))
        
        # pygame.draw.rect(self.window, (255, 255, 0), self.player.hitbox, 2)