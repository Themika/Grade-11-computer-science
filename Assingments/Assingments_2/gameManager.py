import pygame
import sys

# Initialize pygame
pygame.init()

# Define Colors using the new palette
PRIMARY = (39, 26, 12)   
SECONDARY = (51, 36, 18) 
ACCENT = (18, 11, 4)     
BUTTON_COLOR = (136, 109, 64)  
TEXT_COLOR = (255, 255, 255)  
GREY = (169, 169, 169)   

# Set screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Manager")

# Font setup
font = pygame.font.SysFont("Helvetica", 24)
large_font = pygame.font.SysFont("Helvetica", 48)

# Load the background image
background = pygame.image.load('Assingments/Assingments_2/assets/Creepy-Cabin-Graphic-67803520-1.png')  # Ensure you have a background image named 'background_image.png'
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load the bouncing image (replace with the path to your PNG file)
image = pygame.image.load('Assingments/Assingments_2/assets/mptyxj3gnrra1-removebg-preview.png')
image = pygame.transform.scale(image, (100, 100))  # Resize image as needed

# Set initial position and speed for the image (slower speed)
image_x = 400
image_y = 300
image_dx = 2  
image_dy = 2  

class GameManager:
    def __init__(self):
        self.state = "main_menu"  # Tracks current screen (main_menu, game1, game2, game3)
        
        # Set initial position and speed for the image (slower speed)
        self.image_x = 400
        self.image_y = 300
        self.image_dx = 2  
        self.image_dy = 2  
        
        # Button properties (moved to bottom of screen)
        self.game1_button_rect = pygame.Rect(100, SCREEN_HEIGHT - 150, 250, 60)
        self.game2_button_rect = pygame.Rect(375, SCREEN_HEIGHT - 150, 250, 60)
        self.game3_button_rect = pygame.Rect(650, SCREEN_HEIGHT - 150, 250, 60)
        
        # Game loop
        self.running = True
        self.run()

    def run(self):
        """Main game loop."""
        while self.running:
            screen.fill(PRIMARY)  # Fill the screen with the primary background color
            screen.blit(background, (0, 0))  # Display the background image

            # Update image position to make it bounce
            self.image_x += self.image_dx
            self.image_y += self.image_dy

            # Bounce the image off screen edges
            if self.image_x <= 0 or self.image_x >= SCREEN_WIDTH - image.get_width():
                self.image_dx = -self.image_dx
            if self.image_y <= 0 or self.image_y >= SCREEN_HEIGHT - image.get_height():
                self.image_dy = -self.image_dy

            # Handle events
            self.handle_events()

            # Update UI based on the state
            if self.state == "main_menu":
                self.create_main_ui()
            elif self.state == "game1":
                self.create_game_ui("Mini Game 1", self.main_menu)
            elif self.state == "game2":
                self.create_game_ui("Mini Game 2", self.main_menu)
            elif self.state == "game3":
                self.create_game_ui("Mini Game 3", self.main_menu)

            # Always draw the image first so it appears behind the buttons
            mouse_pos = pygame.mouse.get_pos()
            if self.game1_button_rect.collidepoint(mouse_pos) or self.game2_button_rect.collidepoint(mouse_pos) or self.game3_button_rect.collidepoint(mouse_pos):
                # Move the image towards the button and draw behind it
                self.move_image_towards_button(mouse_pos)
            else:
                # If not hovering, keep bouncing the image
                screen.blit(image, (self.image_x, self.image_y))

            # Draw the buttons on top of the image
            pygame.display.flip()

    def move_image_towards_button(self, mouse_pos):
        """Move the image toward the button when hovering over it and scale it."""
        target_x = mouse_pos[0] - image.get_width() // 2  # Center the image on the button
        target_y = mouse_pos[1] - image.get_height() // 2

        # Smoothly move the image closer to the target position
        speed = 5  # Speed at which the face moves towards the button
        distance = pygame.math.Vector2(target_x - self.image_x, target_y - self.image_y).length()
        
        # Ease the image transition by decreasing speed as it approaches the button
        max_distance = 300  # Maximum distance before scaling
        scale_factor = 1 + min(distance / max_distance, 1)  # Smooth scale effect

        # Move the image towards the target position with easing
        if self.image_x < target_x:
            self.image_x += min(speed, target_x - self.image_x)
        elif self.image_x > target_x:
            self.image_x -= min(speed, self.image_x - target_x)

        if self.image_y < target_y:
            self.image_y += min(speed, target_y - self.image_y)
        elif self.image_y > target_y:
            self.image_y -= min(speed, self.image_y - target_y)

        # Scale the image based on distance
        scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), int(image.get_height() * scale_factor)))

        # Draw the image behind the button
        screen.blit(scaled_image, (self.image_x, self.image_y))

    def handle_events(self):
        """Handle all events like mouse clicks and quitting."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.on_click(event)
    
    def on_click(self, event):
        """Handle click events on buttons.""" 
        mouse_pos = event.pos
        if self.state == "main_menu":
            if self.game1_button_rect.collidepoint(mouse_pos):
                self.start_game1()
            elif self.game2_button_rect.collidepoint(mouse_pos):
                self.start_game2()
            elif self.game3_button_rect.collidepoint(mouse_pos):
                self.start_game3()
        elif self.state in ["game1", "game2", "game3"]:
            if self.back_button_rect.collidepoint(mouse_pos):
                self.main_menu()

    def create_main_ui(self):
        """Create the main menu UI.""" 
        # Title
        title_text = large_font.render("Game Manager", True, TEXT_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Buttons with hover effects
        self.draw_button(self.game1_button_rect, "Mini Game 1", BUTTON_COLOR)
        self.draw_button(self.game2_button_rect, "Mini Game 2", BUTTON_COLOR)
        self.draw_button(self.game3_button_rect, "Mini Game 3", BUTTON_COLOR)

    def draw_button(self, rect, text, color):
        """Draw a button with text on the screen and a hover effect.""" 
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, GREY, rect)  # Hover effect
        else:
            pygame.draw.rect(screen, color, rect)

        # Add rounded corners to buttons
        pygame.draw.rect(screen, color, rect, border_radius=20)

        # Centered text
        text_surface = font.render(text, True, TEXT_COLOR)
        screen.blit(text_surface, (rect.centerx - text_surface.get_width() // 2, rect.centery - text_surface.get_height() // 2))

    def create_game_ui(self, game_title, back_command):
        """Create a generic game UI."""        
        # Game title
        title_text = large_font.render(game_title, True, TEXT_COLOR)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Placeholder text
        placeholder_text = font.render("Game content goes here!", True, TEXT_COLOR)
        screen.blit(placeholder_text, (SCREEN_WIDTH // 2 - placeholder_text.get_width() // 2, 200))

        # Back button
        self.back_button_rect = pygame.Rect(375, SCREEN_HEIGHT - 150, 250, 60)
        self.draw_button(self.back_button_rect, "Back to Main Menu", BUTTON_COLOR)

    def start_game1(self):
        """Start Mini Game 1."""
        self.state = "game1"

    def start_game2(self):
        """Start Mini Game 2."""
        self.state = "game2"

    def start_game3(self):
        """Start Mini Game 3."""
        self.state = "game3"

    def main_menu(self):
        """Go back to the main menu."""
        self.state = "main_menu"

# Run the game manager
game_manager = GameManager()
pygame.quit()
sys.exit()


if __name__ == "__main__":
    game_manager = GameManager()
    pygame.quit()
    sys.exit()

