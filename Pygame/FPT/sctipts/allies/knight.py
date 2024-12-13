import pygame
import math
import random


#TODO
# Play test 
# Add ARcher
class State:
    IDLE = 'idle'
    PATROL = 'patrol'
    RUN = 'run'
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'
    ATTACK_3 = "attack_3"
    ATTACK_4 = "attack_4"
    ATTACK_5 = "attack_5"
    SEARCH = 'search'  # New search state
    WATCH = "watch"
    POS = "pos"
    DEAD = 'dead'

class Knight(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.PATROL 
        self.type = "knight"
        self.patrol_points = self.generate_random_patrol_points(5, 2000, 2000)  # Generate 5 random patrol points within a 2000x2000 area
        self.current_patrol_point = 0
        self.target_idle_time = 600000
        self.idle_duration_at_target = 6 
        self.sprites = {
            'idle': [
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_5.png')
            ],
            "watch" : [
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Idle/Warrior_Blue_Idle_5.png')
            ],
            'run': [
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_6.png')
            ],
            'patrol': [
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_6.png')
            ],
            "attack_1": [
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_1/Warrior_Blue_Attack_1_6.png'),
            ],
            "attack_2": [
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_attack_2_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_Attack_2_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_Attack_2_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_Attack_2_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_Attack_2_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_2/Warrior_Blue_Attack_2_6.png'),
            ],
            "attack_3":[
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_3/Warrior_Blue_Attack_3_6.png')
            ],
            "attack_4":[
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_4/Warrior_Blue_Attack_4_6.png')
            ],
            "attack_5":[
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Attack_5/Warrior_Blue_Attack_5_6.png')
            ],
            'search': [  # New search animation
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_6.png')
            ],
            "pos":[
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Knight/Blue_Run/Warrior_Blue_Run_6.png')
            ]
        }
        self.target = None
        self.mouse_pos = None
        self.current_sprite = 0
        self.animation_timer = 0
        self.animation_speed = 750  
        self.facing_right = True
        self.selected = False
        self.has_reached = False

        self.image = self.sprites['idle'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2) 

        self.state_timer = 0 
        self.idle_time = 0 
        self.speed = 2
        self.health = 200  

    def generate_random_patrol_points(self, num_points, max_x, max_y):
        """Generate a list of random patrol points within the given range."""
        return [(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_points)]
    def move_to_click_position(self, pos):
        """Set the mouse position when clicked, only if the knight is selected and not already idle."""
        if self.selected and self.state != State.WATCH and self.state != State.POS:
            self.mouse_pos = pos
            self.state = State.POS
            self.has_reached = False


    def movement(self,other_knights):
        """Determine what the knight should do based on its state."""
        if self.mouse_pos:
            self.state = State.POS  # Ensure the state is RUN when there's a target
            if self.move_towards_pos(self.mouse_pos):  # Continue moving toward the mouse position
                self.mouse_pos = None  # Clear the mouse position when the target is reached
                self.watch()  # Call the watch method instead of setting the state to IDLE
                return  # Exit the function to prevent further action
        else:
            if self.state != State.WATCH:    # Normal behavior when not selected
                if self.state == State.RUN:
                    self.chase_target()
                elif self.state == State.PATROL:
                    self.patrol()
                elif self.state == State.SEARCH:
                    self.search()
                elif self.state == State.IDLE:
                    if pygame.time.get_ticks() - self.state_timer >= self.idle_time:
                        self.state = State.PATROL
                        self.state_timer = pygame.time.get_ticks()
            self.avoid_overlap(other_knights)





    def search(self):
        """Make the knight search for enemies in a small radius."""
        if not hasattr(self, 'search_targets'):
            self.search_targets = []
            self.search_index = 0
            self.search_start_time = pygame.time.get_ticks()  # Track the start time of the search
            self.state = State.SEARCH
    
        if not self.search_targets:
            search_radius = 200  # Set the search radius to 200 pixels
            self.search_targets = []
            for _ in range(5):  # Generate 5 random search targets
                search_angle = random.uniform(0, 360)  # Random angle for wandering direction
                dx = search_radius * math.cos(math.radians(search_angle))
                dy = search_radius * math.sin(math.radians(search_angle))
                self.search_targets.append((self.rect.centerx + dx, self.rect.centery + dy))
            self.search_index = 0
    
        if pygame.time.get_ticks() - self.search_start_time >= 20000:  # Check if 20 seconds have passed
            self.state = State.PATROL
            self.search_targets = []
            self.state_timer = pygame.time.get_ticks()
        elif self.search_index < len(self.search_targets):
            self.move_towards(self.search_targets[self.search_index], tolerance=5)
            if abs(self.rect.centerx - self.search_targets[self.search_index][0]) < 5 and abs(self.rect.centery - self.search_targets[self.search_index][1]) < 5:
                self.search_index += 1
        else:
            # After searching all 5 spots, switch back to patrol
            self.state = State.PATROL
            self.search_targets = []
            self.state_timer = pygame.time.get_ticks()
        

    def update(self, dt, enemies,other_knights):
        """Update knight's behavior and animations."""
        self.detect_enemy(enemies)
        self.movement(other_knights)
        self.animate(dt)
        # Check if the target enemy is dead and transition to SEARCH state
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

    def selection(self):
        """Handle selection of the knight."""
        self.selected = True
        self.state = State.IDLE
        print("Knight selected")

    def deselect(self):
        """Handle deselection of the knight."""
        self.selected = False
        self.state = State.PATROL
        self.has_reached = False
        print("Knight deselected")

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
        """Patrol between predefined points."""
        if self.target:  
            return

        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards(target_point)

        if self.rect.center == target_point or self.rect.colliderect(pygame.Rect(target_point, (10,10))):
            self.state = State.IDLE  
            self.idle_time = random.randint(2000, 5000)  
            self.state_timer = pygame.time.get_ticks()  #
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def chase_target(self):
        """Move toward the set target with tolerance."""
        if self.target:
            reached_target = self.move_towards(self.target, tolerance=10)  # Adjust tolerance as needed
            if reached_target:
                self.target = None 
                self.state = State.IDLE 
                self.idle_time = 600000 
                self.state_timer = pygame.time.get_ticks()  
                

    def move_towards(self, target, tolerance=10):
        """Move the knight towards the target position with a tolerance."""
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist > tolerance:  # Only move if the distance is greater than tolerance
            dx, dy = dx / dist, dy / dist  # Normalize the movement vector
            self.rect.centerx += dx * self.speed  
            self.rect.centery += dy * self.speed

            # Handle facing direction
            self.facing_right = dx > 0
            return False
        return True

    def move_towards_pos(self, target, tolerance=10, random_offset=50):
        """Move the knight towards the target position with a tolerance and random offset."""
        # Add random offset to the target position
        target = (target[0] + random.randint(-random_offset, random_offset), 
                target[1] + random.randint(-random_offset, random_offset))
        
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = math.hypot(dx, dy)
        self.speed = 3
        if dist > tolerance:  # Only move if the distance is greater than tolerance
            dx, dy = dx / dist, dy / dist  # Normalize the movement vector
            self.rect.centerx += dx * self.speed  
            self.rect.centery += dy * self.speed

            # Handle facing direction
            self.facing_right = dx > 0
            return False
        self.speed = 2
        return True

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
        if not self.mouse_pos or (self.selected and self.rect.center == self.mouse_pos) or self.state != State.POS:
            if self.state == primary_attack and self.current_sprite == len(self.sprites[primary_attack]) - 1:
                self.state = secondary_attack
                self.current_sprite = 0
                enemy.take_damage(10)
            elif self.state == secondary_attack and self.current_sprite == len(self.sprites[secondary_attack]) - 1:
                self.state = primary_attack
                self.current_sprite = 0
                enemy.take_damage(10)
            elif self.state not in (primary_attack, secondary_attack):
                self.state = primary_attack
                self.current_sprite = 0
                enemy.take_damage(10)
        
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
        if self.health <= 0:
            self.state = State.DEAD
            self.kill()