import pygame

class Resource(pygame.sprite.Sprite):
    def __init__(self, x, y, final_image, spawn_images=None, spawn_duration=0):
        super().__init__()
        self.x = x
        self.y = y
        # Load the final image and set it as the current image
        self.final_image = pygame.image.load(final_image).convert_alpha()
        self.image = self.final_image
        # Set the position of the sprite
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Initialize spawn images and duration
        self.spawn_images = spawn_images if spawn_images else []
        self.spawn_duration = spawn_duration
        # Record the start time for spawning
        self.spawn_start_time = pygame.time.get_ticks()
        self.image_index = 0

    def add_spawn_image(self, image):
        # Add a new image to the spawn images list
        self.spawn_images.append(image)
        # If this is the first spawn image, set it as the current image
        if len(self.spawn_images) == 1:
            self.image = image

    def update(self):
        # Calculate the elapsed time since the spawn started
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.spawn_start_time

        # If within spawn duration and there are spawn images
        if elapsed_time < self.spawn_duration and self.spawn_images:
            # Calculate the duration of each frame
            frame_duration = self.spawn_duration // len(self.spawn_images)
            # Determine the current frame index based on elapsed time
            self.image_index = min(elapsed_time // frame_duration, len(self.spawn_images) - 1)
            # Set the current image to the appropriate spawn image
            self.image = self.spawn_images[self.image_index]
        else:
            # Set the image to the final image after spawn duration
            self.image = self.final_image

    def draw(self, surface, camera_offset):
        # Adjust the rectangle position based on camera offset
        adjusted_rect = self.rect.move(camera_offset)
        # Draw the current image on the given surface
        surface.blit(self.image, adjusted_rect)
