import pygame

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect(center=(x, y))
    screen.blit(text, text_rect)

class CutScene:
    def __init__(self, name, scene):
        self.name = name
        self.scene = scene
        self.scene_index = 0
        self.timer = pygame.time.get_ticks()
        self.cut_scene_running = True

    def update(self):
        if self.scene_index < len(self.scene):
            self.scene_index += 1
            return True
        else:
            return False

    def draw(self, screen):
        draw_text(screen, self.scene[self.scene_index - 1], 30, (255, 255, 255), screen.get_width() // 2, screen.get_height() // 2)

class CutSceneManager:
    def __init__(self, screen):
        self.cut_scene_completed = []
        self.cut_scene = None
        self.cut_scene_running = False
        self.screen = screen
        self.circle_radius = 0
        self.max_radius = (screen.get_width() ** 2 + screen.get_height() ** 2) ** 0.5 / 2

    def start_cutscene(self, cut_scene):
        if cut_scene.name not in self.cut_scene_completed:
            self.cut_scene_completed.append(cut_scene.name)
            self.cut_scene = cut_scene
            self.cut_scene_running = True
            self.circle_radius = 0

    def end_cutscene(self):
        self.cut_scene = None
        self.cut_scene_running = False

    def update(self):
        if self.cut_scene_running:
            if self.circle_radius < self.max_radius:
                self.circle_radius += 5  # Increase the radius for fade-in effect
            self.cut_scene_running = self.cut_scene.update()
        else:
            if self.circle_radius > 0:
                self.circle_radius -= 5  # Decrease the radius for fade-out effect
            else:
                self.end_cutscene()

    def draw(self):
        if self.cut_scene_running or self.circle_radius > 0:
            mask = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 0))
            pygame.draw.circle(mask, (0, 0, 0, 255), (self.screen.get_width() // 2, self.screen.get_height() // 2), int(self.circle_radius))
            self.screen.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
            if self.cut_scene_running:
                self.cut_scene.draw(self.screen)