import random
import pygame
from enemy.enemy import Enemy  # Assuming Enemy class is in the enemy module

class Torch(Enemy):
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'
    ATTACK_3 = 'attack_3'
    RUN = 'run'
    IDLE = 'idle'
    SEARCH = 'search'
    ANIMATION_INTERVAL = 100

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
        self.state = self.RUN
        self.facing_right = True

        self.animations = {
            self.ATTACK_1: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Attack_1/Torch_Blue_Attack_1_{i}.png') for i in range(1, 6)],
            self.ATTACK_2: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Attack_2/Torch_Blue_Attack_2_{i}.png') for i in range(1, 6)],
            self.ATTACK_3: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Attack_3/Torch_Blue_Attack_3_{i}.png') for i in range(1, 6)],
            self.RUN: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Run/Torch_Blue_Run_{i}.png') for i in range(1, 6)],
            self.IDLE: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Idle/Torch_Blue_Idle_{i}.png') for i in range(1, 6)],
            self.SEARCH: [pygame.image.load(f'Animations/Goblins/Torch/Blue/Run/Torch_Blue_Run_{i}.png') for i in range(1, 6)]
        }
        self.current_frame = 0
        self.animation_time = 0

    def _get_random_position(self):
        """Generate a random position within the 2000x2000 map."""
        return random.randint(0, 2000), random.randint(0, 2000)

    def update(self, knights, archers):
        super().update(knights, archers)
        self.update_animation()

        
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

    def update_state(self):
        if self.attacking_target:
            if self.rect.centery > self.attacking_target.rect.centery:
                self.state = self.ATTACK_2
            elif self.rect.centery < self.attacking_target.rect.centery:
                self.state = self.ATTACK_3
            else:
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