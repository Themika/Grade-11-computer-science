import pygame
import random
import time
from Resources.RawReasources.Meat import Meat

class Sheep(pygame.sprite.Sprite):
    def __init__(self, x, y, all_sheep, meat_group, reasources, group_leader=None):
        super().__init__()
        self.images = [pygame.image.load(f'Animations/Reasources/Sheep/Run/HappySheep_Bouncing_{i}.png') for i in range(1, 6)]  # Load your sheep animation frames
        self.images = [pygame.transform.scale(image, (image.get_width() * 1.5, image.get_height() * 1.5)) for image in self.images]  # Scale images to be larger
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.animation_index = 0
        self.animation_time = 0.1
        self.last_update = time.time()
        self.idle_time = 3
        self.last_idle = time.time()
        self.target_pos = self.get_random_position() if group_leader is None else None  # Only leader has a target position
        self.direction = 1  
        self.all_sheep = all_sheep
        self.meat_group = meat_group  
        self.velocity = pygame.math.Vector2(0, 0)
        self.health = 1000
        self.meat_spawned = False 
        self.reasources = reasources
        self.group_leader = group_leader

    def get_random_position(self):
        return random.randint(0, 3000), random.randint(0, 3000)

    def update(self):
        current_time = time.time()
        if self.group_leader:
            self.follow_leader()
        else:
            if current_time - self.last_idle > self.idle_time:
                self.target_pos = self.get_random_position()  # Update the target position for each sheep
                self.last_idle = current_time

            target_vector = pygame.math.Vector2(self.target_pos) - pygame.math.Vector2(self.rect.center)
            if target_vector.length() > 1:
                self.velocity = target_vector.normalize() * 2  
            else:
                self.target_pos = self.get_random_position()  
                self.velocity = pygame.math.Vector2(0, 0)

        if current_time - self.last_update > self.animation_time:
            self.animation_index = (self.animation_index + 1) % len(self.images)
            self.image = self.images[self.animation_index]
            if self.direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)  
            self.last_update = current_time

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        if self.velocity.x > 0:
            self.direction = 1
        elif self.velocity.x < 0:
            self.direction = -1

        self.prevent_overlap()

        # Highlight the group leader
        if self.group_leader is None:
            pygame.draw.circle(self.image, (255, 0, 0), (self.rect.width // 2, self.rect.height // 2), self.rect.width // 2, 2)

    def follow_leader(self):
        target_vector = pygame.math.Vector2(self.group_leader.rect.center) - pygame.math.Vector2(self.rect.center)
        if target_vector.length() > 1:
            self.velocity = target_vector.normalize() * 2  
        else:
            self.velocity = pygame.math.Vector2(0, 0)

    def prevent_overlap(self):
        for sheep in self.all_sheep:
            if sheep != self and self.rect.colliderect(sheep.rect):
                overlap_vector = pygame.math.Vector2(self.rect.center) - pygame.math.Vector2(sheep.rect.center)
                if overlap_vector.length() > 0:
                    overlap_vector = overlap_vector.normalize() * 1
                    self.rect.x += overlap_vector.x
                    self.rect.y += overlap_vector.y

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.spawn_meat()
            self.kill()  

    def spawn_meat(self):
        """Spawns 3 gold pieces at the mine's location within a 10 by 10 radius and marks the mine as destroyed."""
        if not self.meat_spawned:  
            for _ in range(3):
                offset_x = random.randint(-30, 20)
                offset_y = random.randint(-20, 20)
                meat = Meat(self.rect.centerx + offset_x, self.rect.centery + offset_y, "Tiny_Swords_Assets/Resources/Resources/M_Idle_(NoShadow).png", 500)
                self.meat_group.add(meat)
                self.reasources.add(meat)
            self.meat_spawned = True  
        self.is_destroyed = True