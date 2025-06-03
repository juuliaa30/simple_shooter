import pygame
from Player import Player
from Enemy import Enemy
from Bullet import Bullet
import json
from random import randint

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True

        self.load_levels()
        self.current_level = 0
        self.setup_level(self.current_level)

    def load_levels(self):
        with open('levels.json', 'r') as f:
            self.levels_data = json.load(f)['levels']

    def setup_level(self, level_num):
        level = self.levels_data[level_num]

        self.player = Player()
        self.player.rect.center = (380, 550)
        self.screen.blit(self.player.image, self.player.rect)

        self.obstacles = [
            pygame.Rect(obs['x'], obs['y'], obs['width'], obs['height'])
            for obs in level['obstacles']
        ]

        self.enemies = []
        self.enemies_count = level['enemies_count']
        self.enemy_speed = level['enemy_speed']
        self.enemy_size = level['enemy_size']
        self.enemy_xp = level['enemy_xp']


        pygame.time.set_timer(Enemy().timer, 2000)

        self.bullets = list()

        self.font = pygame.font.SysFont('Arial', 36)

        self.show_level_message(level_num + 1)

    def show_level_message(self, level_num):
        self.screen.fill((0, 204, 0))
        level_text = self.font.render(f"Уровень {level_num}", True, (255, 255, 255))
        info_text = self.font.render("Нажмите любую клавишу для продолжения", True, (255, 255, 255))

        self.screen.blit(level_text, (
            400 - level_text.get_width() // 2,
            300 - level_text.get_height() // 2
        ))
        self.screen.blit(info_text, (
            400 - info_text.get_width() // 2,
            350 - info_text.get_height() // 2
        ))

        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    waiting = False

    def check_level_complete(self):
        level = self.levels_data[self.current_level]
        if self.player.score >= level['score_required']:
            self.current_level += 1
            if self.current_level < len(self.levels_data):
                self.setup_level(self.current_level)
            else:
                self.show_game_complete()
                self.running = False

    def show_game_complete(self):
        self.screen.fill((0, 204, 0))
        complete_text = self.font.render("Поздравляем! Игра пройдена!", True, (255, 255, 255))
        score_text = self.font.render(f"Финальный счет: {self.player.score}", True, (255, 255, 255))

        self.screen.blit(complete_text, (
            400 - complete_text.get_width() // 2,
            250 - complete_text.get_height() // 2
        ))
        self.screen.blit(score_text, (
            400 - score_text.get_width() // 2,
            300 - score_text.get_height() // 2
        ))

        pygame.display.flip()
        pygame.time.wait(3000)

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

        if self.enemies:
            for enemy in self.enemies[:]:
                if enemy.rect.y > 600 or enemy.rect.colliderect(self.player):
                    self.running = False

        self.screen.blit(self.player.image, self.player.rect)
        self.check_level_complete()
        pygame.display.update()

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False
            if e.type == Enemy().timer:
                if self.enemies_count > 0:
                    enemy = Enemy()
                    enemy.speed = self.enemy_speed
                    enemy.xp = self.enemy_xp
                    enemy.image = pygame.transform.scale(
                        pygame.image.load('images/roach.png').convert_alpha(),
                        self.enemy_size
                    )
                    enemy.image = pygame.transform.rotate(enemy.image, 180)
                    enemy.rect = enemy.image.get_rect(topleft=(randint(0, 770), -40))
                    self.enemies.append(enemy)
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