import math
import pygame

from network import Network
from Player import Player
from world.world import World
from world.chunk import Chunk
from Thread import Thread
from settings import *

from world.resources.Tree import Tree
from world.resources.ForestGold import ForestGold
from world.resources.ForestStone import ForestStone

class Client:
    def __init__(self) -> None:
        self.window: pygame.surface.Surface = pygame.display.get_surface()
        self.player: Player = Player((0, 0))
        self.network: Network = Network(self.player)
        self.world: World = None
        self.thread = Thread()
        self.rock_group = pygame.sprite.Group()
        self.render_layers = {
            Player: pygame.sprite.Group(),
            Tree: pygame.sprite.Group(),
            ForestGold: self.rock_group,
            ForestStone: self.rock_group
        }
        
        self.players: dict = {}
        self.view_chunks: list = []
        
        self.generate_player(self.player)
        
    def generate_player(self, player: Player) -> None:
        self.render_layers[Player].add(player)
        
    def load_new_player(self, player_id: str, data: dict):
        player = Player(data["player_coords"])
        player.main_player = self.player
        self.players[player_id] = player
        self.generate_player(player)
        print(f"{player_id} has connected to the server!")
        
    def update_rendered_players(self, player_id, data) -> None:
        player: Player = self.players[player_id]
        player.rotation = data["player_rotation"]
        player.coords = data["player_coords"]
        
    def get_world(self) -> None:
        packet = self.network.received_packet
        if packet and "world" in packet:
            self.world = packet["world"]
    
    def load_worker(self) -> None:
        coordinates = [
                (-1, 1), (0, 1), (1, 1),
                (-1, 0), (0, 0), (1, 0),
                (-1, -1),(0, -1),(1, -1)
        ]
        for coord in coordinates:
            x, y = coord 
            coords = (int((x * CHUNK_WIDTH + self.player.coords.x) / CHUNK_WIDTH), int((y * CHUNK_HEIGHT + self.player.coords.y)/ CHUNK_HEIGHT))
            if coords in self.view_chunks: continue
            
            self.thread.add_queue(self.world.load_chunk, coords)
            self.view_chunks.append(coords)
            
    def unload_worker(self) -> None:
        for coords in self.view_chunks.copy():
            x, y = coords 
            px, py = self.player.coords
            x *= CHUNK_WIDTH; y *= CHUNK_HEIGHT
            dx = math.pow(x - px, 2)
            dy = math.pow(y - py, 2)
            if math.sqrt(dx + dy) >= CHUNK_WIDTH * 3:
                self.view_chunks.remove(coords)
                chunk: Chunk = self.world.chunks[coords]
                self.thread.add_queue(chunk.unload)
                
    def render_chunks(self) -> None:
        for coords in self.view_chunks:
            try:
                chunk: Chunk = self.world.chunks[coords]
                self.thread.add_queue(chunk.load, (self.render_layers, self.player))
            except KeyError:
                pass
            
    def run(self, dt) -> None:
        self.window.fill(DAY_BACKGROUND)
        for layer in self.render_layers.values():
            layer.draw(self.window) 
            layer.update(dt)
            
        packet = self.network.received_packet 
        if packet and "world" not in packet:
            for player_id, data in dict(packet).items():
                if player_id == self.player.id: continue
                if not player_id in self.players: self.load_new_player(player_id, data)
                self.update_rendered_players(player_id, data)
                
        self.get_world()
        if self.world:
            self.load_worker()
            self.unload_worker() 
            self.render_chunks()
            
        self.thread.run_queue()
            