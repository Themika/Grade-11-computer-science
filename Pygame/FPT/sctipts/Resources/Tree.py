import pygame
import os
import random
from Resources.RawReasources.log import Log

class Tree(pygame.sprite.Sprite):
    ANIMATION_SPEED = 60 / 1000  # Animation speed for the tree

    def __init__(self, x, y, log_group, reasouces_group):
        super().__init__()
        self.x = x
        self.y = y
        self.idle_images = self.load_images("Animations/Reasources/Tree/Idle")  # Load idle images
        self.destroyed_images = self.load_images("Animations/Reasources/Tree/Stump")  # Load destroyed images
        self.current_image = 0
        self.image = self.idle_images[self.current_image]  # Set initial image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))  # Set position
        self.animation_counter = 0
        self.health = 500  # Initial health of the tree
        self.is_destroyed = False  # Flag to check if the tree is destroyed
        self.logs_spawned = False  # Flag to check if logs are spawned
        self.log_group = log_group  # Group to add logs
        self.reasouces_group = reasouces_group  # Group to add resources

    def load_images(self, folder):
        """Load all images from a folder."""
        images = []
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                images.append(img)
        return images

    def update(self):
        """Update the tree state."""
        self.animate()
        if self.health <= 0 and not self.is_destroyed:
            self.spawn_log()

    def animate(self):
        """Animate the tree."""
        self.animation_counter += self.ANIMATION_SPEED
        if self.animation_counter >= 1:
            self.animation_counter = 0
            if not self.is_destroyed:
                self.current_image = (self.current_image + 1) % len(self.idle_images)
                self.image = self.idle_images[self.current_image]
            else:
                self.current_image = (self.current_image + 1) % len(self.destroyed_images)
                self.image = self.destroyed_images[self.current_image]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface, camera_offset):
        """Draw the tree on the surface with camera offset."""
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)

    def take_damage(self, amount):
        """Reduce the tree's health by the given amount."""
        self.health -= amount
        if self.health <= 0:
            self.is_destroyed = True

    def spawn_log(self):
        """Spawn 3 logs at the tree's location within a 10 by 10 radius and mark the tree as destroyed."""
        if not self.logs_spawned:
            for _ in range(3):
                offset_x = random.randint(-30, 20)
                offset_y = random.randint(-20, 20)
                log = Log(self.rect.centerx + offset_x, self.rect.centery + offset_y, "Animations/Reasources/Tree/Logs/W_Spawn_7.png", 500, "log")
                self.log_group.add(log)
                self.reasouces_group.add(log)
            self.logs_spawned = True
        self.is_destroyed = True