from Resources.resource import Resource
import pygame

class Gold(Resource):
    def __init__(self, x, y, final_image, spawn_duration, gold_type):
        # Initialize the gold type
        self.type = gold_type
        
        # Load the spawn images for the gold resource
        spawn_images = [
            pygame.image.load(f'Animations/Reasources/Gold_Mine/Gold/G_Spawn_{i}.png').convert_alpha()
            for i in range(1, 6)
        ]
        
        # Call the parent class (Resource) constructor
        super().__init__(x, y, final_image, spawn_images, spawn_duration)

    def add_spawn_image(self, image):
        # Add a spawn image to the resource
        super().add_spawn_image(image)

    def update(self):
        # Update the resource state
        super().update()

    def draw(self, surface, camera_offset):
        # Draw the resource on the given surface with camera offset
        super().draw(surface, camera_offset)