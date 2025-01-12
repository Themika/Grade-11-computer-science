import pygame
import random
from .enemy import Enemy
from utils.projectile import Dynamite

class TNT(Enemy):
    ATTACK_1 = 'attack_1'
    RUN = 'run'
    IDLE = 'idle'
    SEARCH = 'search'
    ANIMATION_INTERVAL = 100
    ATTACK_COOLDOWN = 1100  # Cooldown time for attacks
    DAMAGE = 1  # Damage dealt by the TNT
    ATTACK_RANGE = 350  # Attack range in pixels

    def __init__(self, projectiles_group, tilemap, *groups):
        super().__init__(tilemap, *groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.center = self._get_random_position()
        self.health = 500  # Set initial health to 500
        self.speed = 2  # Movement speed
        self.patrol_points = [self._get_random_position() for _ in range(4)]  # Random patrol points within the 2000x2000 map
        self.current_patrol_point = 0
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()  # Initialize the last attack time
        self.state = self.RUN
        self.facing_right = True
        self.projectiles_group = projectiles_group  # Store the projectiles group

        self.animations = {
            self.ATTACK_1: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Attack_1/TNT_Blue_Attack_1_{i}.png') for i in range(1, 7)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Run/TNT_Blue_Run_{i}.png') for i in range(1, 6)],
            self.IDLE: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Idle/TNT_Blue_Idle_{i}.png') for i in range(1, 6)],
            self.SEARCH: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Run/TNT_Blue_Run_{i}.png') for i in range(1, 6)]
        }
        self.current_frame = 0
        self.animation_time = 0

    def _get_random_position(self):
        """Generate a random position within the 2000x2000 map."""
        return random.randint(0, 2000), random.randint(0, 2000)

    def update(self, knights, archers):
        super().update(knights, archers)
        self.update_animation()
        if self.health <= 0:
            self.kill()  # Destroy the TNT enemy if health is below zero

    def attack(self, target):
        current_time = pygame.time.get_ticks()
        distance = self._get_distance_to_target(target)
        if distance <= self.ATTACK_RANGE and current_time - self.last_attack_time >= self.ATTACK_COOLDOWN:
            target.take_damage(self.DAMAGE)
            self.last_attack_time = current_time
            self.state = self.ATTACK_1
            self.current_frame = 0  # Reset animation frame
            self.shoot_projectile(target)

    def _get_distance_to_target(self, target):
        """Calculate the distance to the target."""
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        return (dx ** 2 + dy ** 2) ** 0.5

    def shoot_projectile(self, target):
        if target:
            dynamite = Dynamite(self.rect.center, target.rect.center, 5, "Animations/Goblins/TNT/Dynamite_Anim/Dynamite_1.png")
            self.projectiles_group.add(dynamite)  # Add the projectile to the projectiles group
            # Determine the direction of the target and set facing_right accordingly
            dx = target.rect.centerx - self.rect.centerx
            self.facing_right = dx > 0

    def update_state(self):
        if self.attacking_target:
            self.state = self.ATTACK_1
        else:
            super().update_state()

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_time > self.ANIMATION_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.animation_time = current_time
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)