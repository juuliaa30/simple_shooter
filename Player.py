import pygame

class Player:
    def __init__(self):
        self.image = pygame.image.load('images/Man Blue/manBlue_stand.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()