import os
import time
import json
import pygame
import random

from utils.ui import UI
from utils.camera import Camera
from utils.menu import Menu

from allies.knight import Knight
from allies.archer import Archer
from allies.pawn import Pawn
from enemy.torch import Torch
from enemy.TNT import TNT
from enemy.barrel import Barrel

from utils.rps_manager import RPSManager

from buildings.House import House
from buildings.Castle import Castle
from buildings.Tower import Tower

from Resources.GoldMine import GoldMine
from Resources.Tree import Tree
from Resources.RawReasources.log import Log

# Initialize Pygame
pygame.init()
WINDOW_HEIGHT, WINDOW_WIDTH = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
display_surface.fill((70, 171, 176))  
pygame.display.set_caption("Protector of the Realm")

# Load the cursor image
cursor_image = pygame.image.load('Tiny_Swords_Assets/UI/Pointers/01.png')
cursor_image = pygame.transform.scale(cursor_image, (64, 64))
cursor_data = pygame.cursors.Cursor((0, 0), cursor_image)
pygame.mouse.set_cursor(cursor_data)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill('blue')
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.speed = 5
        

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.move_ip(0, self.speed)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.move_ip(0, -self.speed)


# Load level data
def load_level_data(level):
    with open(f"maps/level{level}_data.json", mode='r') as f:
        return json.load(f)

# Draw level
def draw_level(surface, level_data, img_list, scroll_x, scroll_y, TILE_SIZE=65):
    for y, row in enumerate(level_data):
        for x, tile in enumerate(row):
            if tile[0] >= 0 and tile[0] < len(img_list):
                surface.blit(img_list[tile[0]], (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))
            if tile[1] >= 0 and tile[1] < len(img_list):
                surface.blit(img_list[tile[1]], (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))
            if tile[2] >= 0 and tile[2] < len(img_list):
                surface.blit(img_list[tile[2]], (x * TILE_SIZE + scroll_x, y * TILE_SIZE + scroll_y))

