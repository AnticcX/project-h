import pygame, random, string, time
from settings import * 

from Objects.Player import Player
from Objects.resources.Tree import Tree
from Objects.resources.ForestGold import ForestGold
from Objects.resources.ForestStone import ForestStone

from Objects.Assets import Assets

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

    def generate_resource(self,
                          Resource: pygame.sprite.Sprite,
                          render_group: pygame.sprite.Group,
                          number: int, 
                          scale_interval: tuple = (1.0, 1.0),
                          rotation_interval: tuple = (1.0, 1.0)) -> list:
        resources = {}
        for _ in range(number):
            x, y = random.randint(-CHUNK_WIDTH/2, CHUNK_WIDTH/2), random.randint(-CHUNK_HEIGHT/2, CHUNK_HEIGHT/2)
            
            asset = self.Assets.assets[Resource]
            if Resource is Tree: asset = asset[random.randint(0, len(asset) - 1)]
            
            scale = random.uniform(*scale_interval)
            rotation = random.uniform(*rotation_interval)
                
            resources[len(resources)] = {
                "load_obj": Resource,
                "render_group": render_group,
                "asset": asset,
                "coords": (x, y),
                "scale": scale,
                "rotation": rotation
            }
            
        return resources
            
    def generate_resources(self) -> None:
        for resource_obj, render_group in self.resources.items():
            resources = self.generate_resource(resource_obj, render_group, random.randint(0, 25))
            for resource in resources.values():
                self.chunk[resource["coords"]] = resource