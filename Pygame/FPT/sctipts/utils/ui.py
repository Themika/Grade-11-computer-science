import pygame

class UI:
    def __init__(self, knight_face_size=(25, 35)):
        self.knight_face = pygame.image.load('UI/Faction/FACE_ID.png')  # Load the knight face image
        self.knight_face = pygame.transform.scale(self.knight_face, knight_face_size)
        self.archer_face = pygame.image.load('UI/Faction/Archer_Face.png')  # Load the archer face image
        self.archer_face = pygame.transform.scale(self.archer_face, (25, 25))
        self.knight_face_size = knight_face_size
        self.margin = 10  # Margin between faces
        self.grayscale_knight_face = None
        self.grayscale_archer_face = None

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
        knight_rows = 0
        archer_rows = 0

        # Calculate the number of rows for knights and archers
        for knight in selected_knights:
            if knight.type == 'knight':
                knight_rows = knight_index // 4 + 1
                knight_index += 1
            else:
                archer_rows = archer_index // 4 + 1
                archer_index += 1

        knight_index = 0
        archer_index = 0
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
            else:
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
            surface.blit(knight_face, (x, y))