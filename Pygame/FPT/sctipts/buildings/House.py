import pygame

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.knights = []
        self.archers = []

    def spawn_knight(self, knight):
        knight.rect.topleft = (self.x, self.y)
        self.knights.append(knight)

    def spawn_archer(self, archer):
        archer.rect.topleft = (self.x, self.y)
        self.archers.append(archer)

    def draw(self, screen):
        screen.blit(self.image, self.rect)