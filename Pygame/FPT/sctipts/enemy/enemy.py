import random
import pygame
from utils.d_star import AStar  # Assuming AStar is in a file named astar.py

class Enemy(pygame.sprite.Sprite):
    IDLE = 'idle'
    RUN = 'run'
    SEARCH = 'search'
    ATTACK_RANGE = 5
    DAMAGE = 5
    ATTACK_COOLDOWN = 1000
    DIRECTION_CHANGE_THRESHOLD = 0.1  # Threshold to prevent rapid flipping
    TILE_SIZE = 65

    def __init__(self, tilemap, *groups):
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
        self.tilemap = tilemap
        self.path_cache = {}
        self.astar = AStar(self._tile_coords(self.rect.center), self._tile_coords(self.patrol_points[0]), tilemap)

    def update(self, knights, archers):
        if self.attacking_target and self.attacking_target.health > 0:
            self.attack_if_close([self.attacking_target], [])
        else:
            self.attacking_target = None
            self.patrol()
            self.attack_if_close(knights, archers)

        self.update_state()

    def patrol(self):
        target = self.patrol_points[self.current_patrol_point]
        if self.distance_to(target) > 1:
            self.state = self.RUN
            self.move_towards(target)
        else:
            self.state = self.IDLE
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def move_towards(self, target):
        start = self._tile_coords(self.rect.center)
        goal = self._tile_coords(target)
        path_key = (start, goal)
        if path_key not in self.path_cache:
            self.astar = AStar(start, goal, self.tilemap)
            self.path_cache[path_key] = self.astar.find_path()

        self.path = self.path_cache[path_key]

        if self.path:
            next_step = self.path.pop(0)
            target_pos = (next_step[0] * self.TILE_SIZE + self.TILE_SIZE / 2, next_step[1] * self.TILE_SIZE / 2)
            dx, dy = target_pos[0] - self.rect.centerx, target_pos[1] - self.rect.centery
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

    def distance_to(self, target):
        return self.distance_between(self.rect.center, target)

    def distance_between(self, pos1, pos2):
        dx, dy = pos1[0] - pos2[0], pos1[1] - pos2[1]
        return (dx**2 + dy**2) ** 0.5

    def _tile_coords(self, pos):
        return (pos[0] // self.TILE_SIZE, pos[1] // self.TILE_SIZE)