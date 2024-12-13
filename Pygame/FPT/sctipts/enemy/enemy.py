import random
import pygame

class Enemy(pygame.sprite.Sprite):
    IDLE = 'idle'
    RUN = 'run'
    SEARCH = 'search'
    ATTACK_RANGE = 0.2
    DAMAGE = 1
    ATTACK_COOLDOWN = 1000
    ANIMATION_INTERVAL = 100

    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill('red')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, 2000), random.randint(0, 2000))
        self.health = 200
        self.speed = 2
        self.patrol_points = [(random.randint(0, 2000), random.randint(0, 2000)) for _ in range(4)]
        self.current_patrol_point = 0
        self.attacking_target = None
        self.last_attack_time = pygame.time.get_ticks()
        self.state = self.RUN
        self.facing_right = True

        self.animations = {
            self.IDLE: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Idle/Torch_Blue_Idle_{i}.png') for i in range(1, 8)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Run/Torch_Blue_Run_{i}.png') for i in range(1, 7)],
            self.SEARCH: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Run/Torch_Blue_Run_{i}.png') for i in range(1, 7)]
        }
        self.current_frame = 0
        self.animation_time = 0

    def update(self, knights, archers):
        if self.attacking_target and self.attacking_target.health > 0:
            self.attack_if_close([self.attacking_target], [])
        else:
            self.attacking_target = None
            self.patrol()
            self.attack_if_close(knights, archers)

        self.update_state()
        self.update_animation()

    def patrol(self):
        target = self.patrol_points[self.current_patrol_point]
        if self.distance_to(target) > 1:
            self.state = self.RUN
            self.move_towards(target)
        else:
            self.state = self.IDLE
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

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

    def attack_if_close(self, knights, archers):
        for target in knights + archers:
            if self.rect.colliderect(target.rect.inflate(self.ATTACK_RANGE, self.ATTACK_RANGE)):
                self.attacking_target = target
                self.attack(target)
                return

    def attack(self, target):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time >= self.ATTACK_COOLDOWN:
            target.take_damage(self.DAMAGE)
            self.last_attack_time = current_time

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.remove(*self.groups())
            self.kill()

    def update_state(self):
        self.state = self.IDLE if self.attacking_target else self.RUN

    def update_animation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_time > self.ANIMATION_INTERVAL:
            self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])
            self.image = self.animations[self.state][self.current_frame]
            self.animation_time = current_time
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def distance_to(self, target):
        return ((self.rect.centerx - target[0]) ** 2 + (self.rect.centery - target[1]) ** 2) ** 0.5