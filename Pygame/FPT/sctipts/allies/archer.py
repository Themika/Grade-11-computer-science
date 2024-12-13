import pygame
import random
import math
from utils.projectile import Projectile

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
    DETECTION_RADIUS = 150
    TOLERANCE = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.PATROL
        self.type = "archer"
        self.previous_state = self.state
        self.patrol_points = self.generate_random_patrol_points(self.PATROL_POINTS, *self.PATROL_AREA)
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

    def load_sprites(self):
        idle_sprites = [
            pygame.image.load(f'Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_{i}.png') for i in range(1, 7)
        ]
        run_sprites = [
            pygame.image.load(f'Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_{i}.png') for i in range(1, 7)
        ]
        attack_sprites = [
            pygame.image.load(f'Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_{i}.png') for i in range(1, 9)
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
        return [(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_points)]

    def update(self, dt, enemies):
        print(self.state)
        self.detect_enemy(enemies)
        self.movement()
        self.animate(dt)
        self.projectiles.update(dt, enemies)

    def draw(self, surface, camera_offset):
        surface.blit(self.image, self.rect.move(camera_offset))
        for projectile in self.projectiles:
            projectile.draw(surface, camera_offset)

    def movement(self):
        if self.selected and self.target_position:
            self.move_towards(self.target_position)
            self.state = State.POS
            if self.rect.center == self.target_position or self.rect.colliderect(pygame.Rect(self.target_position, (55, 55))):
                if self.state != State.WATCH:
                    self.state = State.WATCH
                    self.target_position = None
                    self.has_reached = True
        else:
            if self.state == State.PATROL:
                self.patrol()
            elif self.state == State.IDLE:
                self.idle()
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
        if self.target:
            return
        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards(target_point)
        if self.rect.center == target_point or self.rect.colliderect(pygame.Rect(target_point, (5, 5))):
            self.state = State.IDLE
            self.idle_time = random.randint(*self.IDLE_TIME_RANGE)
            self.state_timer = pygame.time.get_ticks()
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def idle(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.state_timer >= self.idle_time:
            self.state = State.PATROL

    def search(self):
        if not hasattr(self, 'search_targets'):
            self.search_targets = []
            self.search_index = 0
            self.search_start_time = pygame.time.get_ticks()
            self.state = State.SEARCH

        if not self.search_targets:
            self.search_targets = [
                (self.rect.centerx + self.SEARCH_RADIUS * math.cos(math.radians(random.uniform(0, 360))),
                 self.rect.centery + self.SEARCH_RADIUS * math.sin(math.radians(random.uniform(0, 360))))
                for _ in range(5)
            ]
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

    def move_towards(self, target, tolerance=TOLERANCE):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > tolerance:
            dx, dy = dx / dist, dy / dist
            self.rect.centerx += dx * self.SPEED
            self.rect.centery += dy * self.SPEED
            self.facing_right = dx > 0
            return False
        return True

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
            self.state = State.PATROL
        if self.target and self.target.health <= 0:
            self.target.kill()
            self.target = None
            self.state = State.SEARCH
            self.state_timer = pygame.time.get_ticks()
            self.current_sprite = 0

    def shoot_projectile(self, target):
        if target:
            projectile = Projectile(self.rect.center, target.rect.center, 10, 'Tiny_Swords_Assets/Factions/Knights/Troops/Archer/Arrow/Arrow_Stand_Alone.png')
            self.projectiles.add(projectile)

    def selection(self):
        self.selected = True
        self.state = State.IDLE
        print(f"Archer at {self.rect.center} selected")

    def deselect(self):
        self.selected = False
        print(f"Archer at {self.rect.center} deselected")

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
