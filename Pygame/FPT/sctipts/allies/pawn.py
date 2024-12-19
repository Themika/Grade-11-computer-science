import pygame

IDLE = 'idle'
RUN = 'run'
CHOPPING = 'chopping'
COLLECTING = 'collecting'

class Pawn(pygame.sprite.Sprite):
    ANIMATION_SPEED = 750
    SPEED = 2  # Define a speed for the pawn

    def __init__(self, *groups):
        super().__init__(*groups)
        self.target_tree = None
        self.target_resource = None
        self.state = IDLE  # Ensure the initial state is IDLE
        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.animation_timer = 0
        self.image = self.sprites[self.state][self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.center = (1280 // 2, 720 // 2)  
        self.health = 100
        self.facing_right = True  # Track the direction the pawn is facing

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
            COLLECTING: run_sprites,  # Use run sprites for collecting as a placeholder
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

    def update(self, dt, trees, targeted_trees, resources):
        if self.state == CHOPPING:
            self.chop_tree()

        if self.state == IDLE:
            self.search_for_trees(trees, targeted_trees)
            if not self.target_tree:
                self.search_for_resources(resources)

        if self.target_tree is None or self.target_tree not in trees:
            self.target_tree = self.get_nearest_tree(trees, targeted_trees)
            if self.target_tree:
                targeted_trees.add(self.target_tree)

        if self.target_tree:
            self.move_towards_tree(dt)
        elif self.target_resource:
            self.move_towards_resource(dt)

        self.animate(dt)

    def search_for_trees(self, trees, targeted_trees):
        for tree in trees:
            if tree not in targeted_trees and self.rect.colliderect(tree.rect.inflate(50, 50)):
                self.target_tree = tree
                self.state = RUN
                targeted_trees.add(tree)
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
                self.target_tree.take_damage(1)  # Deal damage to the tree
                if self.target_tree.health <= 0:
                    self.target_tree = None
                    self.state = IDLE  # Transition to IDLE state after chopping down the tree

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

    def move_towards_resource(self, dt):
        if self.target_resource:
            self.state = COLLECTING  # Set state to COLLECTING when moving towards the resource
            target_position = pygame.math.Vector2(self.target_resource.rect.center)
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
                self.collect_resource()

    def collect_resource(self):
        if self.target_resource:
            self.rect.center = self.target_resource.rect.center
            self.target_resource.kill()
            self.target_resource = None
            self.state = IDLE

    def search_for_resources(self, resources):
        for resource in resources:
            if self.rect.colliderect(resource.rect.inflate(100, 100)):
                self.target_resource = resource
                self.state = COLLECTING
                break