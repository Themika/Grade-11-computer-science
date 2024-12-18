import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, construction_image_path, finished_image_path, total_waves):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.construction_image = pygame.image.load(construction_image_path)
        self.finished_image = pygame.image.load(finished_image_path)
        self.image = pygame.transform.scale(self.construction_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.units = []
        self.wave_counter = 0
        self.total_waves = total_waves
        self.construction_complete = False
        self.construction_status = 'under_construction'
    def update_construction_status(self, wave_ended):
        if wave_ended:
            self.wave_counter += 1
            if self.wave_counter >= self.total_waves:
                self.image = pygame.transform.scale(self.finished_image, (self.width, self.height))
                self.construction_complete = True
                self.is_fully_constructed()

    def draw_tower(self, surface,camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
        for unit in self.units:
            if unit.type == "archer":
                unit.draw(surface,camera_offset)

    def place_unit(self, unit):
        if self.construction_complete and unit.type == "archer":
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
    def is_fully_constructed(self):
        return self.construction_status == 'finished'
