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
        self.construction_status = 'under_construction'
        self.knight_count = 0
        self.archer_count = 0
        self.max_health = 500
        self.health = 500
        self.ui_visible = False  

    def update_construction_status(self, wave_ended):
        if wave_ended:
            self.image = self.finished_image
            self.construction_complete = True
            self.is_fully_constructed()

    def spawn_knight(self, knight):
        if self.construction_complete and len(self.knights) < self.knight_count:
            knight.rect.topleft = (self.x, self.y)
            self.knights.append(knight)
            self.move_unit_outwards(knight)

    def spawn_archer(self, archer):
        if self.construction_complete and len(self.archers) < self.archer_count:
            archer.rect.topleft = (self.x, self.y)
            self.archers.append(archer)
            self.move_unit_outwards(archer)

    def move_unit_outwards(self, unit):
        # Move the unit outwards from the house
        unit.rect.x += 10  # Adjust the value as needed
        unit.rect.y += 10  # Adjust the value as needed
    def take_damage(self, damage):
        self.health -= damage

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

    def is_fully_constructed(self):
        return self.construction_status == 'finished'

