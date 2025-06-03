import pygame
from Player import Player
from Enemy import Enemy
from Bullet import Bullet

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True


        self.player = Player()
        self.player.rect.center = (380, 550)
        self.screen.blit(self.player.image, self.player.rect)

        self.obstacles = [
            pygame.Rect(150, 450, 50, 50),
            pygame.Rect(650, 450, 50, 50),
            pygame.Rect(350, 450, 125, 50)
        ]

        self.enemies = [Enemy() for _ in range(1)]
        pygame.time.set_timer(Enemy().timer, 2000)

        self.bullets = list()

    def draw(self):
        self.screen.fill((0, 204, 0))
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, (153, 76, 0), obstacle)

        for ememy in self.enemies:
            self.screen.blit(ememy.image, ememy.rect)

        if self.bullets:
            for bullet in self.bullets:
                self.screen.blit(bullet.image, bullet.rect)
                bullet.rect.y -= 10

                if bullet.rect.y < 0:
                    self.bullets.remove(bullet)

                if self.enemies:
                    for enemy in self.enemies:
                        if bullet.rect.colliderect(enemy):
                            self.bullets.remove(bullet)
                            self.enemies.remove(enemy)

        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.update()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == Enemy().timer:
                self.enemies.append(Enemy())
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    bullet = Bullet()
                    bullet.rect.midbottom = self.player.rect.midtop
                    self.bullets.append(bullet)


    def update(self):
        keys = pygame.key.get_pressed()
        self.player.update_image(keys)

        dx, dy = 0, 0
        if keys[pygame.K_a] and self.player.rect.left > 0:
            dx = -self.player.speed
        if keys[pygame.K_d] and self.player.rect.right < 800:
            dx = self.player.speed
        if keys[pygame.K_w] and self.player.rect.top > 400:
            dy = -self.player.speed
        if keys[pygame.K_s] and self.player.rect.bottom < 600:
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

        for enemy in self.enemies:
            enemy.update()

    def run(self):
        while self.running:
            self.draw()
            self.handle_events()
            self.update()
            self.clock.tick(60)