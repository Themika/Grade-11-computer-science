import pygame
import random

class State:
    IDLE = 'idle'
    PATROL = 'patrol'
    RUN = 'run'

class Knight(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.PATROL  # Set initial state to PATROL
        self.patrol_points = [(100, 100), (1000, 100), (100, 600)]  # Define patrol points
        self.current_patrol_point = 0
        self.target_idle_time = 600
        self.idle_duration_at_target = 6  # Not used for patrol but for target
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
            ]
        }
        self.target = None
        self.current_sprite = 0
        self.animation_timer = 0
        self.animation_speed = 750  # milliseconds
        self.facing_right = True
        self.selected = False

        self.image = self.sprites['idle'][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2)  # Center of the screen

        self.state_timer = 0  # Track state duration in ms
        self.idle_time = 0  # Duration for idle between patrol points
    
    def movement(self):
        """Determine what the knight should do based on its state."""
        if self.state == State.RUN:
            self.chase_target()
        elif self.state == State.PATROL:
            self.patrol()
        elif self.state == State.IDLE:
            if pygame.time.get_ticks() - self.state_timer >= self.idle_time:
                self.state = State.PATROL  # Resume patrol after idle time is over
                print("Idle time over. Resuming patrol.")
                self.state_timer = pygame.time.get_ticks()  # Reset timer for next patrol


    def draw(self, surface):
        if self.selected:
            pygame.draw.rect(surface, (255, 0, 0), self.rect.inflate(10, 10), 2)  # Draw a red border around the knight
        surface.blit(self.image, self.rect)

    def update(self, dt):
        """Update knight's behavior and animations."""
        self.movement()
        self.animate(dt)

    def animate(self, dt):
        self.animation_timer += dt * 8500  # Increment animation timer
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.current_sprite]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def selection(self):
        """Handle selection of the knight."""
        self.selected = True
        self.state = State.IDLE  # Stop patrolling and play idle animation
        print("Knight selected")

    def deselect(self):
        """Handle deselection of the knight."""
        self.selected = False
        self.state = State.PATROL  # Resume patrolling
        print("Knight deselected")

    def move_to(self, target):
        self.target = target
        self.state = State.RUN  # Change state to RUN to play run animation
        self.state_timer = 0  # Reset the state timer

    def move_to_potion(self, potion_position):
        """Stop current actions and move to the potion marker."""
        self.target = potion_position
        self.state = State.RUN  # Switch to the RUN state
        self.state_timer = 0  # Reset the state timer
        print(f"Knight is moving towards potion: {potion_position}")

    def patrol(self):
        """Patrol between predefined points."""
        if self.target:  # Interrupt patrolling if there's a target
            return

        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards(target_point)

        # Check if the knight has reached the patrol point
        if self.rect.center == target_point:
            self.state = State.IDLE  # Switch to idle state
            self.idle_time = random.randint(2000, 5000)  # Random idle time between 2 to 5 seconds
            self.state_timer = pygame.time.get_ticks()  # Start the idle timer
            print(f"Knight reached patrol point {target_point}. Idling for {self.idle_time / 1000:.1f} seconds.")
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def chase_target(self):
        """Move toward the set target with tolerance."""
        if self.target:
            reached_target = self.move_towards(self.target, tolerance=10)  # Adjust tolerance as needed
            
            # Check if the knight has reached the target (within tolerance)
            if reached_target:
                self.target = None  # Reset target
                self.state = State.IDLE  # Switch to IDLE state after reaching the target
                self.idle_time = 600  # Set idle time to 60 seconds (60000 ms)
                self.state_timer = pygame.time.get_ticks()  # Start the idle timer
                print("Knight reached the target. Staying idle for 60 seconds.")



    def move_towards(self, target, tolerance=10):
        """Move the knight towards the target position with a tolerance."""
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * 2  # Adjust speed as necessary
        self.rect.y += dy * 2  # Adjust speed as necessary

        # Flip the image based on direction
        if dx > 0 and not self.facing_right:
            self.facing_right = True
        elif dx < 0 and self.facing_right:
            self.facing_right = False

        # Check if the knight is within the target area (with tolerance)
        if abs(dx * dist) < tolerance and abs(dy * dist) < tolerance:
            return True
        return False
