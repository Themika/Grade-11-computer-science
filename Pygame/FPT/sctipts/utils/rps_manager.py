import pygame
from allies.knight import Knight
from allies.archer import Archer
from utils.ui import UI

class RPSManager:
    def __init__(self):
        self.selected_units = []  # Changed to a more generic name
        self.move_marker = None
        self.marker_time = None  # Store the time when the marker is set
        self.ui = UI()  # Initialize the UI class
        self.marker_image = pygame.image.load('Tiny_Swords_Assets/UI/Pointers/02.png').convert_alpha()
        self.marker_alpha = 255  # Full opacity
        self.marker_scale = 1.0  # Initial scale for the placement animation
        self.dragging = False
        self.drag_start = None
        self.drag_rect = None

    def handle_event(self, event, camera, all_sprites, enemies):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
            print(f"Mouse position: {mouse_pos}, Map position: {map_pos}")
            if event.button == 3:  # Right click
                self.dragging = True
                self.drag_start = map_pos
                self.drag_rect = pygame.Rect(self.drag_start, (0, 0))

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_pos = pygame.mouse.get_pos()
                map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
                self.drag_rect.width = map_pos[0] - self.drag_start[0]
                self.drag_rect.height = map_pos[1] - self.drag_start[1]

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
            if event.button == 3:  # Right click
                self.dragging = False
                if self.drag_rect.width == 0 and self.drag_rect.height == 0:
                    # Single unit selection
                    for sprite in all_sprites:
                        if isinstance(sprite, (Knight, Archer)) and sprite.rect.collidepoint(map_pos):
                            if sprite in self.selected_units:
                                sprite.deselect()
                                self.selected_units.remove(sprite)
                            else:
                                self.selected_units.append(sprite)
                                sprite.selection()
                            break  # Stop checking other sprites once a unit is selected or deselected
                else:
                    # Drag selection
                    for sprite in all_sprites:
                        if isinstance(sprite, (Knight, Archer)) and self.drag_rect.colliderect(sprite.rect):
                            if sprite in self.selected_units:
                                sprite.deselect()
                                self.selected_units.remove(sprite)
                            else:
                                self.selected_units.append(sprite)
                                sprite.selection()
                self.drag_rect = None

            elif event.button == 1:  # Left click
                if self.selected_units:
                    for unit in self.selected_units:
                        unit.move_to_click_position(map_pos)
                    self.move_marker = map_pos
                    self.marker_time = pygame.time.get_ticks()  # Set the time when the marker is set
                    self.marker_alpha = 255  # Reset alpha to full opacity
                    self.marker_scale = 1.0  # Reset scale for the placement animation

    def draw_marker(self, surface):
        if self.move_marker:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.marker_time

            if elapsed_time > 4000:  # Check if 4 seconds have passed
                self.move_marker = None  # Remove the marker
                self.marker_time = None  # Reset the marker time
            else:
                # Fade effect
                self.marker_alpha = max(0, 255 - (elapsed_time / 4000) * 255)
                self.marker_image.set_alpha(self.marker_alpha)

                # Placement animation (scaling)
                if elapsed_time < 500:  # First 0.5 seconds for scaling animation
                    self.marker_scale = 1.0 + (0.5 - elapsed_time / 1000)  # Scale from 1.5 to 1.0

                scaled_image = pygame.transform.scale(
                    self.marker_image,
                    (int(self.marker_image.get_width() * self.marker_scale),
                     int(self.marker_image.get_height() * self.marker_scale))
                )
                marker_rect = scaled_image.get_rect(center=self.move_marker)
                surface.blit(scaled_image, marker_rect)

    def draw_ui(self, surface, camera_offset):
        if self.selected_units:
            for unit in self.selected_units:
                exclamation_mark = pygame.font.SysFont(None, 24).render('!', True, (255, 0, 0))
                adjusted_rect = unit.rect.move(camera_offset)
                exclamation_rect = exclamation_mark.get_rect(center=(adjusted_rect.centerx, adjusted_rect.top - 10))
                surface.blit(exclamation_mark, exclamation_rect)
            self.ui.draw_knight_faces(surface, self.selected_units)
        if self.drag_rect:
            adjusted_drag_rect = self.drag_rect.move(camera_offset)
            pygame.draw.rect(surface, (0, 255, 0), adjusted_drag_rect, 2)
