import pygame

BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
font = pygame.font.SysFont(None, 36)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

WINDOW_HEIGHT, WINDOW_WIDTH = 1280, 720

class Button:
    def __init__(self, x, y, text, color, hover_color, callback):
        self.rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.callback = callback

    def draw(self, screen, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class Menu:
    def __init__(self):
        self.buttons = []
        self.show_level_select = False

    def create_main_menu(self):
        self.buttons = [
            Button(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 200, "Play", GREEN, GRAY, self.start_level_select),
            Button(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 300, "Quit", RED, GRAY, self.quit_game),
        ]

    def create_level_select_menu(self):
        self.buttons = [
            Button(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 200, "Level 1", BLUE, GRAY, lambda: self.start_game(1)),
            Button(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 300, "Level 2", BLUE, GRAY, lambda: self.start_game(2)),
            Button(WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2, 400, "Level 3", BLUE, GRAY, lambda: self.start_game(3)),
        ]

    def start_level_select(self):
        self.show_level_select = True
        self.create_level_select_menu()

    def start_game(self, level):
        print(f"Starting Level {level}...")
        # Here you'd integrate the main game loop

    def quit_game(self):
        pygame.quit()
        exit()

    def update(self, mouse_pos, mouse_click,display_surface):
        for button in self.buttons:
            button.draw(display_surface, mouse_pos)
            if mouse_click and button.is_clicked(mouse_pos):
                button.callback()