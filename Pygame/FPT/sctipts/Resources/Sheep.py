import pygame
import random
import time

class Sheep(pygame.sprite.Sprite):
    shared_target_pos = None  # Shared target position for all sheep

    def __init__(self, x, y, all_sheep):
        super().__init__()
        self.images = [pygame.image.load(f'Animations/Reasources/Sheep/Run/HappySheep_Bouncing_{i}.png') for i in range(1, 6)]  # Load your sheep animation frames
        self.images = [pygame.transform.scale(image, (image.get_width() * 1.5, image.get_height() * 1.5)) for image in self.images]  # Scale images to be larger
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_index = 0
        self.animation_time = 0.1
        self.last_update = time.time()
        self.idle_time = 3
        self.last_idle = time.time()
        if Sheep.shared_target_pos is None:
            Sheep.shared_target_pos = self.get_random_position()
        self.direction = 1  # 1 for right, -1 for left
        self.all_sheep = all_sheep
        self.velocity = pygame.math.Vector2(0, 0)

    def get_random_position(self):
        return random.randint(0, 800), random.randint(0, 600)  # Assuming screen size is 800x600

    def update(self):
        current_time = time.time()
        if current_time - self.last_idle > self.idle_time:
            Sheep.shared_target_pos = self.get_random_position()
            self.last_idle = current_time

        self.apply_boids_rules()

        if current_time - self.last_update > self.animation_time:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)  # Flip image if moving left
            self.last_update = current_time

        target_vector = pygame.math.Vector2(Sheep.shared_target_pos) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 1:
            self.velocity = target_vector.normalize() * 2  # Move towards the target position
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Update direction based on velocity
        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1

        # Prevent overlapping
        self.prevent_overlap()

    def apply_boids_rules(self):
        separation = self.separation()
        alignment = self.alignment()
        cohesion = self.cohesion()

        self.velocity += separation + alignment + cohesion
        self.velocity = self.velocity.normalize() * 2  # Limit speed

    def separation(self):
        steer = pygame.math.Vector2(0, 0)
        for sheep in self.all_sheep:
            if sheep != self:
                distance = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(sheep.rect.center)
                if 0 < distance.length() < 50:  # Reduced separation distance to 50 pixels
                    steer += distance.normalize() / distance.length()
                    # Push sheep away from each other
                    overlap = 25 - distance.length()  # Reduced overlap distance
                    steer += distance.normalize() * overlap
        return steer * 1.5  # Increased separation factor to 1.5

    def alignment(self):
        avg_velocity = pygame.math.Vector2(0, 0)
        for sheep in self.all_sheep:
            if sheep != self:
                avg_velocity += sheep.velocity
        avg_velocity /= len(self.all_sheep) - 1
        return (avg_velocity - self.velocity) * 0.1  # Increased alignment factor to 0.1

    def cohesion(self):
        center_mass = pygame.math.Vector2(0, 0)
        for sheep in self.all_sheep:
            if sheep != self:
                center_mass += pygame.math.Vector2(sheep.rect.center)
        center_mass /= len(self.all_sheep) - 1
        return (center_mass - pygame.math.Vector2(self.rect.center)) * 0.15  # Increased cohesion factor to 0.15

    def prevent_overlap(self):
        for sheep in self.all_sheep:
            if sheep != self and self.rect.colliderect(sheep.rect):
                overlap_vector = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(sheep.rect.center)
                if overlap_vector.length() > 0:
                    overlap_vector = overlap_vector.normalize() * 1  # Reduced overlap adjustment
                    self.rect.x += overlap_vector.x
                    self.rect.y += overlap_vector.y

    def take_damage(self, amount):
        # Implement the logic for taking damage
        pass
    