import os
import json
import pygame
from button import Button

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

MAP_WIDTH = 3000
MAP_HEIGHT = 3000

scroll_speed = 5
scroll_x = 0
scroll_y = 0
current_tile = 0
current_page = 0
level = 0

scroll_left = False
scroll_right = False
scroll_up = False
scroll_down = False

screen = pygame.display.set_mode((SCREEN_WIDTH+SIDE_MARGIN, SCREEN_HEIGHT+LOWER_MARGIN))
pygame.display.set_caption('Level Generation')

GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('Futura', 25)

TILE_SIZE = 65  # Assuming each tile is 40x40 pixels
ROWS = MAP_HEIGHT // TILE_SIZE
MAX_COLS = MAP_WIDTH // TILE_SIZE
TILE_TYPES = 45

save_img = pygame.image.load("Tiny_Swords_Assets/Resources/Resources/SAVE.png").convert_alpha()
load_img = pygame.image.load("Tiny_Swords_Assets/Resources/Resources/LOAD.png").convert_alpha()

img_list = []
tile_categories = ['Ground\Green','Bridges','Decorations','Ground\Yellow']

for category in tile_categories:
    category_path = os.path.join('Animations', 'Levels', category.replace('\\', os.sep))
    for x in range(TILE_TYPES):
        img_path = os.path.join(category_path, f'Tilemap_Flat_{x}.png')
        print(f"Checking path: {img_path}")  # Debugging line
        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
            img_list.append(img)
        else:
            print(f"File does not exist: {img_path}")  # Debugging line
print(f"Total images loaded: {len(img_list)}")  # Debugging line

# Initialize world_data with three layers
world_data = []
for row in range(ROWS):
    r = [[-1, -1, -1] for _ in range(MAX_COLS)]
    world_data.append(r)

def draw_grid():
    # vertical lines
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, BLACK, (c * TILE_SIZE + scroll_x, 0), (c * TILE_SIZE + scroll_x, SCREEN_HEIGHT))
    # horizontal lines
    for c in range(ROWS + 1):
        pygame.draw.line(screen, BLACK, (0, c * TILE_SIZE + scroll_y), (SCREEN_WIDTH, c * TILE_SIZE + scroll_y))

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col) 
    screen.blit(img, (x, y))
def draw_bg():
    screen.fill(WHITE)
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDTH//2 + scroll_x, SCREEN_HEIGHT//2 + scroll_y, 50, 50))

save_button = Button(SCREEN_WIDTH-400, SCREEN_HEIGHT+25, save_img, 0.5)
load_button = Button(SCREEN_WIDTH -200, SCREEN_HEIGHT+25, load_img, 0.2)

def draw_buttons(page):
    button_list = []
    button_col = 0
    button_row = 0
    start_index = page * 15
    end_index = start_index + 15
    for i in range(start_index, min(end_index, len(img_list))):
        tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
        button_list.append(tile_button)
        button_col += 1
        if button_col == 3:
            button_row += 1
            button_col = 0
    return button_list

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile[0] >= 0:
                screen.blit(img_list[tile[0]], (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))
                print(f"Drew tile {tile[0]} at ({x}, {y})")  # Debugging line
            if tile[1] >= 0:
                screen.blit(img_list[tile[1]], (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))
                print(f"Drew tile {tile[1]} at ({x}, {y})")  # Debugging line
            if tile[2] >= 0:
                screen.blit(img_list[tile[2]], (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))
                print(f"Drew tile {tile[2]} at ({x}, {y})")  # Debugging line

run = True
while run:
    draw_bg()
    draw_grid()

    # scroll the map horizontally
    if scroll_left:
        scroll_x += scroll_speed
    if scroll_right:
        scroll_x -= scroll_speed
    # scroll the map vertically
    if scroll_up:
        scroll_y += scroll_speed
    if scroll_down:
        scroll_y -= scroll_speed

    # clamp the scrolling to the map boundaries
    scroll_x = max(min(scroll_x, 0), SCREEN_WIDTH - MAP_WIDTH)
    scroll_y = max(min(scroll_y, 0), SCREEN_HEIGHT - MAP_HEIGHT)
    
    pos = pygame.mouse.get_pos()
    x = (pos[0] - scroll_x) // TILE_SIZE
    y = (pos[1] - scroll_y) // TILE_SIZE
    if 0 <= x < MAX_COLS and 0 <= y < ROWS:
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
            if pygame.mouse.get_pressed()[0] == 1:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and keys[pygame.K_TAB]:
                    world_data[y][x][2] = current_tile
                elif keys[pygame.K_SPACE]:
                    world_data[y][x][1] = current_tile
                else:
                    world_data[y][x][0] = current_tile
                print(f"Placed tile {current_tile} at ({x}, {y})")  # Debugging line
            if pygame.mouse.get_pressed()[2] == 1:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE] and keys[pygame.K_TAB]:
                    world_data[y][x][2] = -1
                elif keys[pygame.K_SPACE]:
                    world_data[y][x][1] = -1
                else:
                    world_data[y][x][0] = -1
                print(f"Removed tile at ({x}, {y})")  # Debugging line

    draw_world()
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT, SCREEN_WIDTH + SIDE_MARGIN, LOWER_MARGIN))
    draw_text(f"Level: {level}", font, BLACK, SCREEN_WIDTH-800, SCREEN_HEIGHT+25)
    draw_text(f"Place tiles at differnt layers.\nSPACE for layer 2. SPACE and TAB for layer 3", font, BLACK, SCREEN_WIDTH-800, SCREEN_HEIGHT+50)
    
    if save_button.draw(screen):
        with open(f"maps/level{level}_data.json", mode='w') as f:
            json.dump(world_data, f)
    if load_button.draw(screen):
        with open(f"maps/level{level}_data.json", mode='r') as f:
            world_data = json.load(f)

    button_list = draw_buttons(current_page)
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count + current_page * 15
    pygame.draw.rect(screen, RED, button_list[current_tile % 15].rect, 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP:
                scroll_up = True
            if event.key == pygame.K_DOWN:
                scroll_down = True
            if event.key == pygame.K_a:
                current_page = max(current_page - 1, 0)
            if event.key == pygame.K_d:
                current_page = min(current_page + 1, (len(img_list) - 1) // 15)
            if event.key == pygame.K_w:
                level += 1
            if event.key == pygame.K_s and level > 0:
                level -= 1
            if event.key == pygame.K_j:
                for row in range(ROWS):
                    for col in range(MAX_COLS):
                        world_data[row][col][2] = current_tile

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
            if event.key == pygame.K_UP:
                scroll_up = False
            if event.key == pygame.K_DOWN:
                scroll_down = False

    pygame.display.update()

pygame.quit()