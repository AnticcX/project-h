import pygame

from scripts.resources.Tree import Tree
from scripts.resources.ForestGold import ForestGold
from scripts.resources.ForestStone import ForestStone

class Assets:
    def __init__(self) -> None:
        self.window = pygame.display.get_surface()
        self.assets = {
            Tree: {
                0: pygame.image.load(f"./src/assets/trees/0.png").convert_alpha(),
                1: pygame.image.load(f"./src/assets/trees/1.png").convert_alpha(),
                2: pygame.image.load(f"./src/assets/trees/2.png").convert_alpha(),
                3: pygame.image.load(f"./src/assets/trees/3.png").convert_alpha(),
                4: pygame.image.load(f"./src/assets/trees/4.png").convert_alpha()
            },
            ForestStone: pygame.image.load(f"./src/assets/forest_stone.png").convert_alpha(),
            ForestGold: pygame.image.load(f"./src/assets/forest_gold.png").convert_alpha()
        }