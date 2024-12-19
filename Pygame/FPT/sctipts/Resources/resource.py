import pygame
import os

class Resource(pygame.sprite.Sprite):
    ANIMATION_SPEED = 700
    ANIMATION_DURATION = 500  # 3 seconds in milliseconds

    def __init__(self, x, y, images_folder, spawn_animation_frames, final_image):
        super().__init__()
        self.x = x
        self.y = y
        self.images_folder = images_folder
        self.spawn_animation_frames = spawn_animation_frames
        self.current_frame = 0
        self.image = self.spawn_animation_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_timer = 0
        self.sprites = {'spawn': self.spawn_animation_frames}
        self.animation_done = False
        self.final_image = pygame.image.load(final_image).convert_alpha()
        self.spawn_start_time = pygame.time.get_ticks()

    def load_sprites(self):
        sprites = {
            'spawn': self.load_images(self.images_folder)
        }
        return sprites

    def load_images(self, folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                img = pygame.image.load(os.path.join(folder, filename)).convert_alpha()
                images.append(img)
        return images

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_start_time >= self.ANIMATION_DURATION:
            self.animation_done = True
            self.sprites['spawn'] = []  # Destroy the spawn animation frames
            self.image = self.final_image
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        if not self.animation_done:
            self.animate(dt)

    def animate(self, dt):
        self.animation_timer += dt * 1000
        if self.animation_timer >= self.ANIMATION_SPEED:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.sprites['spawn']):
                self.animation_done = True
                self.image = self.final_image
            else:
                self.image = self.sprites['spawn'][self.current_frame]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_done = True