# Draw grid
def draw_grid(surface, camera):
    start_x = max(0, camera.camera.x // 100 * 100)
    start_y = max(0, camera.camera.y // 100 * 100)
    end_x = min(2000, (camera.camera.x + WINDOW_WIDTH) // 100 * 100 + 100)
    end_y = min(2000, (camera.camera.y + WINDOW_HEIGHT) // 100 * 100 + 100)
    for x in range(start_x, end_x, 100):
        for y in range(start_y, end_y, 100):
            rect = pygame.Rect(x, y, 100, 100)
            adjusted_rect = rect.move(camera.camera.topleft)
            pygame.draw.rect(surface, (200, 200, 200), adjusted_rect, 1)

# Draw grid coordinates
def draw_grid_coordinates(surface, camera):
    font = pygame.font.SysFont(None, 24)
    start_x = max(0, camera.camera.x // 100 * 100)
    start_y = max(0, camera.camera.y // 100 * 100)
    end_x = min(2000, (camera.camera.x + WINDOW_WIDTH) // 100 * 100 + 100)
    end_y = min(2000, (camera.camera.y + WINDOW_HEIGHT) // 100 * 100 + 100)
    for x in range(start_x, end_x, 100):
        for y in range(start_y, end_y, 100):
            adjusted_x, adjusted_y = x + camera.camera.topleft[0], y + camera.camera.topleft[1]
            text_surface = font.render(f'({x}, {y})', True, (255, 255, 255))
            surface.blit(text_surface, (adjusted_x + 5, adjusted_y + 5))

# Spawn wave
def spawn_wave(wave, all_sprites, projectiles, houses, towers):
    corners = [(350, 350), (350, 1800), (1900, 350), (1900, 1800)]
    enemies_per_group = 1 * wave  # Start with 2 enemies per group and increase by 2 every wave
    for corner in corners:
        for _ in range(enemies_per_group):
            enemy_tnt = TNT(projectiles,level_data)
            enemy_tnt.rect.topleft = (corner[0] + random.randint(-50, 50), corner[1] + random.randint(-50, 50))
            all_sprites.add(enemy_tnt)
            barrel = Barrel()
            barrel.rect.topleft = (corner[0] + random.randint(-50, 50), corner[1] + random.randint(-50, 50))
            all_sprites.add(barrel)
                
            enemy_torch = Torch(level_data)
            enemy_torch.rect.topleft = (corner[0] + random.randint(-50, 50), corner[1] + random.randint(-50, 50))
            all_sprites.add(enemy_torch)

    for house in houses:
        house.update_construction_status(wave_ended=True)
        archer = Archer(level_data)
        house.spawn_archer(archer)
        all_sprites.add(archer)
        knight = Knight(level_data)
        house.spawn_knight(knight)
        all_sprites.add(knight)

    for tower in towers:
        if tower.wave_counter is None:
            tower.wave_counter = wave + 2
        if wave >= tower.wave_counter:
            tower.update_construction_status(wave_ended=True)

# Get nearest archer
def get_nearest_archer(tower, archers):
    nearest_archer = None
    min_distance = float('inf')
    for archer in archers:
        if not archer.on_tower:
            distance = ((archer.rect.centerx - tower.rect.centerx) ** 2 + (archer.rect.centery - tower.rect.centery) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_archer = archer
    return nearest_archer

# Initialize groups and variables
gold_mines = pygame.sprite.Group()
trees = pygame.sprite.Group()
reasources = pygame.sprite.Group()
logs = pygame.sprite.Group()
meats = pygame.sprite.Group()
golds = pygame.sprite.Group()
buildings = pygame.sprite.Group()

player = Player()
camera = Camera(WINDOW_HEIGHT, WINDOW_WIDTH,18000,720)
all_sprites = pygame.sprite.Group(player)
projectiles = pygame.sprite.Group()
houses = []
castles = []
towers = []
wave = 1
grace_period = 60
grace_period_start_time = None
rps_manager = RPSManager()
clock = pygame.time.Clock()
placing_building = False
building_to_place = None
placed_houses = []
place_house_next = True
targeted_trees = set()
level = 0
level_data = load_level_data(level)
img_list = []

ui = UI()
def heal_buildings(buildings):
    for building in buildings:
        building.health += 100
def heal_allies(allies):
    for ally in allies:
        ally.health += 50
# Load tile images
tile_categories = ['Ground/Green', 'Bridges', 'Decorations', 'Ground/Yellow', 'Ground/Water']
for category in tile_categories:
    category_path = os.path.join('Animations', 'Levels', category.replace('\\', os.sep))
    for x in range(50):
        img_path = os.path.join(category_path, f'Tilemap_Flat_{x}.png')
        if os.path.exists(img_path):
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (65, 65))
            img_list.append(img)

# Create a House instance
house = House(x=1500, y=500, finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Blue.png', construction_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Construction.png')
house.construction_status = "finished"
buildings.add(house)
houses.append(house)

Castle = Castle(x=2000, y=500, image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/Castle/Castle_Blue.png')
castles.append(Castle)
buildings.add(Castle)
def is_spawnable(x, y, level_data, TILE_SIZE=65):
    tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
    if 0 <= tile_y < len(level_data) and 0 <= tile_x < len(level_data[0]):
        # Check if the first index of the tile is 4
        if level_data[tile_y][tile_x][0] == 4:
            print(f"Water tile detected at ({tile_x}, {tile_y}): {level_data[tile_y][tile_x]}")
            return True
    return False

# Spawn trees and gold mines
for _ in range(250):
    while True:
        x = random.randint(0, 3000)
        y = random.randint(0, 3000)
        if is_spawnable(x, y, level_data):
            print(f"Spawning tree at ({x}, {y})")
            break
        else:
            print(f"Non-water tile detected at ({x}, {y}), looking for another spot")
    tree = Tree(x, y, logs, reasources)
    trees.add(tree)
    all_sprites.add(tree)

for _ in range(1):
    while True:
        x = random.randint(300, 1800)
        y = random.randint(1300, 2000)
        if not is_spawnable(x, y, level_data):
            print(f"Spawning gold mine at ({x}, {y})")
            break
        else:
            print(f"Water tile detected at ({x}, {y}), looking for another spot")
    gold_mine = GoldMine(x, y, golds, reasources)
    gold_mines.add(gold_mine)
    all_sprites.add(gold_mine)

# Spawn pawns, archers, and knights
for i in range(10):
    pawn = Pawn(level_data)
    all_sprites.add(pawn)

for _ in range(5):
    archer = Archer(tile_map=level_data)
    all_sprites.add(archer)

for _ in range(5):
    knight = Knight(level_data)
    all_sprites.add(knight)

spawn_wave(wave, all_sprites, projectiles, houses, towers)

# Main loop
running = True
counts = {'log': 0, 'gold': 0}

def update_counts(counts, log_change=0, gold_change=0):
    counts['log'] += log_change
    counts['gold'] += gold_change

# Main game loop
menu = Menu(display_surface, 1280, 720)
running = True
game_started = False
game_over = False
show_help = False
show_level_selection = False

while running:
    if not game_started:
        if show_help:
            menu.draw_help_page()
        elif show_level_selection:
            menu.draw_level_selection()
        else:
            menu.draw_menu()
        for event in pygame.event.get():
            action = menu.handle_events(event)
            if action == 'level_selection':
                show_level_selection = True
            elif action == 'level1':
                game_started = True
                show_level_selection = False
                # Initialize level 1
            elif action == 'level2':
                game_started = True
                show_level_selection = False
                # Initialize level 2
            elif action == 'help':
                show_help = True
            elif action == 'quit' or (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                running = False
            elif action == 'back':
                if show_help:
                    show_help = False
                elif show_level_selection:
                    show_level_selection = False
        continue

    if game_over:
        menu.draw_game_over()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                game_started = False
        continue

    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    alive_warriors = [allies for allies in all_sprites if isinstance(allies, Knight) or isinstance(allies, Archer) and allies.health > 0]
    alive_allies = [allies for allies in all_sprites if isinstance(allies, Knight) or isinstance(allies, Archer) and allies.health > 0 or isinstance(allies, Pawn) and allies.health > 0]
    alive_enemies = [enemy for enemy in all_sprites if isinstance(enemy, Torch) or isinstance(enemy, TNT) and enemy.health > 0 or isinstance(enemy, Barrel) and enemy.health > 0]
    alive_torch = [torch for torch in all_sprites if isinstance(torch, Torch) and torch.health > 0]
    alive_tnt = [tnt for tnt in all_sprites if isinstance(tnt, TNT) and tnt.health > 0]
    alive_pawns = [pawn for pawn in all_sprites if isinstance(pawn, Pawn) and pawn.health > 0]
    alive_knights = [ally for ally in all_sprites if isinstance(ally, Knight)]
    alive_archers = [ally for ally in all_sprites if isinstance(ally, Archer)]

    if len(alive_archers) == 0 and len(alive_knights) == 0:
        game_over = True
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_started = False
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
            rps_manager.handle_event(event, camera, alive_allies, alive_enemies)
            mouse_pos = pygame.mouse.get_pos()
            map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for tower in towers:
                    if tower.rect.collidepoint(map_pos):
                        if tower.unit_on_tower:
                            tower.remove_unit()
                        else:
                            nearest_archer = get_nearest_archer(tower, alive_archers)
                            if nearest_archer:
                                tower.place_unit(nearest_archer)
                                nearest_archer.on_tower = True
                        break
        if event.type == pygame.MOUSEWHEEL and grace_period_start_time is not None:
            if place_house_next:
                building_to_place = House(x=0, y=0, finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Blue.png', construction_image_path="Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Construction.png")
                if counts['log'] < 10 or counts['gold'] <= 1:
                    building_to_place.image.set_alpha(128)  # Greyed out
            else:
                building_to_place = Tower(x=0, y=0, width=100, height=200, construction_image_path="Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Construction.png", finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Blue.png', total_waves=wave)
                if counts['log'] < 20 or counts['gold'] < 5:
                    building_to_place.image.set_alpha(128)  # Greyed out
            place_house_next = not place_house_next
            placing_building = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if placing_building and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
                building_rect = pygame.Rect(map_pos[0], map_pos[1], building_to_place.rect.width, building_to_place.rect.height)
                collision = any(building.rect.colliderect(building_rect) for building in houses + towers)
                if not collision:
                    if isinstance(building_to_place, House) and counts['log'] >= 10 and counts['gold'] >= 1:
                        building_to_place.rect.topleft = map_pos
                        houses.append(building_to_place)
                        update_counts(counts, log_change=-10, gold_change=-1)
                        placed_houses.append((building_to_place, time.time()))
                    elif isinstance(building_to_place, Tower) and counts['log'] >= 20 and counts['gold'] >= 5:
                        building_to_place.rect.topleft = map_pos
                        towers.append(building_to_place)
                        update_counts(counts, log_change=-20, gold_change=-5)
                placing_building = False
    camera.update(player)
    draw_grid(display_surface, camera)
    draw_grid_coordinates(display_surface, camera)
    draw_level(display_surface, level_data, img_list, camera.camera.x, camera.camera.y)
    camera.custom_draw(display_surface, all_sprites)
    rps_manager.draw_marker(display_surface)
    rps_manager.draw_ui(display_surface, camera.camera.topleft)

    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(keys)
        elif isinstance(sprite, Archer):
            sprite.draw(display_surface, camera.camera.topleft)
            sprite.update(dt, alive_enemies)
        elif isinstance(sprite, Knight):
            sprite.update(dt, alive_enemies, alive_knights)
        elif isinstance(sprite, Pawn):
            sprite.update(dt, trees, targeted_trees, reasources, gold_mines, alive_pawns, (2000, 500), counts)
        elif isinstance(sprite, Torch):
            sprite.update(alive_knights,alive_archers,level_data,alive_enemies,alive_torch)
        elif isinstance(sprite, TNT):
            sprite.update(alive_knights,alive_archers,level_data,alive_enemies,alive_tnt)
        elif isinstance(sprite, Barrel):
            sprite.update(buildings,alive_warriors,level_data,alive_enemies)
    projectiles.update(dt, alive_knights, alive_archers)
    for projectile in projectiles:
        projectile.draw(display_surface, camera.camera.topleft)
    for tree in trees:
        tree.update()
        tree.draw(display_surface, camera.camera.topleft)
        if tree.health <= 0:
            log = tree.spawn_log()
            if log:
                logs.add(log)
                all_sprites.add(log)

    for log in logs:
        log.draw(display_surface, camera.camera.topleft)
        log.update()

    for gold_mine in gold_mines:
        gold_mine.update()
        gold_mine.draw(display_surface, camera.camera.topleft)
        if gold_mine.is_destroyed:
            for gold in gold_mine.gold_group:
                gold.draw(display_surface, camera.camera.topleft)
                gold.update()
        if gold_mine.gold_spawned:
            gold = gold_mine.spawn_gold()
            if gold:
                golds.add(gold)
                all_sprites.add(gold)

    for gold in gold_mines:
        gold.draw(display_surface, camera.camera.topleft)
        gold.update()

    for meat in meats:
        meat.draw(display_surface, camera.camera.topleft)
        meat.update()

    for house in houses:
        house.draw(display_surface, camera.camera.topleft)
    for caste in castles:
        Castle.draw(display_surface, camera.camera.topleft)

    for tower in towers:
        tower.draw(display_surface, camera.camera.topleft)
        tower.draw_tower(display_surface, camera.camera.topleft)

    if not alive_enemies:
        if grace_period_start_time is None:
            grace_period_start_time = time.time()
        current_time = time.time()
        if current_time - grace_period_start_time >= grace_period:
            heal_buildings(buildings)
            heal_allies(alive_allies)
            wave += 1
            spawn_wave(wave, all_sprites, projectiles, houses, towers)
            grace_period_start_time = None

    font = pygame.font.SysFont(None, 36)
    wave_text = font.render(f'Wave: {wave}', True, (255, 255, 255))
    display_surface.blit(wave_text, (10, 10))
    if grace_period_start_time is not None:
        grace_period_text = font.render(f'Grace Period: {max(0, int(grace_period - (time.time() - grace_period_start_time)))}s', True, (255, 255, 255))
        display_surface.blit(grace_period_text, (10, 50))

    if placing_building and building_to_place is not None:
        mouse_pos = pygame.mouse.get_pos()
        map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
        building_to_place.rect.topleft = map_pos
        if isinstance(building_to_place, House):
            building_to_place.draw(display_surface, camera.camera.topleft)
        else:
            building_to_place.draw_tower(display_surface, camera.camera.topleft)

    for house, placement_time in placed_houses[:]:
        if time.time() - placement_time >= 60:
            archer = Archer(level_data)
            knight = Knight(level_data)
            house.spawn_archer(archer)
            house.spawn_knight(knight)
            all_sprites.add(archer)
            all_sprites.add(knight)
            placed_houses.remove((house, placement_time))

    for house in houses:
        if house.ui_visible:
            house.show_spawn_ui(display_surface, pygame.font.SysFont(None, 24), camera.camera.topleft)
    ui.update_icons(display_surface, counts['log'], counts['gold'])
    pygame.display.update()

pygame.quit()