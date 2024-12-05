import pygame 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.WINDOW_HIEGHT = 1280
        self.WINDOW_WIDTH = 720
        self.image = pygame.Surface((50, 50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HIEGHT // 2))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x += self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x -= self.speed
        if keys[pygame.K_UP]:
            self.rect.y += self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y -= self.speed
