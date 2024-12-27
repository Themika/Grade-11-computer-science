from Resources.resource import Resource
import pygame

class Log(Resource):
    def __init__(self, x, y, final_image, spawn_duration):
        spawn_images = [
            pygame.image.load(f'Animations/Reasources/Tree/Logs/W_Spawn_{i}.png').convert_alpha()
            for i in range(1, 7)
        ]
        super().__init__(x, y, final_image, spawn_images, spawn_duration)

    def add_spawn_image(self, image):
        super().add_spawn_image(image)

    def update(self):
        super().update()

    def draw(self, surface, camera_offset):
        super().draw(surface, camera_offset)
