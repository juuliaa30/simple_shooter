import pygame

class Player:
    def __init__(self):
        self.image = pygame.image.load('images/Man Blue/manBlue_stand.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.x = 380
        self.y = 550
        self.go_right = pygame.transform.rotate(self.image, -90)
        self.go_left = pygame.transform.rotate(self.image, 90)
        self.go_back = pygame.transform.rotate(self.image, 180)
        self.go_front = pygame.transform.rotate(self.image, 0)

    def update_image(self, keys):
        if keys[pygame.K_a]:
            self.image = self.go_left
        elif keys[pygame.K_d]:
            self.image = self.go_right
        elif keys[pygame.K_s]:
            self.image = self.go_back
        else:
            self.image = self.go_front