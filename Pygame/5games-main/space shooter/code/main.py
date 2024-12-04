import pygame   
from os.path import join
from random import randint
#general setup

pygame.init()
WINDOW_HIEGHT, WINDOW_WIDTH = 1280,720
display_surface = pygame.display.set_mode((WINDOW_HIEGHT,WINDOW_WIDTH))
running = True
pygame.display.set_caption("Space Shooter")

#Surface
surf = pygame.Surface((100,200))
x = 1280
y = 720
path = join('images',"player.png")
player_surf = pygame.image.load(f'{path}').convert_alpha()
path_to_star = join('images',"star.png")
star_surf = pygame.image.load(f'{path_to_star}').convert_alpha()
#Tupple of random star position
star_posiotion = [(randint(0,WINDOW_HIEGHT),randint(0,WINDOW_WIDTH)) for x in range(20)]

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
    for pos in star_posiotion:
        display_surface.blit(star_surf, (pos))
    x+=1
    y+=1
    display_surface.blit(player_surf, (x/2,y/2))
    pygame.display.update()


pygame.quit()