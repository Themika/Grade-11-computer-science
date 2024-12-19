import pygame
import os
import time

from Resources.RawReasources.log import Log

class Tree(pygame.sprite.Sprite):
    ANIMATION_SPEED = 60 / 1000

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.idle_images = self.load_images("Animations/Reasources/Tree/Idle")
        self.destroyed_images = self.load_images("Animations/Reasources/Tree/Stump")
        self.current_image = 0
        self.image = self.idle_images[self.current_image]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_counter = 0
        self.health = 100
        self.is_destroyed = False
        self.destroy_time = None
        self.resource_spawned = False  # Flag to track if resource has been spawned

    def load_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                images.append(img)
        return images

    def update(self):
        self.animate()
        if self.is_destroyed and self.destroy_time and time.time() - self.destroy_time >= 0.5:
            self.destroy_time = None
            if not self.resource_spawned:
                self.spawn_resource()

    def animate(self):
        self.animation_counter += self.ANIMATION_SPEED
        if self.animation_counter >= 1:
            self.animation_counter = 0
            if not self.is_destroyed:
                self.current_image = (self.current_image + 1) % len(self.idle_images)
                self.image = self.idle_images[self.current_image]
            elif self.resource_spawned:
                self.current_image = (self.current_image + 1) % len(self.destroyed_images)
                self.image = self.destroyed_images[self.current_image]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and not self.is_destroyed:
            self.health = 0
            self.is_destroyed = True
            self.current_image = 0
            self.destroy_time = time.time()

    def spawn_resource(self):
        if not self.resource_spawned:  # Check if resource has already been spawned
            log = Log(self.x, self.y + 100, "Animations/Reasources/Tree/Logs", self.destroyed_images, "Tiny_Swords_Assets/Resources/Resources/W_Idle.png")
            self.resource_spawned = True  # Set the flag to True after spawning the resource
            return log
        return None