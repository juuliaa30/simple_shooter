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

        self.enemies = list()
        self.enemies_count = 5
        pygame.time.set_timer(Enemy().timer, 2000)

        self.bullets = list()

        self.font = pygame.font.SysFont('Arial', 36)


    def draw(self):
        text1 = self.font.render(f"Очки: {self.player.score}", False, (0, 0, 0))
        self.screen.fill((0, 204, 0))
        self.screen.blit(text1, (600, 20))
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
                            enemy.xp -= 1
                            if enemy.xp == 0:
                                self.enemies.remove(enemy)
                                self.player.score += 1

            for obs in self.obstacles:
                if bullet.rect.colliderect(obs):
                    self.bullets.remove(bullet)

        if self.enemies:
            for enemy in self.enemies[:]:

                colliding = any(enemy.rect.colliderect(obs) for obs in self.obstacles)
                if colliding:
                    if not hasattr(enemy, 'original_image'):
                        enemy.original_image = enemy.image.copy()
                        enemy.original_size = enemy.rect.size
                        enemy.original_speed = enemy.speed

                    center = enemy.rect.center
                    enemy.image = pygame.transform.scale(enemy.original_image, (60, 60))
                    enemy.rect = enemy.image.get_rect(center=center)
                elif hasattr(enemy, 'original_image'):
                    center = enemy.rect.center
                    enemy.image = enemy.original_image
                    enemy.rect = enemy.image.get_rect(center=center)

        self.screen.blit(self.player.image, self.player.rect)
        pygame.display.update()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == Enemy().timer:
                if self.enemies_count > 0:
                    self.enemies.append(Enemy())
                    self.enemies_count -= 1
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