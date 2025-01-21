import pygame

class UI:
    def __init__(self, knight_face_size=(25, 35)):
        self.knight_face = pygame.image.load('UI/Faction/FACE_ID.png')  # Load the knight face image
        self.knight_face = pygame.transform.scale(self.knight_face, knight_face_size)
        self.archer_face = pygame.image.load('UI/Faction/Archer_Face.png')  # Load the archer face image
        self.archer_face = pygame.transform.scale(self.archer_face, (25, 25))
        self.pawn_face = pygame.image.load('UI/Faction/Pawn_Face.png')  # Load the pawn face image
        self.pawn_face = pygame.transform.scale(self.pawn_face, (35, 25))

        self.knight_face_size = knight_face_size
        self.margin = 15  
        self.grayscale_knight_face = None
        self.grayscale_archer_face = None
        self.grayscale_pawn_face = None

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)

    def create_grayscale_image(self, image):
        grayscale_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        grayscale_image.fill((0, 0, 0, 0))
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, a = image.get_at((x, y))
                gray = (r + g + b) // 3
                grayscale_image.set_at((x, y), (gray, gray, gray, a))
        return grayscale_image

    def change_archer_face(self, new_face_path):
        self.archer_face = pygame.image.load(new_face_path)
        self.archer_face = pygame.transform.scale(self.archer_face, self.knight_face_size)
        self.grayscale_archer_face = None  # Reset grayscale archer face

    def draw_knight_faces(self, surface, selected_knights):
        knight_index = 0
        archer_index = 0
        pawn_index = 0
        knight_rows = 0
        archer_rows = 0
        pawn_rows = 0

        # Calculate the number of rows for knights, archers, and pawns
        for knight in selected_knights:
            if knight.type == 'knight':
                knight_rows = knight_index // 4 + 1
                knight_index += 1
            elif knight.type == 'archer':
                archer_rows = archer_index // 4 + 1
                archer_index += 1
            elif knight.type == 'pawn':
                pawn_rows = pawn_index // 4 + 1
                pawn_index += 1

        knight_index = 0
        archer_index = 0
        pawn_index = 0
        for knight in selected_knights:
            if knight.type == 'knight':
                row = knight_index // 4
                col = knight_index % 4
                x = 10 + col * (self.knight_face_size[0] + self.margin)
                y = 10 + row * (self.knight_face_size[1] + self.margin)
                knight_index += 1
                if knight.has_reached:
                    if self.grayscale_knight_face is None:
                        self.grayscale_knight_face = self.create_grayscale_image(self.knight_face)
                    knight_face = self.grayscale_knight_face
                else:
                    knight_face = self.knight_face
            elif knight.type == 'archer':
                row = archer_index // 4
                col = archer_index % 4
                x = 10 + col * (self.knight_face_size[0] + self.margin)
                y = 10 + (knight_rows + row) * (self.knight_face_size[1] + self.margin) + self.margin  # Adjust for knight rows and add margin
                archer_index += 1
                if knight.has_reached:
                    if self.grayscale_archer_face is None:
                        self.grayscale_archer_face = self.create_grayscale_image(self.archer_face)
                    knight_face = self.grayscale_archer_face
                else:
                    knight_face = self.archer_face
            elif knight.type == 'pawn':
                row = pawn_index // 4
                col = pawn_index % 4
                x = 10 + col * (self.knight_face_size[0] + self.margin)
                y = 10 + (knight_rows + archer_rows + row) * (self.knight_face_size[1] + self.margin) + 2 * self.margin  # Adjust for knight and archer rows and add margin
                pawn_index += 1
                if knight.has_reached:
                    if self.grayscale_pawn_face is None:
                        self.grayscale_pawn_face = self.create_grayscale_image(self.pawn_face)
                    knight_face = self.grayscale_pawn_face
                else:
                    knight_face = self.pawn_face
            surface.blit(knight_face, (x, y))

    def update_icons(self, surface, log_count, gold_count):
        # Draw log count
        log_icon = pygame.image.load('Tiny_Swords_Assets/Resources/Resources/W_Idle_(NoShadow)_ICON.png')
        log_icon = pygame.transform.scale(log_icon, (45, 25))
        log_text = self.font.render(f'{log_count}', True, (255, 255, 255))
        
        log_icon_rect = log_icon.get_rect()
        log_text_rect = log_text.get_rect()
        
        log_icon_rect.topright = (surface.get_width() - log_text_rect.width - 30, 40)
        log_text_rect.topleft = (log_icon_rect.right + 5, 40)
        
        surface.blit(log_icon, log_icon_rect)
        surface.blit(log_text, log_text_rect)

        # Draw gold count
        gold_icon = pygame.image.load('Tiny_Swords_Assets/Resources/Resources/G_Idle_(NoShadow)_ICON.png')
        gold_icon = pygame.transform.scale(gold_icon, (25, 25))
        gold_text = self.font.render(f'{gold_count}', True, (255, 255, 255))
        
        gold_icon_rect = gold_icon.get_rect()
        gold_text_rect = gold_text.get_rect()
        
        gold_icon_rect.topright = (surface.get_width() - gold_text_rect.width - 30, 10)
        gold_text_rect.topleft = (gold_icon_rect.right + 5, 10)
        
        surface.blit(gold_icon, gold_icon_rect)
        surface.blit(gold_text, gold_text_rect)