import pygame

class House(pygame.sprite.Sprite):
    def __init__(self, x, y, construction_image_path, finished_image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.construction_image = pygame.image.load(construction_image_path)
        self.finished_image = pygame.image.load(finished_image_path)
        self.image = self.construction_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.knights = []
        self.archers = []
        self.construction_complete = False

    def update_construction_status(self, wave_ended):
        if wave_ended:
            self.image = self.finished_image
            self.construction_complete = True

    def spawn_knight(self, knight):
        if self.construction_complete:
            knight.rect.topleft = (self.x, self.y)
            self.knights.append(knight)

    def spawn_archer(self, archer):
        if self.construction_complete:
            archer.rect.topleft = (self.x, self.y)
            self.archers.append(archer)

    def draw(self, screen):
        screen.blit(self.image, self.rect)