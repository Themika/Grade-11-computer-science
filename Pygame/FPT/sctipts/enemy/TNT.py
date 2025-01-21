import pygame
import random
from .enemy import Enemy
from utils.projectile import Dynamite

class TNT(Enemy):
    ATTACK_1 = 'attack_1'
    RUN = 'run'
    IDLE = 'idle'
    SEARCH = 'search'
    SWIM = 'swim'
    ANIMATION_INTERVAL = 100
    ATTACK_COOLDOWN = 1100  # Cooldown time for attacks
    DAMAGE = 1  # Damage dealt by the TNT
    ATTACK_RANGE = 300  # Attack range in pixels
    MIN_DISTANCE = 15  # Minimum distance between TNT enemies
    MAP_WIDTH = 2000  # Width of the map
    MAP_HEIGHT = 2000  # Height of the map

    def __init__(self, projectiles_group, tilemap, *groups):
        super().__init__(tilemap, *groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('orange')
        self.rect = self.image.get_rect()
        self.rect.center = self._get_random_position()
        self.health = 150  # Set initial health to 500
        self.speed = 2  # Movement speed
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()  # Initialize the last attack time
        self.state = self.RUN
        self.facing_right = True
        self.projectiles_group = projectiles_group  # Store the projectiles group

        self.animations = {
            self.ATTACK_1: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Attack_1/TNT_Blue_Attack_1_{i}.png') for i in range(1, 7)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Run/TNT_Blue_Run_{i}.png') for i in range(1, 6)],
            self.IDLE: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Idle/TNT_Blue_Idle_{i}.png') for i in range(1, 6)],
            self.SEARCH: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Run/TNT_Blue_Run_{i}.png') for i in range(1, 6)],
            self.SWIM: [pygame.image.load(f'Animations/Goblins/TNT/Blue/Swimming/TNT_Blue_Swim_{i}.png') for i in range(1, 2)]
        }
        self.current_frame = 0
        self.animation_time = 0

    def _get_random_position(self):
        """Generate a random position within the 2000x2000 map."""
        return random.randint(0, self.MAP_WIDTH), random.randint(0, self.MAP_HEIGHT)

    def update(self, knights, archers, level_data, enemies,alive_tnt):
        self.update_animation()
        self.set_min_distance(alive_tnt)
        if self.health <= 0:
            if self in enemies:
                enemies.remove(self)
            self.kill()  # Destroy the TNT enemy if health is below zero
            return
        nearest_target = self.find_nearest_target(knights, archers)
        if nearest_target:
            self.move_towards(nearest_target.rect.center, enemies)
            self.attack(nearest_target, enemies)

        self.update_state(level_data)

    def is_on_water_tile(self, level_data, TILE_SIZE=65):
        tile_x, tile_y = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
        if 0 <= tile_y < len(level_data) and 0 <= tile_x < len(level_data[0]):
            if level_data[tile_y][tile_x][0] == 40:
                return True
        return False

    def find_nearest_target(self, knights, archers):
        """Find the nearest target (knight or archer)."""
        targets = knights + archers
        if not targets:
            return None
        nearest_target = min(targets, key=lambda target: self.distance_to(target.rect.center))
        return nearest_target

    def attack(self, target, enemies):
        current_time = pygame.time.get_ticks()
        distance = self._get_distance_to_target(target)
        if distance <= self.ATTACK_RANGE and current_time - self.last_attack_time >= self.ATTACK_COOLDOWN:
            target.take_damage(self.DAMAGE)
            self.last_attack_time = current_time
            self.state = self.ATTACK_1
            self.current_frame = 0  # Reset animation frame
            self.shoot_projectile(target)
        elif distance > self.ATTACK_RANGE:
            self.move_towards(target.rect.center, enemies)  # Move closer to the target if not within attack range

    def _get_distance_to_target(self, target):
        """Calculate the distance to the target."""
        dx = target.rect.centerx - self.rect.centerx
        dy = target.rect.centery - self.rect.centery
        return (dx ** 2 + dy ** 2) ** 0.5

    def shoot_projectile(self, target):
        if target:
            dx = target.rect.centerx - self.rect.centerx
            dy = target.rect.centery - self.rect.centery
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance != 0:
                dx, dy = dx / distance, dy / distance
            dynamite = Dynamite(self.rect.center, target.rect.center, 5, "Animations/Goblins/TNT/Dynamite_Anim/Dynamite_1.png")
            self.projectiles_group.add(dynamite)  # Add the projectile to the projectiles group
            # Determine the direction of the target and set facing_right accordingly
            self.facing_right = dx > 0

    def move_towards(self, target_position, enemies):
        """Move the TNT enemy towards the target position while maintaining distance from other TNT enemies."""
        dx, dy = target_position[0] - self.rect.centerx, target_position[1] - self.rect.centery
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance != 0:
            dx, dy = dx / distance, dy / distance  # Normalize the direction vector
            self.rect.centerx += dx * self.speed
            self.rect.centery += dy * self.speed
            self.facing_right = dx > 0  # Update facing direction based on movement

        # Maintain distance from other TNT enemies
        for enemy in enemies:
            if enemy is not self:
                ex, ey = enemy.rect.centerx, enemy.rect.centery
                edx, edy = self.rect.centerx - ex, self.rect.centery - ey
                edistance = (edx ** 2 + edy ** 2) ** 0.5
                if edistance < self.MIN_DISTANCE and edistance != 0:
                    edx, edy = edx / edistance, edy / edistance  # Normalize the direction vector
                    self.rect.centerx += edx * self.speed
                    self.rect.centery += edy * self.speed

        # Ensure the TNT enemy does not move out of bounds
        self.rect.centerx = max(0, min(self.rect.centerx, self.MAP_WIDTH))
        self.rect.centery = max(0, min(self.rect.centery, self.MAP_HEIGHT))

    def update_state(self, level_data):
        if self.state == self.ATTACK_1 and self.current_frame == len(self.animations[self.ATTACK_1]) - 1:
            self.state = self.IDLE
        elif self.attacking_target:
            if self.state != self.SWIM:
                self.state = self.ATTACK_1
        elif self.is_on_water_tile(level_data):
            self.speed = 1
            self.state = self.SWIM
        else:
            self.speed = 2
            self.state = self.RUN

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_time > self.ANIMATION_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.animation_time = current_time
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
    def set_min_distance(self, enemies):
        """Set the minimum distance between TNT ene`mies after all have spawned."""
        if all(enemy.state != self.ATTACK_1 for enemy in enemies):
            self.MIN_DISTANCE = 20

