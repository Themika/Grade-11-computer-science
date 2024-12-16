import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.units = []

    def draw_tower(self, screen):
        screen.blit(self.image, self.rect)
        for unit in self.units:
            if unit.type == "archer":
                unit.draw(screen)

    def place_unit(self, unit):
        if unit.type == "archer":
            if unit in self.units:
                self.remove_unit(unit)
            else:
                unit.rect.midbottom = (self.rect.midtop[0], self.rect.midtop[1] + 90)
                unit.on_tower = True  # Set the flag to indicate the archer is on the tower
                self.units.append(unit)

    def remove_unit(self, unit):
        if unit in self.units:
            unit.on_tower = False  # Reset the flag to indicate the archer is no longer on the tower
            self.units.remove(unit)
            unit.rect.midbottom = (self.rect.midbottom[0], self.rect.midbottom[1] + 90)  # Adjust the position as needed