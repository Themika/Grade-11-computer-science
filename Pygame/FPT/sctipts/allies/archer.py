import pygame
import random
import math
from utils.projectile import Projectile
from utils.d_star import AStar

class State:
    PATROL = 'patrol'
    IDLE = 'idle'
    WATCH = 'watch'
    ATTACK = 'attack'
    DEAD = 'dead'
    SEARCH = 'search'
    POS = 'pos'

class Archer(pygame.sprite.Sprite):
    ANIMATION_SPEED = 750
    SHOOT_COOLDOWN = 1100
    IDLE_TIME_RANGE = (3000, 5000)
    SEARCH_RADIUS = 200
    SEARCH_DURATION = 20000
    PATROL_POINTS = 5
    PATROL_AREA = (2000, 2000)
    SPEED = 3
    DETECTION_RADIUS = 250
    TOLERANCE = 5
    WATER_TILES = ['Tilemap_Flat_46']
    AVOID_TILE = 40

    def __init__(self, tile_map, *groups):
        super().__init__(*groups)
        self.state = State.PATROL
        self.type = "archer"
        self.current_patrol_point = 0
        self.target_idle_time = 600000
        self.target = None
        self.idle_duration_at_target = 6
        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.animation_timer = 0
        self.image = self.sprites['idle'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2)
        self.state_timer = 0
        self.idle_time = 0
        self.facing_right = True
        self.last_shot_time = 0
        self.projectiles = pygame.sprite.Group()
        self.has_reached = False
        self.selected = False
        self.target_position = None
        self.health = 100  # Add health attribute
        self.on_tower = False  # Add flag to indicate if the archer is on a tower
        self.tilemap = tile_map
        self.patrol_points = self.generate_random_patrol_points(self.PATROL_POINTS, *self.PATROL_AREA)

    def load_sprites(self):
        idle_sprites = [
            pygame.image.load(f'Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_{i}.png') for i in range(1, 7)
        ]
        run_sprites = [
            pygame.image.load(f'Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_{i}.png').convert_alpha() for i in range(1, 7)
        ]
        attack_sprites = [
            pygame.image.load(f'Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_{i}.png').convert_alpha() for i in range(1, 9)
        ]
        return {
            'idle': idle_sprites,
            'watch': idle_sprites,
            'search': run_sprites,
            'patrol': run_sprites,
            'attack': attack_sprites,
            'pos': run_sprites
        }

    def generate_random_patrol_points(self, num_points, max_x, max_y):
        """Generate a list of random patrol points within the given range, avoiding water tiles and out-of-bounds points."""
        patrol_points = []
        while len(patrol_points) < num_points:
            point = (random.randint(0, max_x), random.randint(0, max_y))
            if self.is_valid_patrol_point(point):
                patrol_points.append(point)
        return patrol_points

    def update(self, dt, enemies):
        self.detect_enemy(enemies)
        self.movement()
        self.maintain_distance()
        self.animate(dt)
        self.projectiles.update(dt, enemies)

    def draw(self, surface, camera_offset):
        surface.blit(self.image, self.rect.move(camera_offset))
        for projectile in self.projectiles:
            projectile.draw(surface, camera_offset)

    def movement(self):
        if self.on_tower:
            self.DETECTION_RADIUS = 800
            self.SHOOT_COOLDOWN = 700
            self.health = 400  # Increase health by 300
            self.state = State.IDLE if not self.target else State.ATTACK
            if self.target:
                self.attack()
            return  
        if self.selected and self.target_position:
            self.move_towards(self.target_position)
            self.state = State.POS
            if self.rect.center == self.target_position or self.rect.colliderect(pygame.Rect(self.target_position, (25, 25))):
                if self.state != State.WATCH:
                    self.state = State.WATCH
                    self.target_position = None
                    self.has_reached = True
        else:
            if self.state == State.PATROL:
                self.patrol()
            elif self.state == State.IDLE:
                self.idleling()
            elif self.state == State.ATTACK:
                self.attack()
            elif self.state == State.SEARCH:
                self.search()
            elif self.state == State.WATCH:
                self.watch()

    def animate(self, dt):
        self.animation_timer += dt * 8500
        if self.animation_timer >= self.ANIMATION_SPEED:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.current_sprite]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def patrol(self):
        """Patrol between predefined points using pathfinding logic."""
        if self.target:  
            return

        # Ensure the current patrol point is valid
        while not self.is_valid_patrol_point(self.patrol_points[self.current_patrol_point]):
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards_pathfinding(target_point)

        # Check if the archer has reached the target point
        if self.rect.colliderect(pygame.Rect(target_point[0] - 5, target_point[1] - 5, 10, 10)):
            self.state = State.IDLE
            self.idle_time = random.randint(2000, 5000)
            self.state_timer = pygame.time.get_ticks()
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def is_valid_patrol_point(self, point):
        """Check if a patrol point is valid (within map bounds and not a water tile)."""
        x, y = point
        map_width = len(self.tilemap[0]) * 65
        map_height = len(self.tilemap) * 65

        # Check if the point is within the map bounds
        if not (0 <= x < map_width and 0 <= y < map_height):
            return False

        # Check if the point is not on a water tile
        return not self.is_water_tile(x, y)

    def idleling(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.state_timer >= self.idle_time:
            self.state = State.PATROL
        
    def search(self):
        """Make the archer search for enemies in a small radius using detouring system."""
        if not hasattr(self, 'search_targets'):
            self.search_targets = []
            self.search_index = 0
            self.search_start_time = pygame.time.get_ticks()
            self.state = State.SEARCH
        if not self.search_targets:
            self.search_targets = []
            for _ in range(5):  # Generate up to 5 valid search targets
                while True:
                    search_angle = random.uniform(0, 360)
                    dx = self.SEARCH_RADIUS * math.cos(math.radians(search_angle))
                    dy = self.SEARCH_RADIUS * math.sin(math.radians(search_angle))
                    candidate_x = self.rect.centerx + dx
                    candidate_y = self.rect.centery + dy
                    
                    # Check if the candidate point is within map constraints and not a water tile
                    if (0 <= candidate_x < len(self.tilemap[0]) * 65 and 
                        0 <= candidate_y < len(self.tilemap) * 65 and 
                        not self.is_water_tile(candidate_x, candidate_y)):
                        self.search_targets.append((candidate_x, candidate_y))
                        break
            self.search_index = 0
        if pygame.time.get_ticks() - self.search_start_time >= self.SEARCH_DURATION:
            self.state = State.PATROL
            self.search_targets = []
            self.state_timer = pygame.time.get_ticks()
        elif self.search_index < len(self.search_targets):
            self.move_towards(self.search_targets[self.search_index], tolerance=5)
            if abs(self.rect.centerx - self.search_targets[self.search_index][0]) < 5 and abs(self.rect.centery - self.search_targets[self.search_index][1]) < 5:
                self.search_index += 1
        else:
            self.state = State.PATROL
            self.search_targets = []
            self.state_timer = pygame.time.get_ticks()
    
    def move_towards(self, target, tolerance=5):
        """
        Move the archer towards the target position while rerouting around water tiles and tiles to avoid.
        """
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
    
        if dist > tolerance:
            dx, dy = dx / dist, dy / dist
            new_x = self.rect.centerx + dx * self.SPEED
            new_y = self.rect.centery + dy * self.SPEED
    
            if self.is_water_tile(new_x, new_y):
                # Reroute logic using a more sophisticated detour method
                detour_x, detour_y = self.find_detour((self.rect.centerx, self.rect.centery), (new_x, new_y))
                if (detour_x, detour_y) == (self.rect.centerx, self.rect.centery):
                    # If no valid detour found, stop moving
                    return True
                self.rect.centerx, self.rect.centery = detour_x, detour_y
            else:
                # Move normally if no water tile is in the path
                self.rect.centerx = new_x
                self.rect.centery = new_y
    
            self.facing_right = dx > 0  # Adjust the facing direction
            return False
        return True

    def move_towards_pathfinding(self, target, tolerance=5):
        """
        Move the archer towards the target position using pathfinding logic.
        """
        start = (self.rect.centerx, self.rect.centery)
        path = self.find_path(start, target)
        if path:
            next_point = path[0]
            self.move_towards(next_point, tolerance)

    def find_detour(self, start, target):
        """
        Find a more sophisticated detour around water tiles by checking adjacent and diagonal tiles.
        """
        directions = [
            (-self.SPEED, 0), (self.SPEED, 0), (0, -self.SPEED), (0, self.SPEED),  # Cardinal directions
            (-self.SPEED, -self.SPEED), (self.SPEED, -self.SPEED), (-self.SPEED, self.SPEED), (self.SPEED, self.SPEED)  # Diagonal directions
        ]
        for dx, dy in directions:
            detour_x = start[0] + dx
            detour_y = start[1] + dy
            if not self.is_water_tile(detour_x, detour_y):
                return detour_x, detour_y
        return start
    
    def is_water_tile(self, x, y):
        """
        Check if the given position corresponds to a water tile or a tile to avoid.
        """
        tile_x = int(x // 65)
        tile_y = int(y // 65)
        if tile_y < 0 or tile_y >= len(self.tilemap) or tile_x < 0 or tile_x >= len(self.tilemap[0]):
            # Out of bounds check
            return True
        tile = self.tilemap[tile_y][tile_x]
        return tile in self.WATER_TILES or tile[0] == self.AVOID_TILE
    
    def find_path(self, start, target, all_archers=None):
        start_tile = (int(start[0] // 65), int(start[1] // 65))
        target_tile = (int(target[0] // 65), int(target[1] // 65))
        dstar = AStar(start_tile, target_tile, self.tilemap)
        path = dstar.find_path()
        if path and len(path) > 1:
            next_tile = path[1]
        else:
            next_tile = path[0] if path else start_tile
        return [(next_tile[0] * 65 + 32.5, next_tile[1] * 65 + 32.5)]

    def detect_enemy(self, enemies):
        if self.state not in [State.WATCH, State.POS]:
            closest_enemy = None
            closest_distance = float('inf')
            for enemy in enemies:
                if enemy.health > 0:
                    distance = math.hypot(enemy.rect.centerx - self.rect.centerx, enemy.rect.centery - self.rect.centery)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_enemy = enemy
            if closest_enemy and closest_distance <= self.DETECTION_RADIUS:
                self.target = closest_enemy
                self.state = State.ATTACK

    def attack(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.SHOOT_COOLDOWN:
            self.shoot_projectile(self.target)
            self.last_shot_time = current_time
        if self.target and self.target.health <= 0:
            self.target.kill()
            self.target = None
            self.state = State.SEARCH
            self.state_timer = pygame.time.get_ticks()
            self.current_sprite = 0

    def shoot_projectile(self, target):
        if target:
            projectile = Projectile(self.rect.center, target.rect.center, 50, 'Tiny_Swords_Assets/Factions/Knights/Troops/Archer/Arrow/Arrow_Stand_Alone.png')
            self.projectiles.add(projectile)
            # Determine the direction of the target and set facing_right accordingly
            dx = target.rect.centerx - self.rect.centerx
            self.facing_right = dx > 0

    def selection(self):
        self.selected = True
        self.state = State.IDLE

    def deselect(self):
        self.selected = False
        if self.state == State.WATCH:
            self.state = State.PATROL

    def move_to_click_position(self, position):
        if self.state not in [State.WATCH, State.POS]:
            self.target_position = position
            self.state = State.PATROL
            self.has_reached = False

    def watch(self):
        if self.selected:
            self.state = State.WATCH
            self.image = self.sprites['idle'][self.current_sprite]
            self.has_reached = True
            self.mouse_pos = None
        else:
            self.state = State.SEARCH
            self.state_timer = pygame.time.get_ticks()

    def take_damage(self, amount):
        """Reduce health by the given amount and destroy if health is 0 or less."""
        self.health -= amount
        if self.health <= 0:
            self.state = State.DEAD
            self.kill()

    def maintain_distance(self):
        if self.on_tower == False:
            if self.target:
                distance = math.hypot(self.target.rect.centerx - self.rect.centerx, self.target.rect.centery - self.rect.centery)
                if distance < self.DETECTION_RADIUS:
                    angle = math.atan2(self.target.rect.centery - self.rect.centery, self.target.rect.centerx - self.rect.centerx)
                    target_x = self.target.rect.centerx - math.cos(angle) * self.DETECTION_RADIUS
                    target_y = self.target.rect.centery - math.sin(angle) * self.DETECTION_RADIUS
                    if not self.move_towards((target_x, target_y)):
                        self.state = State.SEARCH