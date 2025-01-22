import pygame
import os
import random
from Resources.RawReasources.gold import Gold

class GoldMine(pygame.sprite.Sprite):
    # Initialize the GoldMine object
    def __init__(self, x, y, gold_group, reasources_group):
        super().__init__()
        self.x = x
        self.y = y
        # Load images for different states of the gold mine
        self.idle_image = pygame.image.load("Tiny_Swords_Assets/Resources/Gold Mine/GoldMine_Inactive.png").convert_alpha()
        self.working_image = pygame.image.load("Tiny_Swords_Assets/Resources/Gold Mine/GoldMine_Active.png").convert_alpha()
        self.destroyed_image = pygame.image.load("Tiny_Swords_Assets/Resources/Gold Mine/GoldMine_Destroyed.png").convert_alpha()
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 500
        self.max_health = 500
        self.is_destroyed = False
        self.gold_spawned = False
        self.gold_group = gold_group
        self.reasources_group = reasources_group

    # Update the state of the gold mine
    def update(self):
        if self.health <= 0 and not self.is_destroyed:
            self.take_damage(0)  # Ensure the destroyed state is set

    # Set the gold mine to active state
    def active(self):
        self.image = self.working_image

    # Set the gold mine to inactive state
    def deactive(self):
        self.image = self.idle_image

    # Draw the gold mine and its health bar on the screen
    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
        self.draw_health_bar(surface, adjusted_rect.topleft)

    # Draw the health bar above the gold mine
    def draw_health_bar(self, surface, position):
        bar_width = 50
        bar_height = 5
        health_ratio = self.health / self.max_health
        health_bar_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width * health_ratio, bar_height)
        border_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(surface, (255, 255, 255), border_rect, 1)

    # Apply damage to the gold mine and check if it should be destroyed
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and not self.is_destroyed:
            self.is_destroyed = True
            self.image = self.destroyed_image
            self.spawn_gold()

    # Spawn gold pieces around the destroyed gold mine
    def spawn_gold(self):
        """Spawns 3 gold pieces at the mine's location within a 10 by 10 radius and marks the mine as destroyed."""
        if not self.gold_spawned and not self.is_destroyed:
            for _ in range(3):
                offset_x = random.randint(-30, 20)
                offset_y = random.randint(-20, 20)
                gold = Gold(self.rect.centerx + offset_x, self.rect.centery + offset_y, "Animations/Reasources/Gold_Mine/Gold/G_Spawn_6.png", 500, "gold")
                self.gold_group.add(gold)
                self.reasources_group.add(gold)
            self.gold_spawned = True