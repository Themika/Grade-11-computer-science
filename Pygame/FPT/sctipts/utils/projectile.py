import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, target_pos, damage, image_path, *groups):
        super().__init__(*groups)
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.original_image.get_rect(center=start_pos)
        self.speed = 5  
        self.damage = damage

        # Calculate direction
        dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        self.direction = (0, 0) if distance == 0 else (dx / distance, dy / distance)

        # Calculate angle and rotate image
        angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def update(self, dt, enemies):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        self.check_collision(enemies)

    def check_collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.health -= self.damage
                self.kill()  # Remove the projectile after it hits an enemy

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)

class Dynamite(Projectile):
    def __init__(self, start_pos, target_pos, damage, image_path, *groups):
        super().__init__(start_pos, target_pos, damage, image_path, *groups)
        self.angle = 0  # Initialize the angle for rotation
        self.explosion_images = [
            pygame.image.load(f'Animations/Goblins/Explosion/Explosions_{i}.png') for i in range(3, 11)
        ]
        self.exploding = False
        self.explosion_index = 0

    def update(self, dt, knights, archers):
        if not self.exploding:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed
            self.angle += 5  # Increment the angle for rotation
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.check_collision(knights, archers)
        else:
            self.explode()

    def check_collision(self, knights, archers):
        for knight in knights:
            if self.rect.colliderect(knight.rect):
                knight.health -= self.damage
                self.start_explosion()

        for archer in archers:
            if self.rect.colliderect(archer.rect):
                archer.health -= self.damage
                self.start_explosion()

    def start_explosion(self):
        self.exploding = True
        self.explosion_index = 0

    def explode(self):
        if self.explosion_index < len(self.explosion_images):
            self.image = self.explosion_images[self.explosion_index]
            self.explosion_index += 1
        else:
            self.kill()  # Remove the dynamite after the explosion animation is done