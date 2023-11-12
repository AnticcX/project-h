import pygame, random, threading, time, math
from settings import * 

from scripts.Chunk import Chunk
from scripts.Thread import Thread
from scripts.Player import Player
from scripts.resources.Tree import Tree
from scripts.resources.ForestGold import ForestGold
from scripts.resources.ForestStone import ForestStone

from scripts.Assets import Assets

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
        self.thread = Thread()
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
        
    def generate_world(self) -> None:
        self.player = Player((0, 0), self.player_sprites)
    
    def unload_chunks(self) -> None:
        for coord in self.chunks.copy():
            x, y = coord
            px, py = self.player.coords
            x *= CHUNK_WIDTH; y *= CHUNK_HEIGHT
            dx = math.pow(x - px, 2)
            dy = math.pow(y - py, 2)
            if math.sqrt(dx + dy) >= CHUNK_WIDTH * 3:
                self.thread.add_queue(self.chunks[coord].unload)
                del self.chunks[coord]
            
    def generate_chunks(self) -> None:
            coordinates = [
                (-1, 1), (0, 1), (1, 1),
                (-1, 0), (0, 0), (1, 0),
                (-1, -1),(0, -1),(1, -1)
            ]
            for coord in coordinates:
                x, y = coord 
                coords = (int((x * CHUNK_WIDTH + self.player.coords.x) / CHUNK_WIDTH), int((y * CHUNK_HEIGHT + self.player.coords.y)/ CHUNK_HEIGHT))
                if coords in self.chunks: continue
                
                chunk = Chunk(self, 10, coords)
                self.thread.add_queue(chunk.load)
                self.chunks[coords] = chunk
        

    def run(self, dt) -> None:
        self.window.fill(DAY_BACKGROUND)
        
        for render_layer in self.render_layers:
            render_layer.draw(self.window)
            render_layer.update(dt)
        self.generate_chunks()
        self.unload_chunks()
        self.thread.run_queue()

        self.player.collide(self.chunks, dt)