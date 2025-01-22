import pygame

class UI:
    def __init__(self, knight_face_size=(25, 35)):
        self.knight_face = self.load_and_scale_image('UI/Faction/FACE_ID.png', knight_face_size)
        self.archer_face = self.load_and_scale_image('UI/Faction/Archer_Face.png', (25, 25))
        self.pawn_face = self.load_and_scale_image('UI/Faction/Pawn_Face.png', (35, 25))

        self.knight_face_size = knight_face_size
        self.margin = 15  
        self.grayscale_knight_face = self.create_grayscale_image(self.knight_face)
        self.grayscale_archer_face = self.create_grayscale_image(self.archer_face)
        self.grayscale_pawn_face = self.create_grayscale_image(self.pawn_face)

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.Font("UI/Menu/Text/Press_Start_2P,Tiny5/Tiny5/Tiny5-Regular.ttf", 24)

    def load_and_scale_image(self, path, size):
        image = pygame.image.load(path)
        return pygame.transform.scale(image, size)

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
        self.archer_face = self.load_and_scale_image(new_face_path, self.knight_face_size)
        self.grayscale_archer_face = self.create_grayscale_image(self.archer_face)

    def draw_knight_faces(self, surface, selected_knights):
        knight_index = archer_index = pawn_index = 0
        knight_rows = archer_rows = pawn_rows = 0

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

        knight_index = archer_index = pawn_index = 0
        for knight in selected_knights:
            if knight.type == 'knight':
                row, col = divmod(knight_index, 4)
                x = 10 + col * (self.knight_face_size[0] + self.margin)
                y = 10 + row * (self.knight_face_size[1] + self.margin)
                knight_face = self.grayscale_knight_face if knight.has_reached else self.knight_face
                knight_index += 1
            elif knight.type == 'archer':
                row, col = divmod(archer_index, 4)
                x = 10 + col * (self.knight_face_size[0] + self.margin)
                y = 10 + (knight_rows + row) * (self.knight_face_size[1] + self.margin) + self.margin
                knight_face = self.grayscale_archer_face if knight.has_reached else self.archer_face
                archer_index += 1
            elif knight.type == 'pawn':
                row, col = divmod(pawn_index, 4)
                x = 10 + col * (self.knight_face_size[0] + self.margin)
                y = 10 + (knight_rows + archer_rows + row) * (self.knight_face_size[1] + self.margin) + 2 * self.margin
                knight_face = self.grayscale_pawn_face if knight.has_reached else self.pawn_face
                pawn_index += 1
            surface.blit(knight_face, (x, y))

    def update_icons(self, surface, log_count, gold_count):
        log_icon = self.load_and_scale_image('Tiny_Swords_Assets/Resources/Resources/W_Idle_(NoShadow)_ICON.png', (45, 25))
        log_text = self.font.render(f'{log_count}', True, (255, 255, 255))
        log_icon_rect = log_icon.get_rect(topright=(surface.get_width() - log_text.get_width() - 30, 40))
        log_text_rect = log_text.get_rect(topleft=(log_icon_rect.right + 5, 40))
        surface.blit(log_icon, log_icon_rect)
        surface.blit(log_text, log_text_rect)

        gold_icon = self.load_and_scale_image('Tiny_Swords_Assets/Resources/Resources/G_Idle_(NoShadow)_ICON.png', (25, 25))
        gold_text = self.font.render(f'{gold_count}', True, (255, 255, 255))
        gold_icon_rect = gold_icon.get_rect(topright=(surface.get_width() - gold_text.get_width() - 30, 10))
        gold_text_rect = gold_text.get_rect(topleft=(gold_icon_rect.right + 5, 10))
        surface.blit(gold_icon, gold_icon_rect)
        surface.blit(gold_text, gold_text_rect)
