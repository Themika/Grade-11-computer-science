import pygame
import pygame.gfxdraw

class Menu:
    def __init__(self, display_surface, window_width, window_height):
        self.display_surface = display_surface
        self.window_width = window_width
        self.window_height = window_height
        
        # Load pixel art font
        self.font = pygame.font.Font('UI/Menu/Text/Press_Start_2P,Tiny5/Press_Start_2P/PressStart2P-Regular.ttf', 32)
        self.font_title = pygame.font.Font('UI/Menu/Text/Press_Start_2P,Tiny5/Press_Start_2P/PressStart2P-Regular.ttf', 64)
        self.small_font = pygame.font.Font('UI/Menu/Text/Press_Start_2P,Tiny5/Tiny5/Tiny5-Regular.ttf', 18)  # Smaller font for descriptions
        
        # Load background images
        self.behind_background_image = pygame.image.load('UI/Menu/Carved_3Slides.png')
        self.behind_background_image = pygame.transform.scale(self.behind_background_image, (window_width, 200))
        self.behind_background_rect = self.behind_background_image.get_rect(midtop=(window_width // 2, 75))  # Adjusted position
        self.background_image = pygame.image.load('UI/Menu/BACKGROUND.png')
        self.background_image = pygame.transform.scale(self.background_image, (window_width, window_height))

        # Create a semi-transparent overlay
        self.overlay = pygame.Surface((window_width, window_height))
        self.overlay.set_alpha(128)  # Adjust alpha value for transparency

        # Title
        self.title_text = self.font_title.render('Protector of the \n      Realm', True, (255, 255, 255))
        self.title_shadow = self.font_title.render('Protector of the \n      Realm', True, (0, 0, 0))
        self.title_rect = self.title_text.get_rect(center=(window_width // 2, window_height // 4))

        # Play button
        self.play_button_text = self.font.render('Play', True, (255, 255, 255))
        self.play_button_shadow = self.font.render('Play', True, (0, 0, 0))
        self.play_button_rect = self.play_button_text.get_rect(center=(window_width // 2, window_height // 2))
        
        # Help button
        self.help_button_text = self.font.render('Help', True, (255, 255, 255))
        self.help_button_shadow = self.font.render('Help', True, (0, 0, 0))
        self.help_button_rect = self.help_button_text.get_rect(center=(window_width // 2, window_height // 2 + 100))
        
        # Manual button
        self.manual_button_text = self.font.render('Manual', True, (255, 255, 255))
        self.manual_button_shadow = self.font.render('Manual', True, (0, 0, 0))
        self.manual_button_rect = self.manual_button_text.get_rect(center=(window_width // 2, window_height // 2 + 200))

        # Quit button
        self.quit_button_text = self.font.render('Quit', True, (255, 255, 255))
        self.quit_button_shadow = self.font.render('Quit', True, (0, 0, 0))
        self.quit_button_rect = self.quit_button_text.get_rect(center=(window_width // 2, window_height // 2 + 300))
    
        
        # Game over text
        self.game_over_text = self.font.render('Game Over', True, (255, 0, 0))
        self.game_over_shadow = self.font.render('Game Over', True, (0, 0, 0))
        
        # Back button
        self.back_button_text = self.small_font.render('Back', True, (255, 255, 255))
        self.back_button_shadow = self.small_font.render('Back', True, (0, 0, 0))
        self.back_button_rect = self.back_button_text.get_rect(center=(window_width // 2, window_height // 2 + 250))
        self.back_button_large_rect = self.back_button_rect.inflate(20, 20)  # Increase clickable area
        
        # Level buttons
        self.level1_button_text = self.font.render('Level 1', True, (255, 255, 255))
        self.level1_button_shadow = self.font.render('Level 1', True, (0, 0, 0))
        self.level1_button_rect = self.level1_button_text.get_rect(center=(window_width // 2, window_height // 2 - 100))
        
        self.level2_button_text = self.font.render('Level 2', True, (255, 255, 255))
        self.level2_button_shadow = self.font.render('Level 2', True, (0, 0, 0))
        self.level2_button_rect = self.level2_button_text.get_rect(center=(window_width // 2, window_height // 2 + 100))
        
        # Scroll bar attributes
        self.scroll_bar_rect = pygame.Rect(0, window_height - 20, window_width, 20)
        self.handle_width = window_width // 4
        self.handle_rect = pygame.Rect(0, window_height - 20, self.handle_width, 20)
        self.dragging = False
        self.scroll_position = 0

        # Load card images
        self.card_images = [
            pygame.image.load('UI/Menu/WASD.png'),
            pygame.image.load('UI/Menu/LEFT_CLICK.png'),
            pygame.image.load('UI/Menu/RIGH_CLICK.png'),
            pygame.image.load('UI/Menu/MOUSE_WHEEL.png'),
            pygame.image.load('UI/Menu/Lore.png')  # New lore image
        ]
        self.manual_images = [
            pygame.image.load('Animations/Goblins/Torch/Blue/Idle/Torch_Blue_Idle_1.png'),
            pygame.image.load('Animations/Goblins/TNT/Blue/Idle/TNT_Blue_Idle_1.png'),
            pygame.image.load('Animations/Goblins/Bomb/RUN/Barrel_Blue_Run_5.png'),
            pygame.image.load('Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Blue.png'),
            pygame.image.load('Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Blue.png'),
            pygame.image.load('Tiny_Swords_Assets/Factions/Knights/Buildings/Castle/Castle_Blue.png')
        ]

        # Store original button positions
        self.original_play_button_rect = self.play_button_rect.copy()
        self.original_help_button_rect = self.help_button_rect.copy()
        self.original_quit_button_rect = self.quit_button_rect.copy()
        self.original_manual_button_rect = self.manual_button_rect.copy()

        # Play button enabled flag
        self.play_button_enabled = True

        # Current menu state
        self.current_menu = 'main'

    def draw_menu(self):
        # Draw the background image
        self.display_surface.blit(self.background_image, (0, 0))
        # Apply a semi-transparent overlay
        self.display_surface.blit(self.overlay, (0, 0))

        # Draw the title with a shadow effect
        self.display_surface.blit(self.behind_background_image, self.behind_background_rect.topleft)
        self.display_surface.blit(self.title_shadow, self.title_rect.move(2, 2))
        self.display_surface.blit(self.title_text, self.title_rect)

        # Draw the buttons with shadows and hover effects
        self.draw_button(self.play_button_rect, self.play_button_shadow, self.play_button_text)
        self.draw_button(self.help_button_rect, self.help_button_shadow, self.help_button_text)
        self.draw_button(self.quit_button_rect, self.quit_button_shadow, self.quit_button_text)
        self.draw_button(self.manual_button_rect, self.manual_button_shadow, self.manual_button_text)

        # Update the display to show the changes
        pygame.display.update()

    def draw_button(self, button_rect, button_shadow, button_text):
        # Draw the button shadow
        self.display_surface.blit(button_shadow, button_rect.move(2, 2))
        # Draw the button text
        self.display_surface.blit(button_text, button_rect)

        # Check if the mouse is hovering over the button
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            # Create a grey transparent overlay
            overlay = pygame.Surface(button_rect.size, pygame.SRCALPHA)
            overlay.fill((128, 128, 128, 128))  # Grey transparent overlay
            # Draw the overlay on top of the button
            self.display_surface.blit(overlay, button_rect.topleft)

    def draw_game_over(self):
        # Draw the background images and overlay
        self.display_surface.blit(self.behind_background_image, (0, 0))
        self.display_surface.blit(self.background_image, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))  # Apply overlay

        # Draw the game over text with a shadow effect
        self.display_surface.blit(self.game_over_shadow, (self.window_width // 2 - self.game_over_shadow.get_width() // 2 + 2, self.window_height // 2 - self.game_over_shadow.get_height() // 2 + 2))
        self.display_surface.blit(self.game_over_text, (self.window_width // 2 - self.game_over_text.get_width() // 2, self.window_height // 2 - self.game_over_text.get_height() // 2))

        # Update the display to show the changes
        pygame.display.update()

    def draw_help_page(self):
        self.display_surface.blit(self.behind_background_image, (0, 0))
        self.display_surface.blit(self.background_image, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))  # Apply overlay
        
        instructions = [
            {"image": self.card_images[0], "description": "Use WASD for Movement."},
            {"image": self.card_images[1], "description": "1.) Right click to move unit\n2.) Place Archers on towers\n3.) Place houses & Towers"},
            {"image": self.card_images[2], "description": "1.) Hold left to select multiple units\n2.) Click on them to select singular."},
            {"image": self.card_images[3], "description": "Scroll to select between towers or houses."},
            {"image": self.card_images[4], "description": "The realm is under attack by the goblins.\nAs the last king, you must defend it at all costs.\n1.) Protect your castle \n2.)Protect your Archer and Knights"}  # New lore description
        ]
        
        card_width = self.window_width // 3
        card_height = self.window_height // 2
        card_spacing = 5
        total_width = card_width * len(instructions) + card_spacing * (len(instructions) - 1)
        
        # Load card background image
        card_background_image = pygame.image.load('Tiny_Swords_Assets/UI/Buttons/Button_Hover_9Slides.png')
        
        # Create a surface for the instructions
        instructions_surface = pygame.Surface((total_width, card_height), pygame.SRCALPHA)
        
        for i, card in enumerate(instructions):
            # Adjust card width for the fourth card
            if i == 4:
                adjusted_card_width = card_width * 1.05
            else:
                adjusted_card_width = card_width
            
            # Scale the card background image
            scaled_card_background_image = pygame.transform.scale(card_background_image, (adjusted_card_width, card_height))
            
            # Create a card surface
            card_surface = pygame.Surface((adjusted_card_width, card_height), pygame.SRCALPHA)
            card_surface.blit(scaled_card_background_image, (0, 0))

            # Image
            image = pygame.transform.scale(card["image"], (adjusted_card_width // 2, card_height // 2))
            image_rect = image.get_rect(center=(adjusted_card_width // 2, card_height // 4 + 20))  # Move image 20 pixels lower
            card_surface.blit(image, image_rect)

            # Description
            description_lines = card["description"].split(". ")
            for j, line in enumerate(description_lines):
                desc_text = self.small_font.render(line, True, (80, 80, 80))
                desc_y = image_rect.bottom + 20 + j * 20  # Adjusted line spacing for smaller font
                card_surface.blit(desc_text, (adjusted_card_width // 2 - desc_text.get_width() // 2, desc_y))
            
            instructions_surface.blit(card_surface, (i * (card_width + card_spacing), 0))
        
        # Blit the instructions surface with scroll position
        self.display_surface.blit(instructions_surface, (-self.scroll_position, self.window_height // 4))
        
        # Scroll bar
        self.scroll_bar_rect.y = self.window_height - 20  # Move scroll bar back to bottom
        self.scroll_bar_rect.height = 10  # Make scroll bar height smaller
        pygame.draw.rect(self.display_surface, (200, 200, 200), self.scroll_bar_rect, border_radius=5)  
        pygame.draw.rect(self.display_surface, (100, 100, 100), self.handle_rect, border_radius=5)  
        
        # Back button
        self.back_button_rect.topleft = (10, 10)  # Move back button to top left
        self.back_button_large_rect = self.back_button_rect.inflate(20, 20)  # Update larger rect
        self.display_surface.blit(self.back_button_shadow, self.back_button_rect.move(2, 2))
        self.display_surface.blit(self.back_button_text, self.back_button_rect)

        pygame.display.update()

    def draw_manual_page(self):
        self.display_surface.blit(self.behind_background_image, (0, 0))
        self.display_surface.blit(self.background_image, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))  # Apply overlay

        # Title for Goblin Types section
        goblin_title_text = self.small_font.render('Goblin Types', True, (255, 255, 255))
        goblin_title_shadow = self.small_font.render('Goblin Types', True, (0, 0, 0))
        goblin_title_rect = goblin_title_text.get_rect(center=(100,75))
        self.display_surface.blit(goblin_title_shadow, goblin_title_rect.move(2, 2))
        self.display_surface.blit(goblin_title_text, goblin_title_rect)

        # First section: Images beside descriptions
        manual_items_section1 = [
            {"image": self.manual_images[0], "description": "Torch Goblins: Torch Goblins are melee-focused \ncreatures of chaos,\ndriven by their love for destruction and mischief.\n Armed with flaming torches, \nthey charge into battle with reckless abandon."},
            {"image": self.manual_images[1], "description": "TNT Goblins: Tnt Goblins are the brainiacs of goblin society—though \nthat's not saying much.\nKnown for their cunning and craftiness, \nthey excel at creating and using explosive devices.\nThese goblins are skilled engineers in their own chaotic way."},
            {"image": self.manual_images[2], "description": "Barrel Goblins: Barrel Goblins are a peculiar breed, \nknown for their cowardly demeanor\n yet packing an unexpected punch. These goblins are often seen hiding \ninside large wooden barrels,\nwhich they use both as armor and as a weapon"},
        ]

        for i, item in enumerate(manual_items_section1):
            # Additional image
            background_image_image = pygame.image.load('Tiny_Swords_Assets/UI/Buttons/Button_Hover.png')
            background_image_image = pygame.transform.scale(background_image_image, (150, 150))
            background_image_image_rect = background_image_image.get_rect(topleft=(25, 100 + i * 120))
            self.display_surface.blit(background_image_image, background_image_image_rect)

            image = pygame.transform.scale(item["image"], (100, 100))
            image_rect = image.get_rect(topleft=(50, 100 + i * 120))
            self.display_surface.blit(image, image_rect)

            background_image_image = pygame.image.load('UI/Menu/Carved_3Slides.png')
            background_image_image = pygame.transform.scale(background_image_image, (600, 150))
            background_image_image_rect = background_image_image.get_rect(topleft=(150, 100 + i * 120))
            self.display_surface.blit(background_image_image, background_image_image_rect)
            description_lines = item["description"].split("\n")
            for j, line in enumerate(description_lines):
                text_surface = self.small_font.render(line, True, (255, 255, 255))
                self.display_surface.blit(text_surface, (200, 120 + i * 120 + j * 20))

        # Title for Building Types section
        manual_items_section2 = [
            {"image": self.manual_images[3], "description": "Towers (Gold) 5 Wood(10): \nProvides defense \nadvantages to the archers"},
            {"image": self.manual_images[4], "description": "Houses (Gold) 1 Wood(5): \nHouses provide more troops"},
            {"image": self.manual_images[5], "description": "Castles: \nCastles are the heart \nof your kingdom. \nProtect them at all costs."},
        ]

        y_offset = 500  # Vertical position for the second section
        x_spacing = 300  # Horizontal spacing between the two items
        # Draw the second section
        for i, item in enumerate(manual_items_section2):
            x_offset = 100 + i * x_spacing  # Adjust horizontal position
            image = pygame.transform.scale(item["image"], (100, 100))
            image_rect = image.get_rect(midtop=(x_offset, y_offset))  
            self.display_surface.blit(image, image_rect)

            description_lines = item["description"].split("\n")
            for j, line in enumerate(description_lines):
                text_surface = self.small_font.render(line, True, (255, 255, 255))
                self.display_surface.blit(text_surface, (x_offset - 50, y_offset + 110 + j * 20))  
        # Title for Game Objective section
        manual_items_section3 = [
            "The realm is under attack by the goblins.",
            "As the last king, you must defend it at all costs.",
            "1.) Protect your castle",
            "2.) Protect your Archer and Knights",
            "3.) Use resources wisely to build defenses",
            "4.) Strategize to outsmart the goblin hordes",
            "5.) Remember, the fate of the realm rests \non your shoulders."
        ]

        y_offset = 100  # Vertical position for the third section
        x_offset = 850   # Horizontal position for the text on the right side
        # Draw the third section
        for i, line in enumerate(manual_items_section3):
            text_surface = self.small_font.render(line, True, (255, 255, 255))
            self.display_surface.blit(text_surface, (x_offset, y_offset + i * 30))  # Adjust line spacing

        # Back button
        self.back_button_rect.topleft = (10, 10)  # Move back button to top left
        self.back_button_large_rect = self.back_button_rect.inflate(20, 20)  # Update larger rect
        self.display_surface.blit(self.back_button_shadow, self.back_button_rect.move(2, 2))
        self.display_surface.blit(self.back_button_text, self.back_button_rect)

        pygame.display.update()

    def draw_level_selection(self):
        # Draw the background images and overlay
        self.display_surface.blit(self.behind_background_image, (0, 0))
        self.display_surface.blit(self.background_image, (0, 0))
        self.display_surface.blit(self.overlay, (0, 0))  # Apply overlay

        bar_width = self.window_width * 2 // 3
        bar_height = 100  # Increased height for more space
        bar_color = (50, 50, 50)
        bar_spacing = 50  # Increased spacing

        if self.current_menu != 'help':
            # Draw Level 1 bar
            level1_bar_rect = pygame.Rect(self.window_width // 2 - bar_width // 2, self.window_height // 2 - bar_height - bar_spacing, bar_width, bar_height)
            pygame.draw.rect(self.display_surface, bar_color, level1_bar_rect, border_radius=10)
            pygame.draw.rect(self.display_surface, (255, 255, 255), level1_bar_rect, 2, border_radius=10)  # Add border
            self.level1_button_rect = self.level1_button_text.get_rect(center=level1_bar_rect.center)
            self.display_surface.blit(self.level1_button_shadow, self.level1_button_rect.move(2, 2))
            self.display_surface.blit(self.level1_button_text, self.level1_button_rect)

        # Draw the back button
        self.back_button_rect.topleft = (10, 10)  # Move back button to top left
        self.back_button_large_rect = self.back_button_rect.inflate(20, 20)  # Update larger rect
        self.display_surface.blit(self.back_button_shadow, self.back_button_rect.move(2, 2))
        self.display_surface.blit(self.back_button_text, self.back_button_rect)

        pygame.display.update()

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.help_button_rect.collidepoint(event.pos):
                self.move_buttons_off_screen()
                self.current_menu = 'help'
                return 'help'
            elif self.play_button_enabled and self.play_button_rect.collidepoint(event.pos):
                self.current_menu = 'level_selection'
                return 'level_selection'
            elif self.quit_button_rect.collidepoint(event.pos):
                return 'quit'
            elif self.manual_button_rect.collidepoint(event.pos):
                self.move_buttons_off_screen()
                self.current_menu = 'manual'
                return 'manual'
            elif self.back_button_large_rect.collidepoint(event.pos):  # Check collision with larger rect
                if self.current_menu == 'help' or self.current_menu == 'manual':
                    self.move_buttons_back()
                    self.current_menu = 'main'
                    return 'back_to_main'
                else:
                    self.move_buttons_back()
                    self.current_menu = 'main'
                    return 'back'
            elif self.level1_button_rect.collidepoint(event.pos) and self.current_menu != 'help':
                return 'level1'
            elif self.level2_button_rect.collidepoint(event.pos) and self.current_menu != 'help':
                return 'level2'
            elif self.scroll_bar_rect.collidepoint(event.pos):
                self.dragging = True
                self.mouse_x_offset = event.pos[0] - self.handle_rect.x
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                new_x = event.pos[0] - self.mouse_x_offset
                new_x = max(0, min(new_x, self.window_width - self.handle_width))
                self.handle_rect.x = new_x
                self.scroll_position = (new_x / (self.window_width - self.handle_width)) * (self.window_width * 2 - self.window_width)
        return None

    def move_buttons_off_screen(self):
        # Disable play button and move all buttons off screen
        self.play_button_enabled = False
        self.play_button_rect.center = (self.window_width * 2, self.window_height * 2)
        self.help_button_rect.topleft = (self.window_width * 2, self.window_height * 2)
        self.quit_button_rect.topleft = (self.window_width * 2, self.window_height * 2)
        self.manual_button_rect.topleft = (self.window_width * 2, self.window_height * 2)

    def move_buttons_back(self):
        # Enable play button and move all buttons back to original positions
        self.play_button_enabled = True
        self.play_button_rect = self.original_play_button_rect.copy()
        self.help_button_rect = self.original_help_button_rect.copy()
        self.quit_button_rect = self.original_quit_button_rect.copy()
        self.manual_button_rect = self.original_manual_button_rect.copy()