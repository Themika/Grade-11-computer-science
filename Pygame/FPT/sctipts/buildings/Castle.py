import pygame

class Castle(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.x = x
        self.y = y
        # Load the image of the castle
        self.image = pygame.image.load(image_path)
        # Get the rectangle for positioning the image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        # Initialize health values
        self.health = 10000
        self.max_health = 10000

    def draw(self, surface, camera_offset):
        # Adjust the rectangle position based on the camera offset
        adjusted_rect = self.rect.move(camera_offset)
        # Draw the castle image on the surface
        surface.blit(self.image, adjusted_rect)
        # Draw the health bar above the castle
        self.draw_health_bar(surface, adjusted_rect.topleft)

    def draw_health_bar(self, surface, position):
        bar_width = 50
        bar_height = 5
        # Calculate the health ratio
        health_ratio = self.health / self.max_health
        # Create the health bar rectangle
        health_bar_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width * health_ratio, bar_height)
        # Create the border rectangle for the health bar
        border_rect = pygame.Rect(position[0] + self.rect.width // 2 - bar_width // 2, position[1] - 10, bar_width, bar_height)
        # Draw the health bar
        pygame.draw.rect(surface, (255, 0, 0), health_bar_rect)
        # Draw the border of the health bar
        pygame.draw.rect(surface, (255, 255, 255), border_rect, 1)

    def take_damage(self, damage):
        # Reduce the health by the damage amount
        self.health -= damage
        # Ensure health does not drop below 0
        if self.health < 0:
            self.health = 0

    def heal(self, amount):
        # Increase the health by the heal amount, but not above max health
        self.health = min(self.max_health, self.health + amount)