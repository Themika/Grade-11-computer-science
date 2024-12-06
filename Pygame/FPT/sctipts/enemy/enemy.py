import pygame
import random
class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, 1180), random.randint(100, 620))  # Random position within the screen