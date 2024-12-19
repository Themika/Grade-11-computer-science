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
        self.ui_visible = False  # Flag to track if the UI is currently visible

    def update_construction_status(self, wave_ended):
        if wave_ended:
            self.image = self.finished_image
            self.construction_complete = True
            self.is_fully_constructed()

    def spawn_knight(self, knight):
        if self.construction_complete and len(self.knights) < self.knight_count:
            knight.rect.topleft = (self.x, self.y)
            self.knights.append(knight)

    def spawn_archer(self, archer):
        if self.construction_complete and len(self.archers) < self.archer_count:
            archer.rect.topleft = (self.x, self.y)
            self.archers.append(archer)

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
        if self.ui_visible:
            self.show_spawn_ui(surface, pygame.font.SysFont(None, 24), camera_offset)

    def is_fully_constructed(self):
        return self.construction_status == 'finished'

    def show_spawn_ui(self, surface, font, camera_offset):
        if self.construction_complete:
            adjusted_rect = self.rect.move(camera_offset)
            knight_text = font.render(f"Knights: {self.knight_count}", True, (255, 255, 255))
            archer_text = font.render(f"Archers: {self.archer_count}", True, (255, 255, 255))
            surface.blit(knight_text, (adjusted_rect.x, adjusted_rect.y - 45))
            surface.blit(archer_text, (adjusted_rect.x, adjusted_rect.y - 30))

            # Draw buttons
            self.draw_buttons(surface, font, adjusted_rect)

    def draw_buttons(self, surface, font, adjusted_rect):
        # Define button positions
        knight_plus_rect = pygame.Rect(adjusted_rect.x + 100, adjusted_rect.y - 45, 20, 20)
        knight_minus_rect = pygame.Rect(adjusted_rect.x + 130, adjusted_rect.y - 45, 20, 20)
        archer_plus_rect = pygame.Rect(adjusted_rect.x + 100, adjusted_rect.y - 30, 20, 20)
        archer_minus_rect = pygame.Rect(adjusted_rect.x + 130, adjusted_rect.y - 30, 20, 20)

        # Draw buttons
        pygame.draw.rect(surface, (0, 255, 0), knight_plus_rect)
        pygame.draw.rect(surface, (255, 0, 0), knight_minus_rect)
        pygame.draw.rect(surface, (0, 255, 0), archer_plus_rect)
        pygame.draw.rect(surface, (255, 0, 0), archer_minus_rect)

        # Draw button text
        plus_text = font.render("+", True, (0, 0, 0))
        minus_text = font.render("-", True, (0, 0, 0))
        surface.blit(plus_text, knight_plus_rect.topleft)
        surface.blit(minus_text, knight_minus_rect.topleft)
        surface.blit(plus_text, archer_plus_rect.topleft)
        surface.blit(minus_text, archer_minus_rect.topleft)

        # Store button rects for click detection
        self.knight_plus_rect = knight_plus_rect
        self.knight_minus_rect = knight_minus_rect
        self.archer_plus_rect = archer_plus_rect
        self.archer_minus_rect = archer_minus_rect

    def handle_click(self, pos):
        if self.knight_plus_rect.collidepoint(pos):
            self.knight_count += 1
            print("KNIGHT")
        elif self.knight_minus_rect.collidepoint(pos) and self.knight_count > 0:
            self.knight_count -= 1
        elif self.archer_plus_rect.collidepoint(pos):
            self.archer_count += 1
            print("Archer")
        elif self.archer_minus_rect.collidepoint(pos) and self.archer_count > 0:
            self.archer_count -= 1
        # Redraw the UI to reflect the updated counts
        self.ui_visible = True
        self.draw(pygame.display.get_surface(), (0, 0))  # Update the UI immediately