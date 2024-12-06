import pygame   
from utils.camera import Camera
from player.player import Player
from allies.knight import Knight
from enemy.enemy import Enemy
from utils.rps_manager import RPSManager
import random

pygame.init()
WINDOW_HIEGHT, WINDOW_WIDTH = 1280,720
display_surface = pygame.display.set_mode((WINDOW_HIEGHT,WINDOW_WIDTH))
running = True
pygame.display.set_caption("Protector of the Realm")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HIEGHT // 2))
        self.speed = 5

    def update(self, keys, dt):
        if keys[pygame.K_LEFT]:
            self.rect.x += self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y += self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y -= self.speed

def draw_grid(surface, camera):
    for x in range(0, 2000, 100):
        for y in range(0, 2000, 100):
            rect = pygame.Rect(x, y, 100, 100)
            adjusted_rect = rect.move(camera.camera.topleft)
            pygame.draw.rect(surface, (200, 200, 200), adjusted_rect, 1)

player = Player()
camera = Camera(WINDOW_WIDTH, WINDOW_HIEGHT)
all_sprites = pygame.sprite.Group(player)

# Create a knight and add it to the center of the screen
knight_1 = Knight()
all_sprites.add(knight_1)

# Create an enemy and add it to the screen
enemy_1 = Enemy()
all_sprites.add(enemy_1)

rps_manager = RPSManager()

clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if event.y > 0:  # Scroll up
                camera.zoom(1.1, mouse_pos, all_sprites)
            elif event.y < 0:  # Scroll down
                camera.zoom(0.9, mouse_pos, all_sprites)
        rps_manager.handle_event(event, camera, all_sprites)

    # Update player with keys and dt, update knight with dt only
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(keys, dt)
        elif isinstance(sprite, Knight):
            sprite.update(dt, [enemy_1])
        else:
            sprite.update(dt)

    camera.update(player)

    display_surface.fill('darkgray')
    draw_grid(display_surface, camera)
    rps_manager.draw_marker(display_surface)
    camera.custom_draw(display_surface, all_sprites)
    pygame.display.update()

pygame.quit()