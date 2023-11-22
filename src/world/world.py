import random

from world.chunk import Chunk
from settings import *


class World:
    def __init__(self) -> None:
        self.seed: int = random.randint(0, 10000000)
        self.chunks: dict = {}
        self.loaded_chunks: list = []
        
    def load_chunk(self, x: int, y: int) -> None:
        if not (x, y) in self.chunks:
            chunk = Chunk(x, y, self)
            self.chunks[(x, y)] = chunk 
            
        chunk: Chunk = self.chunks[(x, y)]
        self.chunks[(x, y)] = chunk
    
            