import pygame
from Player import Player

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))


        self.player = Player()
        self.player.rect.center = (380, 550)

        self.obstacles = [
            pygame.Rect(150, 450, 50, 50),
            pygame.Rect(650, 450, 50, 50),
            pygame.Rect(350, 450, 125, 50)
        ]

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_a] and self.player.x > 0:
            dx = -self.player.speed
        if keys[pygame.K_d] and self.player.x < 750:
            dx = self.player.speed
        if keys[pygame.K_w] and self.player.y > 400:
            dy = -self.player.speed
        if keys[pygame.K_s] and self.player.y < 560:
            dy = self.player.speed

        self.player.rect.x += dx
        self.player.rect.y += dy

        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle):
                if dx > 0:
                    self.player.rect.right = obstacle.left
                elif dx < 0:
                    self.player.rect.left = obstacle.right
                if dy > 0:
                    self.player.rect.bottom = obstacle.top
                elif dy < 0:
                    self.player.rect.top = obstacle.bottom

        self.player.x = self.player.rect.x
        self.player.y = self.player.rect.y

    def run(self):
        running = True
        while running:

            self.screen.fill((0, 204, 0))

            for obstacle in self.obstacles:
                pygame.draw.rect(self.screen, (153, 76, 0), obstacle)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.screen.blit(self.player.go_left, (self.player.x, self.player.y))
            elif keys[pygame.K_d]:
                self.screen.blit(self.player.go_right, (self.player.x, self.player.y))
            elif keys[pygame.K_s]:
                self.screen.blit(self.player.go_back, (self.player.x, self.player.y))
            else:
                self.screen.blit(self.player.image, (self.player.x, self.player.y))

            self.handle_movement()

            pygame.display.update()
            self.clock.tick(60)