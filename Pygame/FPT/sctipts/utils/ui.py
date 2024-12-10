import pygame

class UI:
    def __init__(self, knight_face_size=(25, 35)):
        self.knight_face = pygame.image.load('UI/Faction/FACE_ID.png')  # Load the knight face image
        self.knight_face = pygame.transform.scale(self.knight_face, knight_face_size)
        self.knight_face_size = knight_face_size
        self.margin = 10  # Margin between knight faces

    def create_grayscale_image(self, image):
        grayscale_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        grayscale_image.fill((0, 0, 0, 0))
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                r, g, b, a = image.get_at((x, y))
                gray = (r + g + b) // 3
                grayscale_image.set_at((x, y), (gray, gray, gray, a))
        return grayscale_image

    def draw_knight_faces(self, surface, selected_knights):
        for index, knight in enumerate(selected_knights):
            row = index // 4
            col = index % 4
            x = 10 + col * (self.knight_face_size[0] + self.margin)
            y = 10 + row * (self.knight_face_size[1] + self.margin)
            if knight.has_reached:
                knight_face = self.create_grayscale_image(self.knight_face)
            else:
                knight_face = self.knight_face
            surface.blit(knight_face, (x, y))