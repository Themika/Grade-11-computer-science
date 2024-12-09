import pygame
from allies.knight import Knight

class RPSManager:
    def __init__(self):
        self.selected_knights = []
        self.move_marker = None

    def handle_event(self, event, camera, all_sprites):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            adjusted_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
            if event.button == 3:  # Right click
                for sprite in all_sprites:
                    if isinstance(sprite, Knight) and sprite.rect.collidepoint(adjusted_pos):
                        if sprite in self.selected_knights:
                            sprite.deselect()
                            self.selected_knights.remove(sprite)
                        else:
                            self.selected_knights.append(sprite)
                            sprite.selection()
                        break
            elif event.button == 1:  # Left click
                if self.selected_knights:
                    for knight in self.selected_knights:
                        knight.move_to_click_position(adjusted_pos)
                    self.move_marker = adjusted_pos

    def draw_marker(self, surface):
        if self.move_marker:
            pygame.draw.circle(surface, (255, 0, 0), self.move_marker, 5)