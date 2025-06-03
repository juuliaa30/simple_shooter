import pygame

class Bullet:
    def __init__(self):
        self.image = pygame.image.load('images/bullet.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()