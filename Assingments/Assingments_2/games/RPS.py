import pygame
import random
import sys
import os

# Ensure the utils directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from cutscene import CutScene, CutSceneManager

# Initialize pygame
pygame.init()

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set screen size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rock Paper Scissors")

# Load images
rock_img = pygame.image.load('Assingments/Assingments_2/assets/mptyxj3gnrra1-removebg-preview.png')
paper_img = pygame.image.load('Assingments/Assingments_2/assets/mptyxj3gnrra1-removebg-preview.png')
scissors_img = pygame.image.load('Assingments/Assingments_2/assets/mptyxj3gnrra1-removebg-preview.png')
background_img = pygame.image.load('Assingments/Assingments_2/assets/Creepy-Cabin-Graphic-67803520-1.png')

# Scale images
rock_img = pygame.transform.scale(rock_img, (150, 150))
paper_img = pygame.transform.scale(paper_img, (150, 150))
scissors_img = pygame.transform.scale(scissors_img, (150, 150))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Font setup
font = pygame.font.SysFont("Helvetica", 36)
large_font = pygame.font.SysFont("Helvetica", 72)

class RPS:
    def __init__(self):
        self.running = True
        self.player_choice = None
        self.computer_choice = None
        self.result = None
        self.thinking = False
        self.cutscene_manager = CutSceneManager(screen)
        self.cutscene = None

    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
            pygame.display.flip()

    def draw(self):
        screen.blit(background_img, (0, 0))  # Draw the background image
        self.draw_choices()
        self.draw_result()
        self.cutscene_manager.draw()

    def draw_choices(self):
        screen.blit(rock_img, (100, 400))
        screen.blit(paper_img, (325, 400))
        screen.blit(scissors_img, (550, 400))

    def draw_result(self):
        if self.thinking:
            thinking_text = font.render("Computer is thinking...", True, BLACK)
            screen.blit(thinking_text, (SCREEN_WIDTH // 2 - thinking_text.get_width() // 2, 50))
        elif self.result:
            result_text = large_font.render(self.result, True, BLACK)
            screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, 50))
            computer_choice_text = font.render(f"Computer chose: {self.computer_choice}", True, BLACK)
            screen.blit(computer_choice_text, (SCREEN_WIDTH // 2 - computer_choice_text.get_width() // 2, 150))

    def update(self):
        self.cutscene_manager.update()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.thinking:
                self.handle_click(event.pos)

    def handle_click(self, pos):
        if 100 <= pos[0] <= 250 and 400 <= pos[1] <= 550:
            self.player_choice = "rock"
        elif 325 <= pos[0] <= 475 and 400 <= pos[1] <= 550:
            self.player_choice = "paper"
        elif 550 <= pos[0] <= 700 and 400 <= pos[1] <= 550:
            self.player_choice = "scissors"
        if self.player_choice:
            self.thinking = True
            pygame.display.flip()
            self.start_cutscene()

    def start_cutscene(self):
        self.computer_choice = random.choice(["rock", "paper", "scissors"])
        self.determine_winner()
        scenes = [
            "You chose " + self.player_choice,
            "Computer is thinking...",
            "Computer chose " + self.computer_choice,
            self.result
        ]
        self.cutscene = CutScene("RPS_CutScene", scenes)
        self.cutscene_manager.start_cutscene(self.cutscene)
        self.thinking = False

    def determine_winner(self):
        if self.player_choice == self.computer_choice:
            self.result = "It's a tie!"
        elif (self.player_choice == "rock" and self.computer_choice == "scissors") or \
             (self.player_choice == "paper" and self.computer_choice == "rock") or \
             (self.player_choice == "scissors" and self.computer_choice == "paper"):
            self.result = "You win!"
        else:
            self.result = "You lose!"

if __name__ == "__main__":
    game = RPS()
    game.run()
    pygame.quit()
    sys.exit()