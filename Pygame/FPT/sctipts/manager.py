import pygame
import random
from utils.camera import Camera
from player.player import Player
from allies.knight import Knight
from allies.archer import Archer
from enemy.torch import Torch
from enemy.TNT import TNT
from utils.rps_manager import RPSManager

pygame.init()
WINDOW_HEIGHT, WINDOW_WIDTH = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
running = True
pygame.display.set_caption("Protector of the Realm")

# Load the cursor image
cursor_image = pygame.image.load('Tiny_Swords_Assets/UI/Pointers/01.png')
cursor_image = pygame.transform.scale(cursor_image, (64, 64))  # Scale the image if necessary
cursor_data = pygame.cursors.Cursor((0, 0), cursor_image)
pygame.mouse.set_cursor(cursor_data)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.speed = 5
    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.move_ip(0, self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.move_ip(0, -self.speed)

def draw_grid(surface, camera):
    for x in range(0, 2000, 100):
        for y in range(0, 2000, 100):
            rect = pygame.Rect(x, y, 100, 100)
            adjusted_rect = rect.move(camera.camera.topleft)
            pygame.draw.rect(surface, (200, 200, 200), adjusted_rect, 1)

def draw_grid_coordinates(surface, camera):
    font = pygame.font.SysFont(None, 24)
    for x in range(0, 2000, 100):
        for y in range(0, 2000, 100):
            adjusted_x, adjusted_y = x + camera.camera.topleft[0], y + camera.camera.topleft[1]
            text_surface = font.render(f'({x}, {y})', True, (255, 255, 255))
            surface.blit(text_surface, (adjusted_x + 5, adjusted_y + 5))

player = Player()
camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
all_sprites = pygame.sprite.Group(player)
projectiles = pygame.sprite.Group()

# Create allies and enemies
for _ in range(10):
    archer = Archer()
    archer.rect.topleft = (random.randint(0, 500), random.randint(0, 500))
    all_sprites.add(archer)

for _ in range(10):
    knight = Knight()
    knight.rect.topleft = (random.randint(0, 500), random.randint(0, 500))
    all_sprites.add(knight)

# for _ in range(25):
#     enemy = Torch()
#     enemy.rect.topleft = (random.randint(500, 2000), random.randint(500, 2000))
#     all_sprites.add(enemy)
for _ in range(25):
    enemy = TNT(projectiles)
    enemy.rect.topleft = (random.randint(500, 2000), random.randint(500, 2000))
    all_sprites.add(enemy)

rps_manager = RPSManager()
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check if it is a left click
            rps_manager.handle_event(event, camera, all_sprites)
        elif event.type == pygame.MOUSEWHEEL:
            mouse_pos = pygame.mouse.get_pos()
            camera.zoom(1.1 if event.y > 0 else 0.9, mouse_pos, all_sprites)

    # Update the camera
    camera.update(player)
    # Render the scene
    display_surface.fill('darkgray')
    draw_grid(display_surface, camera)
    draw_grid_coordinates(display_surface, camera)
    camera.custom_draw(display_surface, all_sprites)

    rps_manager.draw_marker(display_surface)
    rps_manager.draw_ui(display_surface)  # Draw the UI elements last to ensure they are on top
    rps_manager.handle_event(event, camera, all_sprites)

    alive_enemies = [enemy for enemy in all_sprites if isinstance(enemy, Torch) or isinstance(enemy, TNT) and enemy.health > 0]
    alive_knights = [ally for ally in all_sprites if isinstance(ally, Knight)]
    alive_archers = [ally for ally in all_sprites if isinstance(ally, Archer)]
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(keys)
        elif isinstance(sprite, Archer):
            sprite.draw(display_surface, camera.camera.topleft)
            sprite.update(dt, alive_enemies)
        elif isinstance(sprite, Knight):
            sprite.update(dt, alive_enemies, alive_knights)
        elif isinstance(sprite, TNT) or isinstance(sprite, Torch):
            sprite.update(alive_knights, alive_archers)

    # Update and draw projectiles
    projectiles.update(dt, alive_knights, alive_archers)
    for projectile in projectiles:
        projectile.draw(display_surface, camera.camera.topleft)

    pygame.display.update()

pygame.quit()