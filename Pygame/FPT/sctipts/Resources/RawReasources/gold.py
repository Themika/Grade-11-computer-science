from Resources.resource import Resource
import pygame

class Gold(Resource):
    def __init__(self, x, y, final_image, spawn_duration,gold_type):
        self.type = gold_type
        spawn_images = [
            pygame.image.load(f'Animations/Reasources/Gold_Mine/Gold/G_Spawn_{i}.png').convert_alpha()
            for i in range(1, 6)
        ]
        super().__init__(x, y, final_image, spawn_images, spawn_duration)

    def add_spawn_image(self, image):
        super().add_spawn_image(image)

    def update(self):
        super().update()

    def draw(self, surface, camera_offset):
        super().draw(surface, camera_offset)