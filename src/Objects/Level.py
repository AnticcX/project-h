import pygame, random, string, time
from settings import * 

from Objects.Player import Player
from Objects.resources.Tree import Tree
from Objects.resources.ForestGold import ForestGold
from Objects.resources.ForestStone import ForestStone

from Objects.Assets import Assets

class UnrenderedSprites:
    def get_position_on_screen(self, player_pos, sprite_pos) -> tuple:
        px, py = player_pos
        sx, sy = sprite_pos 
        return sx - px, sy - py
        
    def on_screen(self, player_pos, sprite_pos):
        x, y = self.get_position_on_screen(player_pos, sprite_pos)
        
        if (x >= 0 - UNRENDER_BOUND_X and x <= SCREEN_WIDTH + UNRENDER_BOUND_X) and (y >= 0 - UNRENDER_BOUND_Y and y <= SCREEN_HEIGHT + UNRENDER_BOUND_Y): return True
        else: return False

class Level:
    def __init__(self) -> None:
        self.window = pygame.display.get_surface()
        self.Assets = Assets()
        self.unrendered = UnrenderedSprites()
        self.check_unrendered_time = time.time()
        
        # Sprites
        self.player_sprites = pygame.sprite.Group() # This will include this like player body, hands, armor, cosmetics, etc.
        self.tree_sprites = pygame.sprite.Group() # All trees
        self.stone_sprites = pygame.sprite.Group() # All stones like gold, stone, diamond, amythesist, etc.
        
        # Index determines layer. Ex. 0 = top layer, 1 = next layer, etc.
        self.render_layers = [
            self.tree_sprites,
            self.stone_sprites,
            self.player_sprites
        ]
        self.render_layers.reverse()
        
        self.world_resources: dict = {}
        self.generate_world() 
        
    def generate_world(self) -> None:
        self.player = Player((0, 0), self.player_sprites)
        
        self.generate_world_resource(Tree, self.tree_sprites, 200)
        self.generate_world_resource(ForestGold, self.stone_sprites, 200)
        self.generate_world_resource(ForestStone, self.stone_sprites, 200)
    
    def generate_world_resource(self,
                          Resource: pygame.sprite.Sprite,
                          render_group: pygame.sprite.Group,
                          number: int, 
                          scale_interval: tuple = (1.0, 1.0),
                          rotation_interval: tuple = (1.0, 1.0)) -> None:
        for _ in range(number):
            x, y = random.randint(-MAP_WIDTH/2, MAP_WIDTH/2), random.randint(-MAP_WIDTH/2, MAP_HEIGHT/2)
            
            UID = '%032x' % random.getrandbits(128)
            while UID in self.world_resources: UID = '%032x' % random.getrandbits(128)
            
            asset = self.Assets.assets[Resource]
            if Resource is Tree: asset = asset[random.randint(0, len(asset) - 1)]
            
            self.world_resources[UID] = {
                "load_obj": Resource,
                "rendered": False,
                "render_group": render_group,
                "asset": asset,
                "coords": (x, y),
                "scale": random.uniform(*scale_interval),
                "rotation": random.uniform(*rotation_interval)
            }
    
    def check_unrendered(self) -> None:
        # (player: Sprite, pos: tuple, scale: float, rotation: float, rendered_group: Group, asset: Any) -> None
        for UID, resource_data in self.world_resources.items():
            if not resource_data["rendered"] and self.unrendered.on_screen(self.player.coords, resource_data["coords"]):
                resource_callable = resource_data["load_obj"]
                resource_callable(
                    self.player,
                    resource_data["coords"],
                    resource_data["scale"],
                    resource_data["rotation"],
                    resource_data["render_group"],
                    resource_data["asset"]
                )
                resource_data["rendered"] = True
                self.world_resources[UID] = resource_data
            elif resource_data["rendered"] and not self.unrendered.on_screen(self.player.coords, resource_data["coords"]):
                resource_data["rendered"] = False
                self.world_resources[UID] = resource_data
            
    def run(self, dt) -> None:
        self.window.fill(DAY_BACKGROUND)
        
        for render_layer in self.render_layers:
            render_layer.draw(self.window)
            render_layer.update(dt)
            
        self.check_unrendered()