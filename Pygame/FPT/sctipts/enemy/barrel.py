import pygame
import random
from utils.projectile import Projectile

class Barrel(pygame.sprite.Sprite):
    ATTACK = 'attack'
    RUN = 'run'
    IDLE = 'idle'
    EXPLODE = 'explode'
    SWIM = 'swim'
    ANIMATION_INTERVAL = 150
    ATTACK_RANGE = 50
    ATTACK_COOLDOWN = 1000
    DAMAGE = 100
    ATTACK_DURATION = 3000  # 3 seconds

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = self._get_random_position()
        self.health = 2000
        self.speed = 2
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()
        self.attack_start_time = None
        self.state = self.RUN
        self.facing_right = True
        self.animations = {
            self.SWIM: [pygame.image.load(f'Animations/Goblins/Bomb/Swim/Barrel_Swim_{i}.png') for i in range(1, 2)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/Bomb/RUN/Barrel_Blue_Run_{i}.png') for i in range(1, 6)],
            self.EXPLODE: [pygame.image.load(f'Animations/Goblins/Explosion/Explosions_{i}.png') for i in range(1, 11)],
        }
        self.current_frame = 0
        self.animation_time = 0
        self.explosion_start_time = None

    def _get_random_position(self):
        return random.randint(0, 2000), random.randint(0, 2000)

    def update(self, buildings, enemies, level_data, allied_enemies):
        current_time = pygame.time.get_ticks()
        if self.state == self.EXPLODE:
            self.health = 0
            self.update_animation(current_time)
            if self.current_frame == len(self.animations[self.EXPLODE]) - 1:
                self.damage_nearby_targets(buildings)
                if self in allied_enemies:
                    allied_enemies.remove(self)
                self.kill()  # Remove the barrel from all sprite groups
            return

        if self.health <= 0:
            self.state = self.EXPLODE
            self.current_frame = 0
            self.explosion_start_time = current_time
            self.update_animation(current_time)
            return

        self.update_animation(current_time)

        if self.is_on_water_tile(level_data):
            self.speed = 1
            self.state = self.SWIM
        else:
            self.speed = 2
            if self.state == self.SWIM:
                self.state = self.RUN

        if self.health < 2000:
            allied_enemies.remove(self)
            self.attacking_target = self.find_nearest_target(enemies)

        if self.attacking_target:
            self.move_towards(self.attacking_target.rect.center)
            if self.distance_to(self.attacking_target.rect.center) <= self.ATTACK_RANGE:
                self.state = self.EXPLODE
                self.current_frame = 0
                self.explosion_start_time = current_time
                self.update_animation(current_time)
        else:
            nearest_target = self.find_nearest_target(buildings)
            if nearest_target:
                self.move_towards(nearest_target.rect.center)
                if self.distance_to(nearest_target.rect.center) <= self.ATTACK_RANGE:
                    self.state = self.EXPLODE
            else:
                self.state = self.RUN

    def is_on_water_tile(self, level_data, TILE_SIZE=65):
        tile_x, tile_y = self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
        if 0 <= tile_y < len(level_data) and 0 <= tile_x < len(level_data[0]):
            return level_data[tile_y][tile_x][0] == 40  # Assuming 40 is the water tile ID
        return False

    def find_nearest_target(self, targets):
        rect_center = pygame.Vector2(self.rect.center)
        return min(targets, key=lambda target: rect_center.distance_to(pygame.Vector2(target.rect.center)), default=None)

    def move_towards(self, target):
        target_vec = pygame.Vector2(target)
        current_vec = pygame.Vector2(self.rect.center)
        direction = (target_vec - current_vec).normalize()
        self.rect.center += direction * self.speed
        self.update_facing_direction(direction.x)

    def update_facing_direction(self, dx):
        if (dx > 0 and not self.facing_right) or (dx < 0 and self.facing_right):
            self.facing_right = not self.facing_right
            self.flip_image()

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def take_damage(self, damage, attacker=None):
        self.health -= damage
        if attacker:
            self.attacking_target = attacker

    def damage_nearby_targets(self, targets):
        for target in targets:
            if self.rect.colliderect(target.rect.inflate(self.ATTACK_RANGE, self.ATTACK_RANGE)):
                target.take_damage(self.DAMAGE)

    def update_animation(self, current_time):
        if self.state != 'dead' and current_time - self.animation_time > self.ANIMATION_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.animation_time = current_time
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def distance_to(self, target):
        return pygame.Vector2(self.rect.center).distance_to(pygame.Vector2(target))
