import pygame   
from os.path import join
from random import randint
#general setup

pygame.init()
WINDOW_HIEGHT, WINDOW_WIDTH = 1280,720
display_surface = pygame.display.set_mode((WINDOW_HIEGHT,WINDOW_WIDTH))
running = True
pygame.display.set_caption("Protector of the Realm")

#Surface
surf = pygame.Surface((100,200))

while running:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    #draw the game
    display_surface.fill('darkgray')
    pygame.display.update()


pygame.quit()