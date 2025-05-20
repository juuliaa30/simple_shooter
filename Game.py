import pygame
from Player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.screen.fill((0, 204, 0))
        self.player = Player()

        self.player.rect.center = (400, 300)

    def run(self):
        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            self.screen.blit(self.player.image, (380, 520))

            pygame.display.update()