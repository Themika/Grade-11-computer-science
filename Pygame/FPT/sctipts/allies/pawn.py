import pygame
import random
import time
import math
from utils.d_star import AStar

IDLE = 'idle'
RUN = 'run'
CHOPPING = 'chopping'
MOVING_TO_DROP = 'moving_to_drop'
MOVING_TO_MINE = 'moving_to_mine'
CARRYING = 'carrying'
POS = 'pos'
WATCH = 'watch'
DEATH = 'death'

TOLERANCE = 20

class Pawn(pygame.sprite.Sprite):
    ANIMATION_SPEED = 750
    SPEED = 3
    mine_pawn = None
    mine_cooldown_timer = 0
    WATER_TILES = ['Tilemap_Flat_46']
    AVOID_TILE = 40
    log_count = 0
    gold_count = 0
    def __init__(self, tile_map, *groups):
        super().__init__(*groups)
        self.state = IDLE
        self.type = "pawn"

        self.current_sprite = 0
        self.animation_timer = 0
        self.search_radius = 50
        self.health = 100

        self.target_resources = []
        self.holding_resources = []
        self.dropped_resources = []
        
        self.tilemap = tile_map
        self.sprites = self.load_sprites()
        self.image = self.sprites[self.state][self.current_sprite]
        self.rect = self.image.get_rect(center=(1280 // 2, 720 // 2))

        self.facing_right = True
        self.selected = False
        self.has_reached = False
        self.on_tower = False

        self.drop_position = None
        self.mine_start_time = None
        self.target_gold_mine = None
        self.target_tree = None 
        self.target_position = None
        self.path_cache = None

    def load_sprites(self):
        def load_images(path, count):
            return [pygame.image.load(f'{path}_{i}.png') for i in range(1, count + 1)]

        return {
            IDLE: load_images('Animations/Pawn/Idle/Pawn_Blue_Idle', 5),
            RUN: load_images('Animations/Pawn/Run/Pawn_Blue_Run', 5),
            CHOPPING: load_images('Animations/Pawn/Chopping/Pawn_Blue_Chopping', 5),
            MOVING_TO_DROP: load_images('Animations/Pawn/Carrying/Pawn_Blue_Carrying', 6),
            MOVING_TO_MINE: load_images('Animations/Pawn/Run/Pawn_Blue_Run', 5),
            CARRYING: load_images('Animations/Pawn/Carrying/Pawn_Blue_Carrying', 6),
            POS: load_images('Animations/Pawn/Run/Pawn_Blue_Run', 5),
            WATCH: load_images('Animations/Pawn/Idle/Pawn_Blue_Idle', 5),
            DEATH: load_images('Animations/Warrior/Blue/Knight/Death/Dead', 14)
        }

    def flip_sprite(self):
        self.image = pygame.transform.flip(self.image, True, False)

    def animate(self, dt):
        self.animation_timer += dt * 8500
        if self.animation_timer >= self.ANIMATION_SPEED:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.current_sprite]
            if not self.facing_right:
                self.flip_sprite()

    def update_facing_direction(self, dx):
        if dx < 0 and self.facing_right:
            self.facing_right = False
            self.flip_sprite()
        elif dx > 0 and not self.facing_right:
            self.facing_right = True
            self.flip_sprite()

    def avoid_collisions(self, pawns, dx, dy):
        for pawn in pawns:
            if pawn != self and self.rect.colliderect(pawn.rect):
                if dx > 0:
                    self.rect.right = pawn.rect.left
                elif dx < 0:
                    self.rect.left = pawn.rect.right
                if dy > 0:
                    self.rect.bottom = pawn.rect.top
                elif dy < 0:
                    self.rect.top = pawn.rect.bottom

    def find_nearest(self, sprites):
        nearest_sprite = min(
            sprites,
            key=lambda sprite: ((sprite.rect.centerx - self.rect.centerx) ** 2 + (sprite.rect.centery - self.rect.centery) ** 2) ** 0.5,
            default=None
        )
        return nearest_sprite

    def is_within_radius(self, sprite, radius):
        dx, dy = sprite.rect.centerx - self.rect.centerx, sprite.rect.centery - self.rect.centery
        return abs(dx) <= radius and abs(dy) <= radius

    def chase_sheep(self, sheep,counts):
        if self.holding_resources:
            self.drop_resources(counts)
        self.state = RUN
        target_position = pygame.math.Vector2(sheep.rect.center)
        self.move_towards_pathfinding(target_position)
        if abs(self.rect.centerx - target_position.x) <= 10 and abs(self.rect.centery - target_position.y) <= 10:
            self.attack_sheep(sheep)

    def attack_sheep(self, sheep):
        self.state = CHOPPING
        sheep.take_damage(10)

    def update(self, dt, trees, targeted_trees, resources, gold_mines, pawns, sheep_sprites, castle_position, counts):
        current_time = time.time()
        nearest_sheep = self.find_nearest(sheep_sprites)
        if self.health <= 0:
            self.state = DEATH
            self.animate(dt)
            if self.current_sprite == len(self.sprites[DEATH]) - 1:
                self.kill()
            return
        if nearest_sheep and self.is_within_radius(nearest_sheep, 50) and not self.selected:
            self.chase_sheep(nearest_sheep,counts)
        else:
            if self.selected and self.target_position:
                if self.move_towards_pathfinding(self.target_position):
                    self.state = WATCH
                    self.target_position = None
                    self.has_reached = True
                    for tree in trees:
                        if abs(self.rect.centerx - tree.rect.centerx) <= 5 and abs(self.rect.centery - tree.rect.centery) <= 5:
                            self.target_tree = tree
                            self.state = RUN
                            break
                else:
                    if len(self.holding_resources) > 0:
                        self.state = CARRYING
                    else:
                        self.state = POS
            else:
                if self.state == WATCH or self.state == IDLE:
                    for tree in trees:
                        if abs(self.rect.centerx - tree.rect.centerx) <= 5 and abs(self.rect.centery - tree.rect.centery) <= 5:
                            self.target_tree = tree
                            self.state = CHOPPING
                            break
                if self.state == MOVING_TO_DROP:
                    self.move_towards_drop_position(dt, counts)
                elif self.state == MOVING_TO_MINE:
                    self.handle_mining(current_time)
                else:
                    self.handle_idle_state(dt, trees, targeted_trees, resources, gold_mines, current_time, castle_position)
        self.animate(dt)

        if Pawn.mine_pawn is None and current_time - Pawn.mine_cooldown_timer >= 30 and gold_mines:
            nearest_pawn = self.find_nearest(pawns)
            if nearest_pawn:
                Pawn.mine_pawn = nearest_pawn
                nearest_pawn.target_gold_mine = gold_mines.sprites()[0]
                nearest_pawn.state = RUN
        elif self == Pawn.mine_pawn and self.mine_start_time is not None and current_time - self.mine_start_time >= 30:
            Pawn.mine_pawn = None
            Pawn.mine_cooldown_timer = current_time
            self.state = IDLE

        counts[0] = Pawn.log_count
        counts[1] = Pawn.gold_count
    
    def move_towards_pathfinding(self, target, tolerance=5):
        start = (self.rect.centerx, self.rect.centery)
        target_tile = (int(target[0] // 65), int(target[1] // 65))
        
        # Check if the target has changed significantly
        if not self.path_cache or self.path_cache[-1] != target_tile:
            self.path_cache = self.find_path(start, target)
        
        if self.path_cache:
            next_point = self.path_cache[0]
            if self.move_towards_with_separation(next_point, tolerance):
                self.path_cache.pop(0)


    def move_towards_with_separation(self, target, tolerance=5):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)

        if dist > tolerance:
            dx, dy = dx / dist, dy / dist
            separation_vector = self.calculate_separation_vector()
            new_x = self.rect.centerx + (dx + separation_vector[0]) * self.SPEED
            new_y = self.rect.centery + (dy + separation_vector[1]) * self.SPEED

            if self.is_water_tile(new_x, new_y):
                detour_x, detour_y = self.find_detour((self.rect.centerx, self.rect.centery))
                if (detour_x, detour_y) == (self.rect.centerx, self.rect.centery):
                    return True
                self.rect.centerx, self.rect.centery = detour_x, detour_y
            else:
                self.rect.centerx = new_x
                self.rect.centery = new_y

            if (dx > 0 and not self.facing_right) or (dx < 0 and self.facing_right):
                self.facing_right = dx > 0
                self.flip_sprite()
            return False
        return True

    def calculate_separation_vector(self):
        separation_distance = 30
        separation_vector = pygame.math.Vector2(0, 0)
        for pawn in self.groups()[0]:
            if pawn != self:
                distance = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(pawn.rect.center)
                if 0 < distance.length() < separation_distance:
                    separation_vector += distance.normalize() / distance.length()
        return separation_vector

    def find_detour(self, start):
        directions = [
            (-self.SPEED, 0), (self.SPEED, 0), (0, -self.SPEED), (0, self.SPEED),
            (-self.SPEED, -self.SPEED), (self.SPEED, -self.SPEED), (-self.SPEED, self.SPEED), (self.SPEED, self.SPEED)
        ]
        for dx, dy in directions:
            detour_x = start[0] + dx
            detour_y = start[1] + dy
            if not self.is_water_tile(detour_x, detour_y):
                return detour_x, detour_y
        return start
    
    def is_water_tile(self, x, y):
        tile_x = int(x // 65)
        tile_y = int(y // 65)
        if tile_y < 0 or tile_y >= len(self.tilemap) or tile_x < 0 or tile_x >= len(self.tilemap[0]):
            return True
        tile = self.tilemap[tile_y][tile_x]
        return tile in self.WATER_TILES or tile[0] == self.AVOID_TILE
    
    def find_path(self, start, target):
        start_tile = (int(start[0] // 65), int(start[1] // 65))
        target_tile = (int(target[0] // 65), int(target[1] // 65))
        dstar = AStar(start_tile, target_tile, self.tilemap)
        path = dstar.find_path()
        if path and len(path) > 1:
            next_tile = path[1]
        else:
            next_tile = path[0] if path else start_tile
        return [(next_tile[0] * 65 + 32.5, next_tile[1] * 65 + 32.5)]

    def handle_mining(self, current_time):
        if self.mine_start_time is not None and current_time - self.mine_start_time >= 2:
            if hasattr(self.target_gold_mine, 'spawn_gold'):
                self.target_gold_mine.active()
                self.target_gold_mine.spawn_gold()
            self.state = IDLE
            self.target_gold_mine = None

    def handle_idle_state(self, dt, trees, targeted_trees, resources, gold_mines, current_time,castle_position):
        if self.state != WATCH:
            if self == Pawn.mine_pawn and self.target_gold_mine is not None:
                self.move_towards_mine(self.target_gold_mine)
            else:
                if self.state == CHOPPING and len(resources) <= 9:
                    self.chop_tree(resources)
                if self.state == IDLE:
                    self.search_for_resources(resources)
                    if not self.target_resources and len(resources) <= 9:
                        self.search_for_trees(trees, targeted_trees, resources)
                if self.holding_resources:
                    if self.state != MOVING_TO_DROP:
                        self.move_to_castle(castle_position)
                    self.update_held_resources_position()
                elif self.target_resources:
                    self.move_towards_resource(dt,castle_position)
                elif self.target_tree:
                    if len(resources) <= 9:
                        self.move_towards_tree()
                    else:
                        self.target_tree = None
                        self.state = IDLE
                else:
                    self.target_tree = self.get_nearest_tree(trees, targeted_trees)
                    if self.target_tree and len(resources) <= 9:
                        targeted_trees.add(self.target_tree)

            if Pawn.mine_pawn is None and current_time - Pawn.mine_cooldown_timer >= 30 and gold_mines:
                Pawn.mine_pawn = self
                self.target_gold_mine = gold_mines.sprites()[0]
                self.state = RUN
            elif self == Pawn.mine_pawn and self.mine_start_time is not None and current_time - self.mine_start_time >= 30:
                Pawn.mine_pawn = None
                Pawn.mine_cooldown_timer = current_time
                self.state = IDLE

    def search_for_trees(self, trees, targeted_trees, resources):
        if len(resources) > 9:
            self.target_resources = sorted(resources, key=lambda resource: ((resource.rect.centerx - self.rect.centerx) ** 2 + (resource.rect.centery - self.rect.centery) ** 2) ** 0.5)[:3]
            self.state = RUN
            return
        for tree in trees:
            if tree not in targeted_trees and self.rect.colliderect(tree.rect.inflate(50, 50)):
                self.target_tree = tree
                self.state = RUN
                targeted_trees.add(tree)
                break

    def chop_tree(self, resources):
        if self.target_tree:
            self.update_facing_direction(self.target_tree.rect.centerx - self.rect.centerx)
            self.target_tree.take_damage(2)
            if self.target_tree.health <= 0:
                self.target_tree = None
                new_resources = self.get_nearest_resources(resources)
                self.target_resources.extend(new_resources)
                self.state = RUN if self.target_resources else IDLE

    def get_nearest_tree(self, trees, targeted_trees):
        nearest_tree = min(
            (tree for tree in trees if tree not in targeted_trees),
            key=lambda tree: ((tree.rect.centerx - self.rect.centerx) ** 2 + (tree.rect.centery - self.rect.centery) ** 2) ** 0.5,
            default=None
        )
        return nearest_tree

    def get_nearest_resources(self, resources):
        return sorted(resources, key=lambda resource: ((resource.rect.centerx - self.rect.centerx) ** 2 + (resource.rect.centery - self.rect.centery) ** 2) ** 0.5)[:3]

    def move_towards_tree(self):
        if self.target_tree:
            self.state = RUN
            target_position = pygame.math.Vector2(self.target_tree.rect.left - self.rect.width // 6 + 15, self.target_tree.rect.centery + self.target_tree.rect.height // 4)
            self.move_towards_pathfinding(target_position, tolerance=10)
            if abs(self.rect.centerx - target_position.x) <= 45 and abs(self.rect.centery - target_position.y) <= 45:
                self.state = CHOPPING

    def move_towards_resource(self, dt,castle_position):
        if self.target_resources and len(self.holding_resources) < 3:
            self.state = RUN
            target_resource = self.target_resources[0]
            target_position = pygame.math.Vector2(target_resource.rect.center)
            self.move_towards_position(target_position, dt)
            if self.rect.center == target_position:
                self.pick_up_resource(target_resource)
                if len(self.holding_resources) >= 2 or not self.target_resources:
                    self.state = MOVING_TO_DROP
                    self.move_to_castle(castle_position)


    def move_towards_mine(self, mine_sprite):
        self.state = RUN 
        target_position = pygame.math.Vector2(mine_sprite.rect.center)
        self.move_towards_pathfinding(target_position)
        if abs(self.rect.centerx - target_position.x) <= 10 and abs(self.rect.centery - target_position.y) <= 10:
            self.state = MOVING_TO_MINE
            self.mine_start_time = time.time()

    def pick_up_resource(self, resource):
        resource.rect.midbottom = (self.rect.midtop[0], self.rect.midtop[1] - 150)
        self.holding_resources.append(resource)
        self.target_resources.pop(0)
        if not self.target_resources or len(self.holding_resources) >= 2:
            self.state = MOVING_TO_DROP
        if self.holding_resources:
            self.state = CARRYING

    def search_for_resources(self, resources):
        if len(self.holding_resources) < 3:
            nearby_resources = [resource for resource in resources if self.rect.colliderect(resource.rect.inflate(self.search_radius, self.search_radius)) and resource not in self.dropped_resources]
            if nearby_resources:
                nearby_resources.sort(key=lambda resource: ((resource.rect.centerx - self.rect.centerx) ** 2 + (resource.rect.centery - self.rect.centery) ** 2) ** 0.5)
                self.target_resources = nearby_resources[:3]
                self.state = RUN
                self.search_radius = 50
            else:
                self.search_radius += 50
        elif len(resources) > 5:
            self.target_resources = sorted(resources, key=lambda resource: ((resource.rect.centerx - self.rect.centerx) ** 2 + (resource.rect.centery - self.rect.centery) ** 2) ** 0.5)[:3]
            self.state = RUN

    def move_to_castle(self, castle_position):
        self.drop_position = castle_position
        self.state = MOVING_TO_DROP

    def move_towards_drop_position(self, dt, counts):
        if self.drop_position:
            target_position = pygame.math.Vector2(self.drop_position)
            self.move_towards_position(target_position, dt)
            if self.rect.center == target_position:
                self.drop_resources(counts)
        self.update_held_resources_position()
    def move_towards_position(self, target_position, dt):
        direction = target_position - pygame.math.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize() * 100 * dt
            self.rect.move_ip(direction)
            self.update_facing_direction(direction.x)

    def update_held_resources_position(self):
        for i, resource in enumerate(self.holding_resources):
            resource.rect.midbottom = (self.rect.midtop[0], self.rect.midtop[1] - i * 10)

    def drop_resources(self,counts):
        for resource in self.holding_resources:
            if resource.type == 'log':
                Pawn.log_count += 1
                counts[0] = Pawn.log_count
            if resource.type == "gold":
                Pawn.gold_count += 1
                counts[1] = Pawn.gold_count
            if resource.type == "meat":
                print("MEAT")
            resource.kill()
        self.holding_resources.clear()
        self.state = IDLE

    def draw(self, screen):
        for resource in self.holding_resources:
            screen.blit(resource.image, resource.rect.topleft)

    def selection(self):
        self.selected = True

    def deselect(self):
        self.selected = False
        self.state = IDLE

    def move_to_click_position(self, position):
        self.target_position = position
        self.state = POS  
        self.has_reached = False