import pygame, random, string, time
from settings import * 

from scripts.Player import Player
from scripts.resources.Tree import Tree
from scripts.resources.ForestGold import ForestGold
from scripts.resources.ForestStone import ForestStone

from scripts.Assets import Assets

def seed_from_coord_hash(seed: int, x: int, y: int) -> int:
    return (((seed * 73) ^ x) * 73) ^ y

class Chunk:
    def __init__(self, level, seed: int, coordinates: tuple) -> None:
        self.level = level
        
        self.x, self.y = coordinates
        random.seed(seed_from_coord_hash(seed, self.x, self.y))
        
        
        self.chunk = {}
        self.resources = {
            Tree: self.level.tree_sprites,
            ForestGold: self.level.stone_sprites,
            ForestStone: self.level.stone_sprites
        }
        
        self.Assets = Assets()
        self.generate_resources()
        
        self.resources_rendered = []

    def generate_resource(self,
                          Resource: pygame.sprite.Sprite,
                          render_group: pygame.sprite.Group,
                          number: int, 
                          scale_interval: tuple = (1.0, 1.0),
                          rotation_interval: tuple = (1.0, 1.0)) -> list:
        
        for _ in range(number):
            x, y = random.randint(-CHUNK_WIDTH/2, CHUNK_WIDTH/2), random.randint(-CHUNK_HEIGHT/2, CHUNK_HEIGHT/2)
            
            asset = self.Assets.assets[Resource]
            if Resource is Tree: asset = asset[random.randint(0, len(asset) - 1)]
            
            scale = random.uniform(*scale_interval)
            rotation = random.uniform(*rotation_interval)
                
            resource = {
                "load_obj": Resource,
                "render_group": render_group,
                "asset": asset,
                "coords": (x, y),
                "scale": scale,
                "rotation": rotation
            }
            self.chunk[(x, y)] = resource
            
    def generate_resources(self) -> None:
        for resource_obj, render_group in self.resources.items():
            self.generate_resource(resource_obj, render_group, random.randint(1, 25), (0.35, 1.35), (0, 360))
                
    def load(self) -> None:
        for resource_data in self.chunk.values():
            resource_callable = resource_data["load_obj"]
            resource_x, resource_y = resource_data["coords"]
            x, y = self.x * CHUNK_WIDTH + resource_x, self.y * CHUNK_HEIGHT + resource_y
            rr = resource_callable(
                    self.level.player,
                    (x, y),
                    resource_data["scale"],
                    resource_data["rotation"],
                    resource_data["render_group"],
                    resource_data["asset"]
            )
            self.resources_rendered.append(rr)

    def unload(self) -> None:
        for sprite in self.resources_rendered:
            sprite.kill()
        self.resources_rendered = []