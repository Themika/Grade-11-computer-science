import pygame

class Camera:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.camera = pygame.Rect(0, 0, width, height)
        self.zoom_factor = 1.0

    def custom_draw(self, surface, sprites):
        # Adjust the drawing position based on the camera
        for sprite in sprites:
            adjusted_rect = self.apply(sprite)
            surface.blit(sprite.image, adjusted_rect)

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Center the camera on the target
        self.camera = pygame.Rect(target.rect.centerx - self.width // 2,
                                  target.rect.centery - self.height // 2,
                                  self.width, self.height)

    def move(self, dx, dy):
        self.camera.x += dx
        self.camera.y += dy

    def zoom(self, zoom_factor, mouse_pos, sprites):
        self.zoom_factor *= zoom_factor
        old_width, old_height = self.width, self.height
        self.width = int(self.width * zoom_factor)
        self.height = int(self.height * zoom_factor)

        # Adjust camera position to zoom towards the mouse position
        mouse_x, mouse_y = mouse_pos
        self.camera.x = int(mouse_x - (mouse_x - self.camera.x) * zoom_factor)
        self.camera.y = int(mouse_y - (mouse_y - self.camera.y) * zoom_factor)

        for sprite in sprites:
            sprite.image = pygame.transform.scale(sprite.image, (int(sprite.rect.width * zoom_factor), int(sprite.rect.height * zoom_factor)))
            sprite.rect = sprite.image.get_rect(center=sprite.rect.center)