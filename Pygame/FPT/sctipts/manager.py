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

for _ in range(25):
    knight = Knight()
    knight.rect.x = random.randint(0, 2000)
    knight.rect.y = random.randint(0, 2000)
    all_sprites.add(knight)
for _ in range(200):  # Change the number to spawn more or fewer enemies
    enemy = Enemy()
    enemy.rect.x = random.randint(0, 2000)
    enemy.rect.y = random.randint(0, 2000)
    all_sprites.add(enemy)

rps_manager = RPSManager()

clock = pygame.time.Clock()
last_print_time = 0  # Initialize the last print time

while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Check if it is a left click
                mouse_pos = pygame.mouse.get_pos()
                knight.move_to_click_position(mouse_pos)
        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            if event.y > 0:  # Scroll up
                camera.zoom(1.1, mouse_pos, all_sprites)
            elif event.y < 0:  # Scroll down
                camera.zoom(0.9, mouse_pos, all_sprites)
        rps_manager.handle_event(event, camera, all_sprites)

    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(keys, dt)
        elif isinstance(sprite, Knight):
            # Filter out dead enemies dynamically
            alive_enemies = [enemy for enemy in all_sprites if isinstance(enemy, Enemy) and enemy.health > 0]
            sprite.update(dt, alive_enemies)
        elif isinstance(sprite, Enemy):
            if sprite.health <= 0:
                all_sprites.remove(sprite)  # Remove dead enemy
        else:
            sprite.update(dt)
    # Update the camera
    camera.update(player)

    # Render the scene
    display_surface.fill('darkgray')
    draw_grid(display_surface, camera)
    rps_manager.draw_marker(display_surface)
    camera.custom_draw(display_surface, all_sprites)
    pygame.display.update()

pygame.quit()