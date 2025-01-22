import pygame

class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.health = 10000
        self.max_health = 10000

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
        self.draw_health_bar(surface, adjusted_rect.topleft)

    def draw_health_bar(self, surface, position):
        bar_width = 50
        bar_height = 5
        health_ratio = self.health / self.max_health
        health_bar_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width * health_ratio, bar_height)
        border_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(surface, (255, 255, 255), border_rect, 1)

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
