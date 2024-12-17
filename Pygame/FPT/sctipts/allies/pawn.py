import pygame
import random

# Define constants for the states
IDLE = 'idle'
RUN = 'run'
CHOPPING = 'chopping'
WANDERING = 'wandering'

"""
Have it so it eitehr chooses ot cut  a tree, kill a sheep or mine for gold. After that they take  a 
break and wander around for a bit and idle aroud add a ffect shoing tehy are taking a break
Finish AI for the pawn
"""
class Pawn(pygame.sprite.Sprite):
    ANIMATION_SPEED = 750
    SPEED = 2  # Define a speed for the pawn
    WANDER_TIME = 60000  # 1 minute in milliseconds

    def __init__(self, *groups):
        super().__init__(*groups)
        self.target_tree = None
        self.state = IDLE  # Ensure the initial state is IDLE
        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.animation_timer = 0
        self.image = self.sprites[self.state][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2)  
        self.health = 100
        self.facing_right = True  # Track the direction the pawn is facing
        self.wander_timer = 0
        self.wander_direction = pygame.math.Vector2(0, 0)  # Initialize wander_direction

    def load_sprites(self):
        idle_sprites = [
            pygame.image.load(f'Animations/Pawn/Idle/Pawn_Blue_Idle_{i}.png') for i in range(1, 6)
        ]
        run_sprites = [
            pygame.image.load(f'Animations/Pawn/Run/Pawn_Blue_Run_{i}.png') for i in range(1, 6)
        ]
        chopping_sprites = [
            pygame.image.load(f'Animations/Pawn/Chopping/Pawn_Blue_Chopping_{i}.png') for i in range(1, 6)
        ]
        return {
            IDLE: idle_sprites,
            RUN: run_sprites,
            CHOPPING: chopping_sprites,
            WANDERING : run_sprites
        }

    def animate(self, dt):
        self.animation_timer += dt * 8500
        if self.animation_timer >= self.ANIMATION_SPEED:
            self.animation_timer = 0
            self.current_sprite = (self.current_sprite + 1) % len(self.sprites[self.state])
            self.image = self.sprites[self.state][self.current_sprite]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if facing left

    def movement(self, pawns):
        if self.state == RUN and self.target_tree:
            dx, dy = self.target_tree.rect.centerx - self.rect.centerx, self.target_tree.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            if distance > self.SPEED:
                dx, dy = dx / distance, dy / distance  # Normalize the direction
                self.rect.x += dx * self.SPEED
                self.rect.y += dy * self.SPEED
                if dx < 0 and self.facing_right:
                    self.facing_right = False
                    self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if moving left
                elif dx > 0 and not self.facing_right:
                    self.facing_right = True
                    self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if moving right
            else:
                self.rect.center = self.target_tree.rect.center
                self.state = CHOPPING
                print("Reached tree, starting to chop")
            
            # Check for collisions with other pawns
            for pawn in pawns:
                if pawn != self and self.rect.colliderect(pawn.rect):
                    # Adjust position to avoid overlap
                    if dx > 0:
                        self.rect.right = pawn.rect.left
                    elif dx < 0:
                        self.rect.left = pawn.rect.right
                    if dy > 0:
                        self.rect.bottom = pawn.rect.top
                    elif dy < 0:
                        self.rect.top = pawn.rect.bottom

    def update(self, dt, trees, pawns, targeted_trees):
        print(self.wander_timer)
        if self.state == WANDERING:
            self.wander(dt)
        else:
            if self.state == IDLE:
                print("Searching for trees")
                self.search_for_trees(trees, targeted_trees)
            if self.target_tree is None or self.target_tree not in trees:
                self.target_tree = self.get_nearest_tree(trees, targeted_trees)
                if self.target_tree:
                    targeted_trees.add(self.target_tree)

            if self.target_tree:
                self.move_towards_tree(dt)

            if self.state == CHOPPING:
                self.chop_tree()
        self.animate(dt)

    def search_for_trees(self, trees, targeted_trees):
        for tree in trees:
            if tree not in targeted_trees and self.rect.colliderect(tree.rect.inflate(50, 50)):
                self.target_tree = tree
                self.state = RUN
                targeted_trees.add(tree)
                print("Tree found, moving to tree")
                break

    def chop_tree(self):
        if self.target_tree:
            # Flip the sprite based on the tree's position
            if self.target_tree.rect.centerx < self.rect.centerx and self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if tree is on the left
            elif self.target_tree.rect.centerx > self.rect.centerx and not self.facing_right:
                self.facing_right = True
                self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if tree is on the right

            # Only deal damage if the current sprite is the chopping frame
            if self.current_sprite == 2:  # Assuming the 3rd frame (index 2) is the chopping frame
                print("Chopping tree at", self.target_tree.rect.topleft)
                self.target_tree.take_damage(1)  # Deal damage to the tree
                if self.target_tree.health <= 0:
                    self.target_tree = None
                    self.state = WANDERING
                    self.wander_timer = pygame.time.get_ticks()
                    print("Tree destroyed, wandering")

    def get_nearest_tree(self, trees, targeted_trees):
        nearest_tree = None
        min_distance = float('inf')
        for tree in trees:
            if tree not in targeted_trees:
                distance = ((tree.rect.centerx - self.rect.centerx) ** 2 + (tree.rect.centery - self.rect.centery) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_tree = tree
        return nearest_tree

    def move_towards_tree(self, dt):
        if self.target_tree:
            self.state = RUN  # Set state to RUN when moving towards the tree
            target_position = pygame.math.Vector2(self.target_tree.rect.left - self.rect.width//6+15, self.target_tree.rect.centery + self.target_tree.rect.height // 4)
            direction = target_position - pygame.math.Vector2(self.rect.center)
            if direction.length() != 0:
                direction = direction.normalize() * 100 * dt  # Move at a speed of 100 pixels per second
                self.rect.move_ip(direction)
                
                # Flip the sprite based on the direction
                if direction.x < 0 and self.facing_right:
                    self.facing_right = False
                    self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if moving left
                elif direction.x > 0 and not self.facing_right:
                    self.facing_right = True
                    self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if moving right
            else:
                self.state = CHOPPING

    def wander(self, dt):
        """Wander between random points."""
        if pygame.time.get_ticks() - self.wander_timer > self.WANDER_TIME:
            self.state = IDLE
            self.wander_timer = pygame.time.get_ticks()  # Reset the wander timer
            return

        if not hasattr(self, 'wander_points'):
            self.wander_points = self.generate_random_patrol_points(10, 1280, 720)
            self.current_wander_point = 0

        target_position = self.wander_points[self.current_wander_point]
        self.move_towards(target_position)

        if self.rect.center == target_position or self.rect.colliderect(pygame.Rect(target_position, (10, 10))):
            self.current_wander_point = (self.current_wander_point + 1) % len(self.wander_points)

    def move_towards(self, target_position):
        direction = pygame.math.Vector2(target_position) - pygame.math.Vector2(self.rect.center)
        if direction.length() != 0:
            direction = direction.normalize() * self.SPEED
            self.rect.move_ip(direction)

            # Flip the sprite based on the direction
            if direction.x < 0 and self.facing_right:
                self.facing_right = False
                self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if moving left
            elif direction.x > 0 and not self.facing_right:
                self.facing_right = True
                self.image = pygame.transform.flip(self.image, True, False)  # Flip the sprite if moving right

    def generate_random_patrol_points(self, num_points, max_x, max_y):
        """Generate a list of random patrol points within the given range."""
        return [(random.randint(0, max_x), random.randint(0, max_y)) for _ in range(num_points)]

    def selection(self):
        pass

    def attack(self):
        pass
