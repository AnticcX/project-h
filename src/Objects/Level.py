import pygame, random, threading, time, math
from settings import * 

from Objects.Chunk import Chunk
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
        
        self.chunks: dict = {}
        self.generate_world() 
        self.thread = threading.Thread(target=self.load_chunks)
        self.thread.start()
        
    def generate_world(self) -> None:
        self.player = Player((0, 0), self.player_sprites)
    
    def unload_chunks(self) -> None:
        for coord in self.chunks.copy():
            x, y = coord
            px, py = self.player.coords
            x *= CHUNK_WIDTH; y *= CHUNK_HEIGHT
            dx = math.pow(x - px, 2)
            dy = math.pow(y - py, 2)
            if math.sqrt(dx + dy) >= CHUNK_WIDTH * 2:
                for sprite in self.chunks[coord]["rendered_resources"]:
                    sprite.kill()
                del self.chunks[coord]
            
    def load_chunks(self) -> None:
        while True:
            coordinates = [
                (-1, 1), (0, 1), (1, 1),
                (-1, 0), (0, 0), (1, 0),
                (-1, -1),(0, -1),(1, -1)
            ]
            for coord in coordinates:
                x, y = coord 
                coords = (int((x * CHUNK_WIDTH + self.player.coords.x) / CHUNK_WIDTH), int((y * CHUNK_HEIGHT + self.player.coords.y)/ CHUNK_HEIGHT))
                if coords in self.chunks: continue
                
                chunk = Chunk(self, 1, coords)
                resource_rendered = []
                for resource_data in chunk.chunk.values():
                    resource_callable = resource_data["load_obj"]
                    resource_x, resource_y = resource_data["coords"]
                    x, y = coords[0] * CHUNK_WIDTH + resource_x, coords[1] * CHUNK_HEIGHT + resource_y
                    rr = resource_callable(
                            self.player,
                            (x, y),
                            resource_data["scale"],
                            resource_data["rotation"],
                            resource_data["render_group"],
                            resource_data["asset"]
                    )
                    resource_rendered.append(rr)
                    
                resource_data["chunk"] = chunk
                self.chunks[coords] = {
                    "chunk_data": chunk,
                    "rendered_resources": resource_rendered
                }
            
            # TEMP FIX FOR NOT CLOSING
            try: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:   
                        return
            except: return
            time.sleep(0.0005)
        

    def run(self, dt) -> None:
        self.window.fill(DAY_BACKGROUND)
        
        for render_layer in self.render_layers:
            try:
                render_layer.draw(self.window)
                render_layer.update(dt)
            except Exception as e:
                pass
        self.unload_chunks()
