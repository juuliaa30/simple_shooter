import pygame
from random import randint

class Enemy:
    def __init__(self):
        self.image = pygame.image.load('images/roach.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(topleft=(randint(0, 770), -40))
        self.timer = pygame.USEREVENT + 1
        self.speed = 1
        self.xp = 2
        self.size = (40,40)

    def update(self):
        self.rect.y += self.speed