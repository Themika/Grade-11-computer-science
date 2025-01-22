import pygame
from allies.knight import Knight
from allies.archer import Archer
from allies.pawn import Pawn
from utils.ui import UI

class RPSManager:
    def __init__(self):
        self.selected_units = []  # List to store selected units
        self.move_marker = None  # Position of the move marker
        self.marker_time = None  # Time when the marker is set
        self.ui = UI()  # Initialize the UI class
        self.marker_image = pygame.image.load('Tiny_Swords_Assets/UI/Pointers/02.png').convert_alpha()  # Load marker image
        self.marker_alpha = 255  # Full opacity for the marker
        self.marker_scale = 1.0  # Initial scale for the placement animation
        self.dragging = False  # Flag to check if dragging is in progress
        self.drag_start = None  # Starting position of the drag
        self.drag_rect = None  # Rectangle for the drag selection

    def handle_event(self, event, camera, all_sprites, enemies):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position
            map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)  # Adjust for camera offset
            if event.button == 3:  # Right click
                self.dragging = True  # Start dragging
                self.drag_start = map_pos  # Set drag start position
                self.drag_rect = pygame.Rect(self.drag_start, (0, 0))  # Initialize drag rectangle

        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_pos = pygame.mouse.get_pos()  # Get mouse position
                map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)  # Adjust for camera offset
                self.drag_rect.width = map_pos[0] - self.drag_start[0]  # Update drag rectangle width
                self.drag_rect.height = map_pos[1] - self.drag_start[1]  # Update drag rectangle height

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()  # Get mouse position
            map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)  # Adjust for camera offset
            if event.button == 3:  # Right click
                self.dragging = False  # Stop dragging
                if self.drag_rect.width == 0 and self.drag_rect.height == 0:
                    # Single unit selection
                    for sprite in all_sprites:
                        if isinstance(sprite, (Knight, Archer)) and sprite.rect.collidepoint(map_pos):
                            if sprite in self.selected_units:
                                sprite.deselect()  # Deselect unit
                                self.selected_units.remove(sprite)  # Remove from selected units
                            else:
                                self.selected_units.append(sprite)  # Add to selected units
                                sprite.selection()  # Select unit
                            break  # Stop checking other sprites once a unit is selected or deselected
                else:
                    # Drag selection
                    for sprite in all_sprites:
                        if isinstance(sprite, (Knight, Archer, Pawn)) and self.drag_rect.colliderect(sprite.rect):
                            if sprite in self.selected_units:
                                sprite.deselect()  # Deselect unit
                                self.selected_units.remove(sprite)  # Remove from selected units
                            else:
                                self.selected_units.append(sprite)  # Add to selected units
                                sprite.selection()  # Select unit
                self.drag_rect = None  # Reset drag rectangle

            elif event.button == 1:  # Left click
                if self.selected_units:
                    for unit in self.selected_units:
                        unit.move_to_click_position(map_pos)  # Move unit to clicked position
                    self.move_marker = map_pos  # Set move marker position
                    self.marker_time = pygame.time.get_ticks()  # Set the time when the marker is set
                    self.marker_alpha = 255  # Reset alpha to full opacity
                    self.marker_scale = 1.0  # Reset scale for the placement animation

    def draw_marker(self, surface):
        if self.move_marker:
            current_time = pygame.time.get_ticks()  # Get current time
            elapsed_time = current_time - self.marker_time  # Calculate elapsed time

            if elapsed_time > 4000:  # Check if 4 seconds have passed
                self.move_marker = None  # Remove the marker
                self.marker_time = None  # Reset the marker time
            else:
                # Fade effect
                self.marker_alpha = max(0, 255 - (elapsed_time / 4000) * 255)  # Calculate alpha for fade effect
                self.marker_image.set_alpha(self.marker_alpha)  # Set marker image alpha

                # Placement animation (scaling)
                if elapsed_time < 500:  # First 0.5 seconds for scaling animation
                    self.marker_scale = 1.0 + (0.5 - elapsed_time / 1000)  # Scale from 1.5 to 1.0

                scaled_image = pygame.transform.scale(
                    self.marker_image,
                    (int(self.marker_image.get_width() * self.marker_scale),
                     int(self.marker_image.get_height() * self.marker_scale))
                )  # Scale marker image
                marker_rect = scaled_image.get_rect(center=self.move_marker)  # Get marker rectangle
                surface.blit(scaled_image, marker_rect)  # Draw marker on surface

    def draw_ui(self, surface, camera_offset):
        if self.selected_units:
            for unit in self.selected_units:
                exclamation_mark = pygame.font.SysFont(None, 24).render('!', True, (255, 0, 0))  # Create exclamation mark
                adjusted_rect = unit.rect.move(camera_offset)  # Adjust unit rectangle for camera offset
                exclamation_rect = exclamation_mark.get_rect(center=(adjusted_rect.centerx, adjusted_rect.top - 10))  # Position exclamation mark
                surface.blit(exclamation_mark, exclamation_rect)  # Draw exclamation mark on surface
            self.ui.draw_knight_faces(surface, self.selected_units)  # Draw knight faces on UI
        if self.drag_rect:
            adjusted_drag_rect = self.drag_rect.move(camera_offset)  # Adjust drag rectangle for camera offset
            pygame.draw.rect(surface, (0, 255, 0), adjusted_drag_rect, 2)  # Draw drag rectangle on surface
