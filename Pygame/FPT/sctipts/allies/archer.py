import pygame
import random
import math

class State:
    PATROL = 'patrol'
    IDLE = 'idle'
    WATCH = 'watch'
    ATTACK = 'attack'
    DEAD = 'dead'

class Archer(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.PATROL  
        self.patrol_points = self.generate_random_patrol_points(5, 2000, 2000)  # Generate 5 random patrol points within a 2000x2000 area
        self.current_patrol_point = 0
        self.target_idle_time = 600000
        self.target = None
        self.idle_duration_at_target = 6 
        self.sprites = {
            'idle': [
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_6.png'),
            ],
            "watch": [
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Idle/Archer_Blue_Idle_6.png'),
            ],
            'patrol': [
                pygame.image.load('Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Run/Archer_Blue_Run_6.png'),
            ],
            "attack": [
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_6.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_7.png'),
                pygame.image.load('Animations/Warrior/Blue/Archer/Attack_1/Archer_Blue_Attack_8.png'),
            ]
        }
        self.current_sprite = 0
        self.animation_timer = 0
        self.animation_speed = 750  
        self.image = self.sprites['idle'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2) 

        self.state_timer = 0 
        self.idle_time = 0 
        self.speed = 3  

        self.facing_right = True
        self.shoot_cooldown = 1000  
        self.last_shot_time = 0

    def generate_random_patrol_points(self, num_points, max_x, max_y):
        """Generate a list of random patrol points within the given range."""
        return [(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_points)]

    def update(self, dt, enemies):
        self.detect_enemy(enemies)
        self.movement()
        self.animate(dt)

    def draw(self, surface):
        surface.blit(self.image, self.rect) 

    def movement(self):
        if self.state == State.PATROL:
            self.patrol()
        elif self.state == State.IDLE:
            current_time = pygame.time.get_ticks()
            if current_time - self.state_timer >= self.idle_time:
                self.state = State.PATROL
        elif self.state == State.ATTACK:
            self.attack()

    def animate(self, dt):
        self.animation_timer += dt * 8500  
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.current_sprite]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def patrol(self):
        """Patrol between predefined points."""
        if self.target:  
            return
        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards(target_point)

        if self.rect.center == target_point or self.rect.colliderect(pygame.Rect(target_point, (5,5))):
            self.state = State.IDLE  
            self.idle_time = random.randint(3000, 5000)  # Idle for 3-5 seconds
            self.state_timer = pygame.time.get_ticks()  
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def move_towards(self, target, tolerance=10):
        """Move the knight towards the target position with a tolerance."""
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > tolerance:  
            dx, dy = dx / dist, dy / dist  
            self.rect.centerx += dx * self.speed  
            self.rect.centery += dy * self.speed

            # Handle facing direction
            self.facing_right = dx > 0
            return False
        return True

    def avoid_overlap(self, other_knights, min_distance=50):
        """Avoid overlapping with other knights."""
        for knight in other_knights:
            if knight != self:
                dx, dy = self.rect.centerx - knight.rect.centerx, self.rect.centery - knight.rect.centery
                dist = math.hypot(dx, dy)
                if dist < min_distance:
                    dx, dy = dx / dist, dy / dist 
                    self.rect.centerx += dx * (min_distance - dist)
                    self.rect.centery += dy * (min_distance - dist)

    def detect_enemy(self, enemies):
        if self.state != State.WATCH:
            """Detect the closest alive enemy and move towards it if within range."""
            closest_enemy = None
            closest_distance = float('inf')

            for enemy in enemies:
                if enemy.health > 0:  
                    distance = math.hypot(enemy.rect.centerx - self.rect.centerx, enemy.rect.centery - self.rect.centery)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_enemy = enemy

            if closest_enemy and closest_distance <= 150:  
                self.target = closest_enemy
                self.state = State.ATTACK

    def attack(self):
        """Attack the target enemy."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            self.last_shot_time = current_time

            if self.target.health <= 0:
                print('Enemy is dead')
                if self.target is not None:
                    self.target.kill() 
                self.target = None
                self.state = State.PATROL
                self.state_timer = pygame.time.get_ticks()
                self.current_sprite = 0

    def watch(self):
        """Stay idle at the mouse position until deselected."""
        if self.selected:
            self.state = State.WATCH
            self.image = self.sprites['idle'][self.current_sprite]
            self.has_reached = True
            self.mouse_pos = None  # Ignore mouse commands to move the knight
        else:
            self.state = State.PATROL
            self.state_timer = pygame.time.get_ticks()
