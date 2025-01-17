import pygame

class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
