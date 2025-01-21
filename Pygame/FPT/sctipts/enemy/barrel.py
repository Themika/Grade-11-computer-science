import pygame 
import random

class Barrel(pygame.sprite.Sprite):
    ATTACK = 'attack'
    RUN = 'run'
    IDLE = 'idle'
    ANIMATION_INTERVAL = 150
    ATTACK_RANGE = 50
    ATTACK_COOLDOWN = 1000
    DAMAGE = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = self._get_random_position()
        self.health = 100
        self.speed = 2
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()
        self.state = self.RUN
        self.facing_right = True
        self.animations = {
            self.ATTACK: [pygame.image.load(f'Animations/Goblins/Bomb/Attack/Barrel_Blue_Attack_{i}.png') for i in range(1, 3)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/Bomb/RUN/Barrel_Blue_Run_{i}.png') for i in range(1, 6)],
        }
        self.current_frame = 0
        self.animation_time = 0

    def _get_random_position(self):
        return random.randint(0, 2000), random.randint(0, 2000)

    def update(self, houses, towers, level_data, enemies):
        if self.health <= 0:
            self.state = 'dead'
            if self in enemies:
                enemies.remove(self)
            self.kill()
        current_time = pygame.time.get_ticks()
        self.update_animation(current_time)

        nearest_target = self.find_nearest_target(houses + towers)
        if nearest_target:
            self.move_towards(nearest_target.rect.center)
            self.attack_if_close([nearest_target], [])
        self.update_state()

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
        if dx > 0 and not self.facing_right:
            self.facing_right = True
            self.flip_image()
        elif dx < 0 and self.facing_right:
            self.facing_right = False
            self.flip_image()

    def flip_image(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def attack_if_close(self, houses, towers):
        for target in houses + towers:
            if self.rect.colliderect(target.rect.inflate(self.ATTACK_RANGE, self.ATTACK_RANGE)):
                self.attacking_target = target
                self.attack(target)
                return
        self.attacking_target = None

    def attack(self, target):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.ATTACK_COOLDOWN:
            target.take_damage(self.DAMAGE)
            self.last_attack_time = current_time
            self.state = self.ATTACK
            self.current_frame = 0
        else:
            self.state = self.RUN

    def update_state(self):
        if self.attacking_target:
            self.state = self.ATTACK
        else:
            self.state = self.RUN

    def update_animation(self, current_time):
        if self.state != 'dead' and current_time - self.animation_time > self.ANIMATION_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.animation_time = current_time
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def distance_to(self, target):
        dx, dy = self.rect.centerx - target[0], self.rect.centery - target[1]
        return (dx**2 + dy**2) ** 0.5
