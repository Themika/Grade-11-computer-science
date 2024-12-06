import pygame
import random

class State:
    IDLE = 'idle'
    PATROL = 'patrol'
    RUN = 'run'
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'
    ATTACK_3 = "attack_3"
    ATTACK_4 = "attack_4"
    ATTACK_5 = "attack_5"

class Knight(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.PATROL 
        self.patrol_points = [(100, 100), (1000, 100), (100, 600)] 
        self.current_patrol_point = 0
        self.target_idle_time = 600000
        self.idle_duration_at_target = 6 
        self.sprites = {
            'idle': [
                pygame.image.load('Animations/Warrior/Blue/Blue_Idle/Warrior_Blue_Idle.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Idle/Warrior_Blue_Idle_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Idle/Warrior_Blue_Idle_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Idle/Warrior_Blue_Idle_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Idle/Warrior_Blue_Idle_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Idle/Warrior_Blue_Idle_5.png')
            ],
            'run': [
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_6.png')
            ],
            'patrol': [
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Run/Warrior_Blue_Run_6.png')
            ],
            "attack_1": [
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_1/Warrior_Blue_Attack_1_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_1/Warrior_Blue_Attack_1_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_1/Warrior_Blue_Attack_1_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_1/Warrior_Blue_Attack_1_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_1/Warrior_Blue_Attack_1_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_1/Warrior_Blue_Attack_1_6.png'),
            ],
            "attack_2": [
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_2/Warrior_Blue_attack_2_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_2/Warrior_Blue_Attack_2_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_2/Warrior_Blue_Attack_2_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_2/Warrior_Blue_Attack_2_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_2/Warrior_Blue_Attack_2_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_2/Warrior_Blue_Attack_2_6.png'),
            ],
            "attack_3":[
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_3/Warrior_Blue_Attack_3_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_3/Warrior_Blue_Attack_3_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_3/Warrior_Blue_Attack_3_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_3/Warrior_Blue_Attack_3_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_3/Warrior_Blue_Attack_3_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_3/Warrior_Blue_Attack_3_6.png')
            ],
            "attack_4":[
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_4/Warrior_Blue_Attack_4_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_4/Warrior_Blue_Attack_4_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_4/Warrior_Blue_Attack_4_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_4/Warrior_Blue_Attack_4_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_4/Warrior_Blue_Attack_4_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_4/Warrior_Blue_Attack_4_6.png')
            ],
            "attack_5":[
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_5/Warrior_Blue_Attack_5_1.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_5/Warrior_Blue_Attack_5_2.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_5/Warrior_Blue_Attack_5_3.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_5/Warrior_Blue_Attack_5_4.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_5/Warrior_Blue_Attack_5_5.png'),
                pygame.image.load('Animations/Warrior/Blue/Blue_Attack_5/Warrior_Blue_Attack_5_6.png')
            ]
        }
        self.target = None
        self.current_sprite = 0
        self.animation_timer = 0
        self.animation_speed = 750  
        self.facing_right = True
        self.selected = False

        self.image = self.sprites['idle'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2) 

        self.state_timer = 0 
        self.idle_time = 0 
    
    def movement(self):
        """Determine what the knight should do based on its state."""
        if self.state == State.RUN:
            self.chase_target()
        elif self.state == State.PATROL:
            self.patrol()
        elif self.state == State.IDLE:
            if pygame.time.get_ticks() - self.state_timer >= self.idle_time:
                self.state = State.PATROL 
                print("Idle time over. Resuming patrol.")
                self.state_timer = pygame.time.get_ticks()  

    def draw(self, surface):
        if self.selected:
            pygame.draw.rect(surface, (255, 0, 0), self.rect.inflate(10, 10), 2) 
        surface.blit(self.image, self.rect)

    def update(self, dt, enemies):
        """Update knight's behavior and animations."""
        self.detect_enemy(enemies)
        self.movement()
        self.animate(dt)

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
        print(f"Knight is moving towards potion: {potion_position}")

    def patrol(self):
        """Patrol between predefined points."""
        if self.target:  
            return

        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards(target_point)

        if self.rect.center == target_point:
            self.state = State.IDLE  
            self.idle_time = random.randint(2000, 5000)  
            self.state_timer = pygame.time.get_ticks()  #
            print(f"Knight reached patrol point {target_point}. Idling for {self.idle_time / 1000:.1f} seconds.")
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
                print("Knight reached the target. Staying idle for 60 seconds.")

    def move_towards(self, target, tolerance=10):
        """Move the knight towards the target position with a tolerance."""
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * 2
        self.rect.y += dy * 2

        if dx > 0 and not self.facing_right:
            self.facing_right = True
        elif dx < 0 and self.facing_right:
            self.facing_right = False

        if abs(dx * dist) < tolerance and abs(dy * dist) < tolerance:
            return True
        return False

    def detect_enemy(self, enemies):
        """Detect enemies and move towards them if within range."""
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect.inflate(100, 100)):  
                self.target = enemy.rect.center
                if self.rect.colliderect(enemy.rect.inflate(5, 5)): 
                    if self.rect.centery < enemy.rect.centery:
                        if self.state == State.ATTACK_3 and self.current_sprite == len(self.sprites[State.ATTACK_3]) - 1:
                            self.state = State.ATTACK_4
                            self.current_sprite = 0
                            enemy.take_damage(10)
                        elif self.state == State.ATTACK_4 and self.current_sprite == len(self.sprites[State.ATTACK_4]) - 1:
                            self.state = State.ATTACK_3
                            self.current_sprite = 0
                            enemy.take_damage(10)
                        elif self.state != State.ATTACK_3 and self.state != State.ATTACK_4:
                            self.state = State.ATTACK_3
                            self.current_sprite = 0
                            enemy.take_damage(10)
                    elif self.rect.centery > enemy.rect.centery:
                        if self.state == State.ATTACK_5 and self.current_sprite == len(self.sprites[State.ATTACK_5]) - 1:
                            self.state = State.ATTACK_5
                            self.current_sprite = 0
                            enemy.take_damage(10)
                        elif self.state == State.ATTACK_1 and self.current_sprite == len(self.sprites[State.ATTACK_1]) - 1:
                            self.state = State.ATTACK_5
                            self.current_sprite = 0
                            enemy.take_damage(10)
                        elif self.state != State.ATTACK_5 and self.state != State.ATTACK_1:
                            self.state = State.ATTACK_5
                            self.current_sprite = 0
                            enemy.take_damage(10)
                    else:
                        if self.state == State.ATTACK_1 and self.current_sprite == len(self.sprites[State.ATTACK_1]) - 1:
                            self.state = State.ATTACK_2
                            self.current_sprite = 0
                            enemy.take_damage(10)
                        elif self.state == State.ATTACK_2 and self.current_sprite == len(self.sprites[State.ATTACK_2]) - 1:
                            self.state = State.ATTACK_1
                            self.current_sprite = 0
                            enemy.take_damage(10)
                        elif self.state != State.ATTACK_1 and self.state != State.ATTACK_2:
                            self.state = State.ATTACK_1
                            self.current_sprite = 0
                            enemy.take_damage(10)
                    print(f"Enemy detected. Attacking with {self.state}.")
                else:
                    self.state = State.RUN  
                    print("Enemy detected. Moving closer to attack.")
                break