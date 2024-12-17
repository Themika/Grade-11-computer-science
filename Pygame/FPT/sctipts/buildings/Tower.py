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

    def update_construction_status(self, wave_ended):
        if wave_ended:
            self.wave_counter += 1
            if self.wave_counter >= self.total_waves:
                self.image = pygame.transform.scale(self.finished_image, (self.width, self.height))
                self.construction_complete = True

    def draw_tower(self, screen):
        screen.blit(self.image, self.rect)
        self.draw_progress_bar(screen)
        for unit in self.units:
            if unit.type == "archer":
                unit.draw(screen)

    def draw_progress_bar(self, screen):
        if not self.construction_complete:
            progress = self.wave_counter / self.total_waves
            bar_width = self.width
            bar_height = 5
            fill_width = int(bar_width * progress)
            bar_color = (0, 255, 0)
            background_color = (255, 0, 0)
            bar_rect = pygame.Rect(self.rect.x, self.rect.y - bar_height - 2, bar_width, bar_height)
            fill_rect = pygame.Rect(self.rect.x, self.rect.y - bar_height - 2, fill_width, bar_height)
            pygame.draw.rect(screen, background_color, bar_rect)
            pygame.draw.rect(screen, bar_color, fill_rect)

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