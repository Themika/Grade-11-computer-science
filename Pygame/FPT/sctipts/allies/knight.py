import pygame
import math
import random
from utils.d_star import AStar

class State:
    IDLE = 'idle'
    PATROL = 'patrol'
    RUN = 'run'
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'
    ATTACK_3 = "attack_3"
    ATTACK_4 = "attack_4"
    ATTACK_5 = "attack_5"
    SEARCH = 'search'
    WATCH = "watch"
    POS = "pos"
    DEAD = 'dead'

class Knight(pygame.sprite.Sprite):
    SEARCH_RADIUS = 200  
    WATER_TILES = ['Tilemap_Flat_46']
    AVOID_TILE = 40
    PATHFINDING_COOLDOWN = 1000

    def __init__(self, tile_map, *groups):
        super().__init__(*groups)
        self.state = State.PATROL 
        self.type = "knight"
        self.facing_right = True
        self.tilemap = tile_map
        self.current_sprite = 0
        self.sprites = self.load_sprites()
        self.image = self.sprites['idle'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2) 
        self.patrol_points = self.generate_random_patrol_points(5, 600, 2000)
        self.current_patrol_point = 0
        self.target_idle_time = 600000
        self.idle_duration_at_target = 6 
        self.on_tower = True
        self.target = None
        self.mouse_pos = None
        self.animation_timer = 0
        self.animation_speed = 750  
        self.selected = False
        self.has_reached = False
        self.state_timer = 0 
        self.idle_time = 0 
        self.speed = 2
        self.health = 200  
        self.SEARCH_DURATION = 2000
        self.last_pathfinding_time = 0
        self.path = []
        self.damage = 25

    def load_sprites(self):
        """Load all sprites for the knight."""
        def load_animation(path, count):
            return [pygame.image.load(f'{path}{i}.png') for i in range(1,count)]

        return {
            'idle': load_animation('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_', 6),
            'watch': load_animation('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_', 6),
            'run': load_animation('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_', 6),
            'patrol': load_animation('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_', 6),
            'attack_1': load_animation('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_', 6),
            'attack_2': load_animation('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_Attack_2_', 6),
            'attack_3': load_animation('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_', 6),
            'attack_4': load_animation('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_', 6),
            'attack_5': load_animation('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_', 6),
            'search': load_animation('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_', 6),
            'pos': load_animation('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_', 6),
            "dead":load_animation('Animations/Warrior/Blue/Knight/Death/Dead_',14)
        }

    def generate_random_patrol_points(self, num_points, max_x, max_y):
        """Generate a list of random patrol points within the given range, avoiding water tiles."""
        patrol_points = []
        while len(patrol_points) < num_points:
            point = (random.randint(0, max_x), random.randint(0, max_y))
            if not self.is_water_tile(point[0], point[1]):
                patrol_points.append(point)
        return patrol_points

    def move_to_click_position(self, pos):
        """Set the mouse position when clicked, only if the knight is selected and not already idle."""
        if self.selected and self.state != State.WATCH and self.state != State.POS:
            self.mouse_pos = pos
            self.state = State.POS
            self.has_reached = False

    def is_water_tile(self, x, y):
        """
        Check if the given position or two tiles ahead corresponds to a water tile or a tile to avoid.
        """
        def check_tile(x, y):
            tile_x = int(x // 65)
            tile_y = int(y // 65)
            tile = self.tilemap[tile_y][tile_x]
            return tile in self.WATER_TILES or tile[0] == self.AVOID_TILE
        self.speed = 2
        # Check the current tile
        if check_tile(x, y):
            return True

        # Check two tiles ahead in the direction of movement
        dx = self.speed if self.facing_right else -self.speed
        dy = self.speed if self.rect.centery < y else self.speed

        if check_tile(x + 2 * dx, y) or check_tile(x, y + 2 * dy) or check_tile(x + dx, y + dy):
            return True

        return False

    def movement(self, other_knights):
        """Determine what the knight should do based on its state."""
        if self.mouse_pos:
            self.state = State.POS
            target_pos = (self.mouse_pos[0] + random.randint(-50, 50), self.mouse_pos[1] + random.randint(-50,50))
            if self.move_towards_pathfinding(target_pos):
                self.mouse_pos = None
                self.state = State.WATCH
                self.watch()
        else:
            if self.state != State.WATCH:
                if self.state == State.RUN:
                    self.chase_target()
                elif self.state == State.PATROL:
                    self.patrol()
                elif self.state == State.SEARCH:
                    self.search()
                elif self.state == State.IDLE and pygame.time.get_ticks() - self.state_timer >= self.idle_time:
                    self.state = State.PATROL
                    self.state_timer = pygame.time.get_ticks()
            self.avoid_overlap(other_knights)

    def search(self):
        """Make the knight search for enemies in a small radius using detouring system."""
        if not hasattr(self, 'search_targets'):
            self.search_targets = []
            self.search_index = 0
            self.search_start_time = pygame.time.get_ticks()
            self.state = State.SEARCH
        if not self.search_targets:
            for _ in range(5):  # Generate up to 5 valid search targets
                while True:
                    dx, dy = self.SEARCH_RADIUS * math.cos(math.radians(random.uniform(0, 360))), self.SEARCH_RADIUS * math.sin(math.radians(random.uniform(0, 360)))
                    candidate_x, candidate_y = self.rect.centerx + dx, self.rect.centery + dy
                    if (0 <= candidate_x < len(self.tilemap[0]) * 65 and 0 <= candidate_y < len(self.tilemap) * 65 and not self.is_water_tile(candidate_x, candidate_y)):
                        self.search_targets.append((candidate_x, candidate_y))
                        break
            self.search_index = 0
        if pygame.time.get_ticks() - self.search_start_time >= self.SEARCH_DURATION:
            self.state = State.PATROL
            self.search_targets = []
            self.state_timer = pygame.time.get_ticks()
        elif self.search_index < len(self.search_targets):
            if self.move_towards(self.search_targets[self.search_index], tolerance=5):
                self.search_index += 1
        else:
            self.state = State.PATROL
            self.search_targets = []
            self.state_timer = pygame.time.get_ticks()

    def update(self, dt, enemies, other_knights):
        """Update knight's behavior and animations."""
        if self.state == State.DEAD:
            self.animate(dt)
            if self.current_sprite == len(self.sprites[State.DEAD]) - 1:
                self.kill()  
        else:
            self.detect_enemy(enemies)
            self.movement(other_knights)
            self.animate(dt)
            if self.target and not any(enemy.rect.center == self.target and enemy.health > 0 for enemy in enemies):
                self.target = None
                self.state = State.SEARCH
                self.state_timer = pygame.time.get_ticks()
                self.current_sprite = 0

    def animate(self, dt):
        self.animation_timer += dt * 8500  
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.current_sprite]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)
    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
    def selection(self):
        """Handle selection of the knight."""
        self.selected = True
        self.state = State.IDLE

    def deselect(self):
        """Handle deselection of the knight."""
        self.selected = False
        self.state = State.PATROL
        self.has_reached = False

    def move_to(self, target):
        self.target = target
        self.state = State.RUN  
        self.state_timer = 0  

    def move_to_potion(self, potion_position):
        """Stop current actions and move to the potion marker."""
        self.target = potion_position
        self.state = State.RUN  
        self.state_timer = 0  

    def patrol(self):
        """Patrol between predefined points using pathfinding logic."""
        if self.target:  
            return
        while not self.is_valid_patrol_point(self.patrol_points[self.current_patrol_point]):
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)
        target_point = self.patrol_points[self.current_patrol_point]
        if self.move_towards_pathfinding(target_point):
            self.state = State.IDLE
            self.idle_time = random.randint(2000, 5000)
            self.state_timer = pygame.time.get_ticks()
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def is_valid_patrol_point(self, point):
        """Check if a patrol point is valid (within map bounds and not a water tile)."""
        x, y = point
        map_width, map_height = len(self.tilemap[0]) * 65, len(self.tilemap) * 65
        return 0 <= x < map_width and 0 <= y < map_height and not self.is_water_tile(x, y)

    def chase_target(self):
        """Move toward the set target with tolerance."""
        if self.target and self.move_towards(self.target, tolerance=10):
            self.target = None 
            self.state = State.IDLE 
            self.idle_time = 600000 
            self.state_timer = pygame.time.get_ticks()  

    def move_towards(self, target, tolerance=5):
        """Move the knight towards the target position while rerouting around water tiles and tiles to avoid."""
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > tolerance:
            dx, dy = dx / dist, dy / dist
            new_x, new_y = self.rect.centerx + dx * self.speed, self.rect.centery + dy * self.speed
            if self.is_water_tile(new_x, new_y):
                detour_x, detour_y = self.find_detour((self.rect.centerx, self.rect.centery))
                if (detour_x, detour_y) == (self.rect.centerx, self.rect.centery):
                    return True
                self.rect.centerx, self.rect.centery = detour_x, detour_y
            else:
                self.rect.centerx, self.rect.centery = new_x, new_y
            self.facing_right = dx > 0
            return False
        return True
    
    def move_towards_pathfinding(self, target, tolerance=5):
        """Move the knight towards the target position using pathfinding, but avoid frequent pathfinding calculations."""
        current_time = pygame.time.get_ticks()
        if not self.path or self.path[-1] != target or current_time - self.last_pathfinding_time > self.PATHFINDING_COOLDOWN:
            start = (self.rect.centerx, self.rect.centery)
            self.path = self.find_path(start, target)
            self.last_pathfinding_time = current_time  # Update the last pathfinding time
        
        if self.path:
            return self.move_towards(self.path[0], tolerance)
        return True

    def find_detour(self, start):
        """Find a more sophisticated detour around water tiles by checking adjacent and diagonal tiles."""
        directions = [(-self.speed, 0), (self.speed, 0), (0, -self.speed), (0, self.speed), (-self.speed, -self.speed), (self.speed, -self.speed), (-self.speed, self.speed), (self.speed, self.speed)]
        for dx, dy in directions:
            detour_x, detour_y = start[0] + dx, start[1] + dy
            if not self.is_water_tile(detour_x, detour_y):
                return detour_x, detour_y
        return start
    
    def is_water_tile(self, x, y):
        """Check if the given position corresponds to a water tile or a tile to avoid."""
        tile_x, tile_y = int(x // 65), int(y // 65)
        if tile_y < 0 or tile_y >= len(self.tilemap) or tile_x < 0 or tile_x >= len(self.tilemap[0]):
            return True
        tile = self.tilemap[tile_y][tile_x]
        return tile in self.WATER_TILES or tile[0] == self.AVOID_TILE
    
    def find_path(self, start, target):
        start_tile, target_tile = (int(start[0] // 65), int(start[1] // 65)), (int(target[0] // 65), int(target[1] // 65))
        dstar = AStar(start_tile, target_tile, self.tilemap)
        path = dstar.find_path()
        if path and len(path) > 1:
            next_tile = path[1]
        else:
            next_tile = path[0] if path else start_tile
        return [(next_tile[0] * 65 + 32.5, next_tile[1] * 65 + 32.5)]
    def avoid_overlap(self, other_knights, min_distance=25):
        """Avoid overlapping with other knights."""
        if self.state in [State.ATTACK_1, State.ATTACK_2, State.ATTACK_3, State.ATTACK_4, State.ATTACK_5]:
            for knight in other_knights:
                if knight != self:
                    dx, dy = self.rect.centerx - knight.rect.centerx, self.rect.centery - knight.rect.centery
                    dist = math.hypot(dx, dy)
                    if dist < min_distance and dist != 0:
                        dx, dy = dx / dist, dy / dist  # Normalize the movement vector
                        offset = random.randint(-10, 10)  # Add random offset
                        self.rect.centerx += dx * (min_distance - dist + offset) / 2
                        self.rect.centery += dy * (min_distance - dist + offset) / 2
                        knight.rect.centerx -= dx * (min_distance - dist + offset) / 2
                        knight.rect.centery -= dy * (min_distance - dist + offset) / 2

    def detect_enemy(self, enemies):
        if self.state != State.WATCH:
            """Detect the closest alive enemy and move towards it if within range."""
            closest_enemy = None
            closest_distance = float('inf')

            for enemy in enemies:
                if enemy.health > 0:  # Only consider alive enemies
                    distance = math.hypot(enemy.rect.centerx - self.rect.centerx, enemy.rect.centery - self.rect.centery)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_enemy = enemy

            if closest_enemy and closest_distance <= 250:  # Only consider enemies within 200 pixels
                self.target = closest_enemy.rect.center
                if self.rect.colliderect(closest_enemy.rect.inflate(0.2, .2)):
                    self.handle_attack(closest_enemy, enemies)
                else:
                    self.state = State.RUN  # Move toward the enemy if not close enough

    def handle_attack(self, enemy, enemies):
        """Handle the attack logic based on the knight's position relative to the enemy."""
        if self.rect.centery < enemy.rect.centery:
            self.perform_attack(enemy, State.ATTACK_3, State.ATTACK_4)
        elif self.rect.centery > enemy.rect.centery:
            self.perform_attack(enemy, State.ATTACK_5, State.ATTACK_1)
        else:
            self.perform_attack(enemy, State.ATTACK_1, State.ATTACK_2)

        if enemy.health <= 0:
            self.target = None
            self.state = State.SEARCH
            self.state_timer = pygame.time.get_ticks()
            self.current_sprite = 0
            enemies.remove(enemy)  # Remove the enemy from the list
            enemy.kill()  # Remove the enemy from all sprite groups

    def perform_attack(self, enemy, primary_attack, secondary_attack):
        """Perform the attack sequence on the enemy."""
        if self.state == primary_attack and self.current_sprite == len(self.sprites[primary_attack]) - 1:
            self.state = secondary_attack
            self.current_sprite = 0
            enemy.take_damage(self.damage)
        elif self.state == secondary_attack and self.current_sprite == len(self.sprites[secondary_attack]) - 1:
            self.state = primary_attack
            self.current_sprite = 0
            enemy.take_damage(self.damage)
        elif self.state not in (primary_attack, secondary_attack):
            self.state = primary_attack
            self.current_sprite = 0
            enemy.take_damage(self.damage)
        
    def watch(self):
        """Stay idle at the mouse position until deselected."""
        if self.selected:
            self.state = State.WATCH
            self.image = self.sprites['idle'][self.current_sprite]
            self.has_reached = True
            self.mouse_pos = None  # Ignore mouse commands to move the knight
        else:
            self.state = State.SEARCH
            self.state_timer = pygame.time.get_ticks()

    def take_damage(self, amount):
        """Reduce health by the given amount and destroy if health is 0 or less."""
        self.health -= amount
        if self.health <= 0 and self.state != State.DEAD:
            self.state = State.DEAD
            self.current_sprite = 0
            self.animation_speed = 100  # Adjust the speed of the death animation if needed

