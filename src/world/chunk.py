import random 
import pygame

from settings import *
from world.resources.Tree import Tree
from world.resources.ForestGold import ForestGold
from world.resources.ForestStone import ForestStone
from Assets import Assets

def seed_from_coord_hash(x: int, y: int, seed: int) -> int:
    return (((seed * 73) ^ x) * 73) ^ y

CHUNK_WIDTH = 2500
CHUNK_HEIGHT = 2500

class Chunk:
    def __init__(self, x: int, y: int, world: object) -> None:
        self.x: int = x
        self.y: int = y
        
        self.seed: int = world.seed
        random.seed(seed_from_coord_hash(self.x, self.y, self.seed))
        
        self.chunk: dict = {}
        self.asset_manager: Assets = Assets()
        self.resources = [Tree, ForestGold, ForestStone]
        self.resources_rendered: list = []
        
        self.populate()
    
    def generate_resource(self,
                       Resource: pygame.sprite.Sprite,
                       scale_interval: tuple = (1.0, 1.0)
    ):
        x, y = random.randint(-CHUNK_WIDTH/2, CHUNK_WIDTH/2), random.randint(-CHUNK_HEIGHT/2, CHUNK_HEIGHT/2)
        asset = self.asset_manager.assets[Resource]
        if Resource is Tree: asset = asset[random.randint(0, len(asset) - 1)]
        
        resource = {
            "load_obj": Resource,
            "asset": asset, 
            "coords": pygame.math.Vector2((x, y)),
            "scale": random.uniform(*scale_interval)
        }
        
        self.chunk[(x, y)] = resource
        
    def populate(self) -> None:
        for resource_obj in self.resources:
            for _ in range(random.randint(0, 15)):
                self.generate_resource(resource_obj)
                
    def load(self, render_layers, player) -> None:
        if len(self.resources_rendered) > 0: return
        for resource_data in self.chunk.values():
            Resource = resource_data["load_obj"]
            x, y = resource_data["coords"]
            x += self.x * CHUNK_WIDTH
            y += self.y * CHUNK_HEIGHT
            
            resource = Resource(player, (x, y), resource_data["scale"], resource_data["asset"])
            render_layers[Resource].add(resource)
            self.resources_rendered.append(resource)
            
    def unload(self) -> None:
        for resource in self.resources_rendered:
            resource.kill() 
        self.resources_rendered = []