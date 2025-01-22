import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, construction_image_path, finished_image_path, total_waves, destroyed_image_path):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # Load images for different tower states
        self.construction_image = pygame.image.load(construction_image_path)
        self.finished_image = pygame.image.load(finished_image_path)
        self.destroyed_image = pygame.image.load(destroyed_image_path)
        # Set initial image to construction image
        self.image = pygame.transform.scale(self.construction_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.units = []
        self.wave_counter = 0
        self.total_waves = total_waves
        self.construction_complete = False
        self.unit_on_tower = False
        self.construction_status = 'under_construction'
        self.health = 1000
        self.max_health = 1000

    def draw(self, surface, camera_offset):
        # Draw the tower on the surface with camera offset
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
        self.draw_health_bar(surface, adjusted_rect.topleft)

    def draw_health_bar(self, surface, position):
        # Draw the health bar above the tower
        bar_width = 50
        bar_height = 5
        health_ratio = self.health / self.max_health
        health_bar_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width * health_ratio, bar_height)
        border_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width, bar_height)
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        pygame.draw.rect(surface, (255, 255, 255), border_rect, 1)

    def update_construction_status(self, wave_ended):
        # Update the construction status based on waves
        if wave_ended:
            self.wave_counter += 1
            if self.wave_counter >= self.total_waves:
                self.image = pygame.transform.scale(self.finished_image, (self.width, self.height))
                self.construction_complete = True
                self.is_fully_constructed()

    def update(self):
        # Update the tower state
        if self.health <= 0:
            self.image = self.destroyed_image
        self.update_construction_status()

    def draw_tower(self, surface, camera_offset):
        # Draw the tower and any units on it
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
        for unit in self.units:
            if unit.type == "archer":
                unit.draw(surface, camera_offset)

    def place_unit(self, unit):
        # Place a unit on the tower if construction is complete
        if self.construction_complete and unit.type == "archer":
            if self.unit_on_tower:
                print("There is already an archer on this tower.")
            else:
                unit.rect.midbottom = (self.rect.midtop[0], self.rect.midtop[1] + 90)
                self.unit_on_tower = True  
                self.units.append(unit)

    def remove_unit(self):
        # Remove a unit from the tower
        if self.units:
            unit = self.units.pop()
            self.unit_on_tower = False  # Reset the flag to indicate the archer is no longer on the tower
            unit.rect.midbottom = (self.rect.midbottom[0], self.rect.midbottom[1] + 90)  # Adjust the position as needed
            unit.on_tower = False

    def is_fully_constructed(self):
        # Check if the tower is fully constructed
        return self.construction_status == 'finished'

    def heal(self, amount):
        # Heal the tower by a certain amount
        self.health = min(self.max_health, self.health + amount)