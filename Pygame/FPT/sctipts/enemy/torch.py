import random
import pygame
import math
from enemy.enemy import Enemy  # Assuming Enemy class is in the enemy module

class Torch(Enemy):
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'
    ATTACK_3 = 'attack_3'
    RUN = 'run'
    IDLE = 'idle'
    SEARCH = 'search'
    SWIM = 'swim'  # New swim state
    ANIMATION_INTERVAL = 150  # Increased interval to slow down animations
    ATTACK_RANGE = 50
    ATTACK_COOLDOWN = 1000
    DAMAGE = 10
    DIRECTION_CHANGE_THRESHOLD = 0.1

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = self._get_random_position()
        self.health = 100  # Set initial health to 200
        self.speed = 3  # Increased movement speed
        self.patrol_points = [self._get_random_position() for _ in range(4)]  # Random patrol points within the 2000x2000 map
        self.current_patrol_point = 0
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()  # Initialize the last attack time
        self.state = self.RUN
        self.facing_right = True
        self.start_position = self.rect.center
        self.animations = {
            self.ATTACK_1: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Attack_1/Torch_Blue_Attack_1_{i}.png') for i in range(1, 6)],
            self.ATTACK_2: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Attack_2/Torch_Blue_Attack_2_{i}.png') for i in range(1, 6)],
            self.ATTACK_3: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Attack_3/Torch_Blue_Attack_3_{i}.png') for i in range(1, 6)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Run/Torch_Blue_Run_{i}.png') for i in range(1, 6)],
            self.IDLE: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Idle/Torch_Blue_Idle_{i}.png') for i in range(1, 6)],
            self.SEARCH: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Run/Torch_Blue_Run_{i}.png') for i in range(1, 6)],
            self.SWIM: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Swimming/Torch_Blue_Swimming_{i}.png') for i in range(1,2)]  # Add swim animations
        }
        self.current_frame = 0
        self.animation_time = 0

        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 20)

    def _get_random_position(self):
        """Generate a random position within the 2000x2000 map."""
        return random.randint(0, 2000), random.randint(0, 2000)

    def update(self, knights, archers, level_data, enemies,alive_torch):
        if self.health <= 0:
            self.state = 'dead'
            if self in enemies:
                enemies.remove(self)
            self.kill()
        current_time = pygame.time.get_ticks()
        self.update_animation(current_time)

        nearest_target = self.find_nearest_target(knights + archers)
        if nearest_target:
            self.move_towards(nearest_target.rect.center)
            self.attack_if_close([nearest_target], [])
        self.update_state(level_data)
        self.maintain_minimum_distance(alive_torch)

    def maintain_minimum_distance(self, enemies, min_distance=25):
        for enemy in enemies:
            if enemy is not self:
                distance = self.distance_to(enemy.rect.center)
                if distance < min_distance:
                    dx, dy = self.rect.centerx - enemy.rect.centerx, self.rect.centery - enemy.rect.centery
                    distance = (dx**2 + dy**2) ** 0.5
                    if distance != 0:
                        dx, dy = dx / distance, dy / distance
                        self.rect.centerx += dx * (min_distance - distance) / 2
                        self.rect.centery += dy * (min_distance - distance) / 2
                        enemy.rect.centerx -= dx * (min_distance - distance) / 2
                        enemy.rect.centery -= dy * (min_distance - distance) / 2


    def is_on_water_tile(self, level_data, TILE_SIZE=65):
        tile_x, tile_y = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
        if 0 <= tile_y < len(level_data) and 0 <= tile_x < len(level_data[0]):
            if level_data[tile_y][tile_x][0] == 40:  # Assuming 40 is the water tile identifier
                return True
        return False

    def find_nearest_target(self, targets):
        nearest_target = None
        min_distance = float('inf')
        for target in targets:
            distance = self.distance_to(target.rect.center)
            if distance < min_distance:
                min_distance = distance
                nearest_target = target
        return nearest_target

    def move_towards(self, target):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        distance = (dx**2 + dy**2) ** 0.5
        if distance != 0:
            dx, dy = dx / distance, dy / distance
            self.rect.centerx += dx * self.speed
            self.rect.centery += dy * self.speed
            self.update_facing_direction(dx)

    def update_facing_direction(self, dx):
        if abs(dx) > self.DIRECTION_CHANGE_THRESHOLD:
            if dx > 0 and not self.facing_right:
                self.facing_right = True
                self.flip_image()
            elif dx < 0 and self.facing_right:
                self.facing_right = False
                self.flip_image()

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def attack_if_close(self, knights, archers):
        for target in knights + archers:
            if self.rect.colliderect(target.rect.inflate(self.ATTACK_RANGE, self.ATTACK_RANGE)):
                self.attacking_target = target
                self.attack(target)
                return
        self.attacking_target = None  # Reset attacking target if no target is close

    def attack(self, target):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.ATTACK_COOLDOWN:
            target.take_damage(self.DAMAGE)
            self.last_attack_time = current_time
            if self.rect.centery < target.rect.centery:
                self.state = self.ATTACK_2
            else:
                self.state = self.ATTACK_1
            self.current_frame = 0  # Reset animation frame
        else:
            self.state = self.RUN  # Transition back to RUN state after attack

    def update_state(self,level_data):
        if self.attacking_target:
            if self.rect.centery > self.attacking_target.rect.centery:
                self.state = self.ATTACK_2
            elif self.rect.centery < self.attacking_target.rect.centery:
                self.state = self.ATTACK_3
            else:
                self.state = self.ATTACK_1
        if self.is_on_water_tile(level_data):
            self.state = self.SWIM
        else:
            self.state = self.RUN  # Ensure state transitions back to RUN when not attacking
            if self.health <= 0:
                self.state = 'dead'
                self.kill()

    def update_animation(self, current_time):
        if self.state != 'dead' and current_time - self.animation_time > self.ANIMATION_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.animation_time = current_time
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)