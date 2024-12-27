import pygame
import random

IDLE = 'idle'
RUN = 'run'
CHOPPING = 'chopping'
MOVING_TO_DROP = 'moving_to_drop'

class Pawn(pygame.sprite.Sprite):
    ANIMATION_SPEED = 750
    SPEED = 10

    def __init__(self, *groups):
        super().__init__(*groups)
        self.target_tree = None
        self.target_resources = []
        self.holding_resources = []
        self.state = IDLE
        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.animation_timer = 0
        self.image = self.sprites[self.state][self.current_sprite]
        self.rect = self.image.get_rect(center=(1280 // 2, 720 // 2))
        self.health = 100
        self.facing_right = True
        self.drop_position = None
        self.dropped_resources = []

    def load_sprites(self):
        def load_images(path, count):
            return [pygame.image.load(f'{path}_{i}.png') for i in range(1, count + 1)]

        return {
            IDLE: load_images('Animations/Pawn/Idle/Pawn_Blue_Idle', 5),
            RUN: load_images('Animations/Pawn/Run/Pawn_Blue_Run', 5),
            CHOPPING: load_images('Animations/Pawn/Chopping/Pawn_Blue_Chopping', 5),
            MOVING_TO_DROP: load_images('Animations/Pawn/Run/Pawn_Blue_Run', 5),
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

    def movement(self, pawns):
        if self.state == RUN and self.target_tree:
            dx, dy = self.target_tree.rect.centerx - self.rect.centerx, self.target_tree.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2) ** 0.5
            if distance > self.SPEED:
                dx, dy = dx / distance, dy / distance
                self.rect.x += dx * self.SPEED
                self.rect.y += dy * self.SPEED
                self.update_facing_direction(dx)
            else:
                self.rect.center = self.target_tree.rect.center
                self.state = CHOPPING
            self.avoid_collisions(pawns, dx, dy)

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

    
    def update(self, dt, trees, targeted_trees, resources):
        print(f"The pawn is in {self.state} state")
        if self.state == MOVING_TO_DROP:
            self.move_towards_drop_position(dt)
        else:
            if self.state == CHOPPING:
                self.chop_tree(resources)
            if self.state == IDLE:
                self.search_for_resources(resources)  # Look for resources first
                if not self.target_resources:
                    self.search_for_trees(trees, targeted_trees)
            if self.holding_resources:
                if self.state != MOVING_TO_DROP:
                    self.move_to_random_position()
                self.update_held_resources_position()
            elif self.target_resources:
                self.move_towards_resource(dt)
            elif self.target_tree:
                self.move_towards_tree(dt)
            else:
                self.target_tree = self.get_nearest_tree(trees, targeted_trees)
                if self.target_tree:
                    targeted_trees.add(self.target_tree)
        self.animate(dt)

    def search_for_trees(self, trees, targeted_trees):
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

    def move_towards_tree(self, dt):
        if self.target_tree:
            self.state = RUN
            target_position = pygame.math.Vector2(self.target_tree.rect.left - self.rect.width // 6 + 15, self.target_tree.rect.centery + self.target_tree.rect.height // 4)
            self.move_towards_position(target_position, dt)
            if self.rect.center == target_position:
                self.state = CHOPPING

    def move_towards_resource(self, dt):
        if self.target_resources and len(self.holding_resources) < 3:
            self.state = RUN
            target_resource = self.target_resources[0]
            target_position = pygame.math.Vector2(target_resource.rect.center)
            self.move_towards_position(target_position, dt)
            if self.rect.center == target_position:
                self.pick_up_resource(target_resource)

    def pick_up_resource(self, resource):
        resource.rect.midbottom = self.rect.midtop
        self.holding_resources.append(resource)
        self.target_resources.pop(0)
        if not self.target_resources or len(self.holding_resources) >= 3:
            self.state = MOVING_TO_DROP

    def search_for_resources(self, resources):
        if len(self.holding_resources) < 3:
            nearby_resources = [resource for resource in resources if self.rect.colliderect(resource.rect.inflate(50, 50)) and resource not in self.dropped_resources]
            if nearby_resources:
                nearby_resources.sort(key=lambda resource: ((resource.rect.centerx - self.rect.centerx) ** 2 + (resource.rect.centery - self.rect.centery) ** 2) ** 0.5)
                self.target_resources = nearby_resources[:3]
                self.state = RUN

    def move_to_random_position(self):
        self.drop_position = (random.randint(0, 1280), random.randint(0, 720))
        self.state = MOVING_TO_DROP

    def move_towards_drop_position(self, dt):
        if self.drop_position:
            target_position = pygame.math.Vector2(self.drop_position)
            self.move_towards_position(target_position, dt)
            if self.rect.center == target_position:
                self.drop_resources()
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

    def drop_resources(self):
        for resource in self.holding_resources:
            resource.kill()  # Destroy the resource after dropping it off
        self.holding_resources.clear()
        self.state = IDLE

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        for resource in self.holding_resources:
            screen.blit(resource.image, resource.rect.topleft)
