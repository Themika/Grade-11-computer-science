import pygame
import os
import random
from Resources.RawReasources.gold import Gold

class GoldMine(pygame.sprite.Sprite):

    def __init__(self, x, y, gold_group,reasources_group):
        super().__init__()
        self.x = x
        self.y = y
        self.idle_image = pygame.image.load("Tiny_Swords_Assets/Resources/Gold Mine/GoldMine_Inactive.png").convert_alpha()
        self.working_image = pygame.image.load("Tiny_Swords_Assets/Resources/Gold Mine/GoldMine_Active.png").convert_alpha()
        self.destroyed_image = pygame.image.load("Tiny_Swords_Assets/Resources/Gold Mine/GoldMine_Destroyed.png").convert_alpha()
        self.image = self.idle_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 500
        self.is_destroyed = False
        self.gold_spawned = False  
        self.gold_group = gold_group  
        self.reasources_group = reasources_group

    def update(self):
        if self.health <= 0 and not self.is_destroyed:
            self.spawn_gold()
    def active(self):
        self.image = self.working_image

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.is_destroyed = True
            self.image = self.destroyed_image

    def spawn_gold(self):
        """Spawns 3 gold pieces at the mine's location within a 10 by 10 radius and marks the mine as destroyed."""
        if not self.gold_spawned:  
            for _ in range(3):
                offset_x = random.randint(-30, 20)
                offset_y = random.randint(-20, 20)
                gold = Gold(self.rect.centerx + offset_x, self.rect.centery + offset_y, "Animations/Reasources/Gold_Mine/Gold/G_Spawn_6.png", 500)
                self.gold_group.add(gold)
                self.reasources_group.add(gold)
            self.gold_spawned = True  
        self.is_destroyed = True