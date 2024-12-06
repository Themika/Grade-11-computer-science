import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(100, 1180), random.randint(100, 620))  # Random position within the screen
        self.health = 50  # Set initial health to 50

    def take_damage(self, amount):
        """Reduce health by the given amount and destroy if health is 0 or less."""
        self.health -= amount
        print(f"Enemy took {amount} damage. Health is now {self.health}.")
        if self.health <= 0:
            self.remove(*self.groups())
            self.kill()
            print("Enemy destroyed.")