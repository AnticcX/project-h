import pygame, sys
from settings import *
from client import Client

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(PROJECT_NAME)
        
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.debug_font = pygame.font.SysFont("freesans", 16)
        self.clock = pygame.time.Clock()
        
        self.client: Client = Client()
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   
                    pygame.quit()
                    self.client.network.running = False
                    sys.exit()
                
            dt = self.clock.tick() / 1000
            self.client.run(dt)
            
            img = self.debug_font.render(f'FPS: {int(self.clock.get_fps())}', True, (255, 255, 255))
            self.window.blit(img, (10, 10))
            pygame.display.update()

if __name__ == '__main__':
    game = Game()
    game.run()