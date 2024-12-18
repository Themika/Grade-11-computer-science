import pygame
import os

class Resource(pygame.sprite.Sprite):
    def __init__(self, x, y, images_folder, spawn_animation_frames):
        super().__init__()
        self.x = x
        self.y = y
        self.images = self.load_images(images_folder)
        self.spawn_animation_frames = spawn_animation_frames
        self.current_frame = 0
        self.image = self.spawn_animation_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_speed = 60 / 1000
        self.animation_counter = 0

    def load_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                images.append(img)
        return images

    def update(self):
        self.animate()

    def animate(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.spawn_animation_frames)
            self.image = self.spawn_animation_frames[self.current_frame]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))