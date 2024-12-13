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
        self.direction = (dx / distance, dy / distance)

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