import pygame

class Camera:
    def __init__(self, width, height, max_width, max_height):
        # Initialize the camera with given dimensions and maximum bounds
        self.width = width
        self.height = height
        self.max_width = max_width
        self.max_height = max_height
        self.camera = pygame.Rect(0, 0, width, height)
        self.zoom_factor = 1.0

    def custom_draw(self, surface, sprites):
        # Draw all sprites adjusted by the camera's position
        for sprite in sprites:
            adjusted_rect = self.apply(sprite)
            surface.blit(sprite.image, adjusted_rect)

    def apply(self, entity):
        # Adjust the entity's position based on the camera's position
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Center the camera on the target entity
        self.camera = pygame.Rect(target.rect.centerx - self.width // 2,
                                  target.rect.centery - self.height // 2 - 300,
                                  self.width, self.height)
        # Clamp the target's position within specific bounds
        if target.rect.centerx > 575:
            target.rect.centerx = 575
        if target.rect.centerx < -875:
            target.rect.centerx = -875
        if target.rect.centery > 640:
            target.rect.centery = 640
        if target.rect.centery < -1615:
            target.rect.centery = -1615
        self.clamp_camera()

    def move(self, dx, dy):
        # Move the camera by a certain amount
        self.camera.x += dx
        self.camera.y += dy
        self.clamp_camera()

    def clamp_camera(self):
        # Clamp the camera's x and y coordinates within specific bounds
        self.camera.x = max(-1515, min(self.camera.x, -70))
        self.camera.y = max(-2270, min(self.camera.y, -20))