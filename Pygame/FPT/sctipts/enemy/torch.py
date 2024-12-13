import random
import pygame
from .enemy import Enemy  # Assuming Enemy class is in the enemy module

class Torch(Enemy):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.center = self._get_random_position()
        self.health = 200  # Set initial health to 200
        self.speed = 2  # Movement speed
        self.patrol_points = [self._get_random_position() for _ in range(4)]  # Random patrol points within the 2000x2000 map
        self.current_patrol_point = 0
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()  # Initialize the last attack time
        self.attack_animation_frames = []  # List to hold attack animation frames
        self.current_frame = 0  # Current frame of the animation
        self.is_attacking = False  # Flag to check if attacking
        self.facing_right = True  # Initial facing direction

    def _get_random_position(self):
        """Generate a random position within the 2000x2000 map."""
        return random.randint(0, 2000), random.randint(0, 2000)

    def update(self, knights, archers):
        super().update(knights, archers)
        if self.is_attacking:
            self.animate_attack()
        else:
            self.patrol()

    def patrol(self):
        """Move towards the current patrol point."""
        target_x, target_y = self.patrol_points[self.current_patrol_point]
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance < self.speed:
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)
        else:
            self.rect.x += self.speed * dx / distance
            self.rect.y += self.speed * dy / distance

            # Flip the image based on the direction
            if dx > 0 and not self.facing_right:
                self.facing_right = True
                self.flip_image()
            elif dx < 0 and self.facing_right:
                self.facing_right = False
                self.flip_image()

    def attack(self, target):
        """Attack the target."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= 1000:  # Check if 1 second has passed
            damage = 5  # Define the damage amount
            target.take_damage(damage)
            self.last_attack_time = current_time  # Update the last attack time
            self.is_attacking = True  # Set attacking flag to true

    def animate_attack(self):
        """Animate the attack."""
        if self.attack_animation_frames:
            self.current_frame = (self.current_frame + 1) % len(self.attack_animation_frames)
            self.image = self.attack_animation_frames[self.current_frame]
            if self.current_frame == len(self.attack_animation_frames) - 1:
                self.is_attacking = False  # Reset attacking flag after animation ends