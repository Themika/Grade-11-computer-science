import pygame

class Resource(pygame.sprite.Sprite):
    def __init__(self, x, y, final_image, spawn_images=None, spawn_duration=0):
        super().__init__()
        self.x = x
        self.y = y
        self.final_image = pygame.image.load(final_image).convert_alpha()
        self.image = self.final_image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.spawn_images = spawn_images if spawn_images else []
        self.spawn_duration = spawn_duration
        self.spawn_start_time = pygame.time.get_ticks()
        self.image_index = 0

    def add_spawn_image(self, image):
        self.spawn_images.append(image)
        if len(self.spawn_images) == 1:
            self.image = image

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_start_time

        if elapsed_time < self.spawn_duration and self.spawn_images:
            frame_duration = self.spawn_duration // len(self.spawn_images)
            self.image_index = min(elapsed_time // frame_duration, len(self.spawn_images) - 1)
            self.image = self.spawn_images[self.image_index]
        else:
            self.image = self.final_image

    def draw(self, surface, camera_offset):
        adjusted_rect = self.rect.move(camera_offset)
        surface.blit(self.image, adjusted_rect)
