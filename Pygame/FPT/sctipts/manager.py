import pygame   
from utils.camera import Camera
from player.player import Player
import random

pygame.init()
WINDOW_HIEGHT, WINDOW_WIDTH = 1280,720
display_surface = pygame.display.set_mode((WINDOW_HIEGHT,WINDOW_WIDTH))
running = True
pygame.display.set_caption("Protector of the Realm")



player = Player()
camera = Camera(WINDOW_WIDTH, WINDOW_HIEGHT)
all_sprites = pygame.sprite.Group(player)

def draw_grid(surface, camera):
    for x in range(0, 2000, 100):
        for y in range(0, 2000, 100):
            rect = pygame.Rect(x, y, 100, 100)
            adjusted_rect = rect.move(camera.camera.topleft)
            pygame.draw.rect(surface, (200, 200, 200), adjusted_rect, 1)

while running:
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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_pos = pygame.mouse.get_pos()
                adjusted_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)

    all_sprites.update(keys)
    camera.update(player)

    display_surface.fill('darkgray')
    draw_grid(display_surface, camera)
    camera.custom_draw(display_surface, all_sprites)
    pygame.display.update()

pygame.quit()