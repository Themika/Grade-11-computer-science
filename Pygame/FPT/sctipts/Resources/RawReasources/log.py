from Resources.resource import Resource
import pygame

class Log(Resource):
    def __init__(self, x, y, final_image, spawn_duration, log_type):
        # Initialize the log type
        self.type = log_type
        
        # Load spawn images for the log animation
        spawn_images = [
            pygame.image.load(f'Animations/Reasources/Tree/Logs/W_Spawn_{i}.png').convert_alpha()
            for i in range(1, 7)
        ]
        
        # Call the parent class (Resource) constructor
        super().__init__(x, y, final_image, spawn_images, spawn_duration)

    def add_spawn_image(self, image):
        # Add a new spawn image to the resource
        super().add_spawn_image(image)

    def update(self):
        # Update the resource state
        super().update()

    def draw(self, surface, camera_offset):
        # Draw the resource on the given surface with the camera offset
        super().draw(surface, camera_offset)
