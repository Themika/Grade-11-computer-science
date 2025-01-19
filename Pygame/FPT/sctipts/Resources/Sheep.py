import pygame
import random
import math
from Resources.RawReasources.Meat import Meat
from utils.d_star import AStar

class Sheep(pygame.sprite.Sprite):
    WATER_TILES = ['Tilemap_Flat_46']
    AVOID_TILE = 40
    TILE_SIZE = 65

    def __init__(self, x, y, all_sheep, meat_group, reasources, tilemap, group_leader=None):
        super().__init__()
        self.images = [pygame.image.load(f'Animations/Reasources/Sheep/Run/HappySheep_Bouncing_{i}.png') for i in range(1, 6)]
        self.images = [pygame.transform.scale(image, (image.get_width() * 1.5, image.get_height() * 1.5)) for image in self.images]
        self.flipped_images = [pygame.transform.flip(image, True, False) for image in self.images]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_index = 0
        self.animation_time = 100  # in milliseconds
        self.last_update = pygame.time.get_ticks()
        self.idle_time = 3000  # in milliseconds
        self.last_idle = pygame.time.get_ticks()
        self.target_pos = self.get_random_position(tilemap) if group_leader is None else None
        self.direction = 1
        self.all_sheep = all_sheep
        self.meat_group = meat_group
        self.velocity = pygame.math.Vector2(0, 0)
        self.health = 1000
        self.meat_spawned = False
        self.reasources = reasources
        self.group_leader = group_leader
        self.tilemap = tilemap
        self.facing_right = False
        self.path = []

    def get_random_position(self, tilemap):
        while True:
            x = random.choice([random.randint(1500, 3000), random.randint(2500, 3000)])
            y = random.choice([random.randint(1500, 3000), random.randint(2500, 3000)])
            tile_x, tile_y = int(x // self.TILE_SIZE), int(y // self.TILE_SIZE)
            if tile_y < 0 or tile_y >= len(tilemap) or tile_x < 0 or tile_x >= len(tilemap[0]):
                continue
            tile = tilemap[tile_y][tile_x]
            if tile not in self.WATER_TILES and tile[0] != self.AVOID_TILE:
                return x, y

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.group_leader:
            self.follow_leader()
        else:
            if current_time - self.last_idle > self.idle_time:
                self.target_pos = self.get_random_position(self.tilemap)
                self.last_idle = current_time

            if not self.path or self.target_pos != self.path[-1]:
                self.path = self.find_path((self.rect.centerx, self.rect.centery), self.target_pos)

            if self.path:
                next_point = self.path[0]
                self.move_towards(next_point)
            else:
                self.target_pos = self.get_random_position(self.tilemap)
                self.velocity = pygame.math.Vector2(0, 0)

        if current_time - self.last_update > self.animation_time:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index] if self.direction == 1 else self.flipped_images[self.animation_index]
            self.last_update = current_time

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1

        self.prevent_overlap()

        if self.group_leader is None:
            pygame.draw.circle(self.image, (255, 0, 0), (self.rect.width // 2, self.rect.height // 2), self.rect.width // 2, 2)

    def follow_leader(self):
        if not self.path or self.group_leader.rect.center != self.path[-1]:
            self.path = self.find_path((self.rect.centerx, self.rect.centery), self.group_leader.rect.center)
        if self.path:
            next_point = self.path[0]
            self.move_towards(next_point)
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def prevent_overlap(self):
        for sheep in self.all_sheep:
            if sheep != self and self.rect.colliderect(sheep.rect):
                overlap_vector = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(sheep.rect.center)
                if overlap_vector.length() > 0:
                    overlap_vector = overlap_vector.normalize() * 1
                    self.rect.x += overlap_vector.x
                    self.rect.y += overlap_vector.y

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.spawn_meat()
            self.kill()

    def spawn_meat(self):
        if not self.meat_spawned:
            for _ in range(3):
                offset_x = random.randint(-30, 20)
                offset_y = random.randint(-20, 20)
                meat = Meat(self.rect.centerx + offset_x, self.rect.centery + offset_y, "Tiny_Swords_Assets/Resources/Resources/M_Idle_(NoShadow).png", 500,"meat")
                self.meat_group.add(meat)
                self.reasources.add(meat)
            self.meat_spawned = True
        self.is_destroyed = True

    def find_path(self, start, target):
        start_tile = (int(start[0] // self.TILE_SIZE), int(start[1] // self.TILE_SIZE))
        target_tile = (int(target[0] // self.TILE_SIZE), int(target[1] // self.TILE_SIZE))
        pathfinder = AStar(start_tile, target_tile, self.tilemap)
        path = pathfinder.find_path()
        if path and len(path) > 1:
            next_tile = path[1]
        else:
            next_tile = path[0] if path else start_tile
        return [(next_tile[0] * self.TILE_SIZE + self.TILE_SIZE / 2, next_tile[1] * self.TILE_SIZE + self.TILE_SIZE / 2)]

    def move_towards(self, target, tolerance=5):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > tolerance:
            dx, dy = dx / dist, dy / dist
            self.velocity = pygame.math.Vector2(dx * 2, dy * 2)
            self.rect.centerx += self.velocity.x
            self.rect.centery += self.velocity.y
            if dx > 0 and not self.facing_right:
                self.facing_right = True
                self.image = pygame.transform.flip(self.image, True, False)
            elif dx < 0 and self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.image, True, False)
            return False
        return True
