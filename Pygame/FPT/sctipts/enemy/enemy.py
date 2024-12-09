import random 
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 100), random.randint(0, 100))  # Random position within the screen
        self.health = 50  # Set initial health to 50

    def take_damage(self, amount):
        """Reduce health by the given amount and destroy if health is 0 or less."""
        self.health -= amount
        if self.health <= 0:
            # Remove from all sprite groups and kill
            self.remove(*self.groups())  # Remove from all groups
            self.kill()  # Ensure it's destroyed from the scene
