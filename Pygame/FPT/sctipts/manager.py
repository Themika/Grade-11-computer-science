import os
import time
import json
import pygame
import random
from utils.camera import Camera
from allies.knight import Knight
from allies.archer import Archer
from allies.pawn import Pawn
from enemy.torch import Torch
from enemy.TNT import TNT
from utils.rps_manager import RPSManager
from buildings.House import House
from Resources.GoldMine import GoldMine
from buildings.Tower import Tower
from Resources.Tree import Tree
from Resources.RawReasources.log import Log
from Resources.Sheep import Sheep

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
    for _ in range(1 + wave * 2):
        enemy_tnt = TNT(projectiles, level_data)
        enemy_tnt.rect.topleft = (random.randint(250, 600), random.randint(250, 500))
        all_sprites.add(enemy_tnt)

        enemy_torch = Torch(level_data) 
        enemy_torch.rect.topleft = (random.randint(200, 500), random.randint(200, 500))
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
sheeps = pygame.sprite.Group()
trees = pygame.sprite.Group()
reasources = pygame.sprite.Group()
logs = pygame.sprite.Group()
meats = pygame.sprite.Group()
golds = pygame.sprite.Group()
player = Player()
camera = Camera(WINDOW_HEIGHT, WINDOW_WIDTH)
all_sprites = pygame.sprite.Group(player)
projectiles = pygame.sprite.Group()
houses = []
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
houses.append(house)

# Spawn trees and gold mines
for _ in range(20):
    x = random.randint(0, 2000)
    y = random.randint(0, 2000)
    tree = Tree(x, y, logs, reasources)
    trees.add(tree)
    all_sprites.add(tree)

for _ in range(1):
    x = random.randint(0, 2000)
    y = random.randint(0, 2000)
    gold_mine = GoldMine(x, y, golds, reasources)
    gold_mines.add(gold_mine)
    all_sprites.add(gold_mine)

# Spawn pawns, archers, and knights
for i in range(10):
    pawn = Pawn()
    all_sprites.add(pawn)

num_sheep = 20
sheep_per_group = 5
group_leader_count = 0
group_leader = None

def is_water_tile(x, y, level_data, TILE_SIZE=65):
    tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
    if 0 <= tile_y < len(level_data) and 0 <= tile_x < len(level_data[0]):
        return level_data[tile_y][tile_x][0] == 3  # Assuming 3 represents water tiles
    return False

for i in range(num_sheep):
    while True:
        x, y = random.randint(1500, 3000), random.randint(0, 3000)
        if not is_water_tile(x, y, level_data):
            break
    if i % sheep_per_group == 0:
        group_leader = Sheep(x, y, sheeps, meats, reasources, level_data)
        group_leader_count += 1
        sheeps.add(group_leader)
        all_sprites.add(group_leader)
    else:
        sheep = Sheep(x, y, sheeps, meats, reasources, level_data, group_leader=group_leader)
        sheeps.add(sheep)
        all_sprites.add(sheep)


for _ in range(5):
    archer = Archer(level_data)
    all_sprites.add(archer)

for _ in range(10):
    knight = Knight(level_data)
    all_sprites.add(knight)

spawn_wave(wave, all_sprites, projectiles, houses, towers)

# Main loop
running = True
while running:
    dt = clock.tick(60) / 1000
    keys = pygame.key.get_pressed()
    alive_allies = [allies for allies in all_sprites if isinstance(allies, Knight) or isinstance(allies, Archer) and allies.health > 0 or isinstance(allies, Pawn) and allies.health > 0]
    alive_enemies = [enemy for enemy in all_sprites if isinstance(enemy, Torch) or isinstance(enemy, TNT) and enemy.health > 0]
    alive_pawns = [pawn for pawn in all_sprites if isinstance(pawn, Pawn) and pawn.health > 0]
    alive_knights = [ally for ally in all_sprites if isinstance(ally, Knight)]
    alive_archers = [ally for ally in all_sprites if isinstance(ally, Archer)]
    not_fully_constructed_buildings = [building for building in houses + towers if not building.is_fully_constructed()]

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
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
                for house in houses:
                    if house.rect.collidepoint(map_pos):
                        house.ui_visible = not house.ui_visible
                        if house.ui_visible:
                            house.show_spawn_ui(display_surface, pygame.font.SysFont(None, 24), camera.camera.topleft)
                        else:
                            house.ui_visible = False
            for house in houses:
                if house.ui_visible:
                    house.handle_click(mouse_pos)
        if event.type == pygame.MOUSEWHEEL and grace_period_start_time is not None:
            placing_building = True
            if place_house_next:
                building_to_place = House(x=0, y=0, finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Blue.png', construction_image_path="Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Construction.png")
            else:
                building_to_place = Tower(x=0, y=0, width=100, height=200, construction_image_path="Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Construction.png", finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Blue.png', total_waves=wave)
            place_house_next = not place_house_next
        elif event.type == pygame.MOUSEBUTTONUP:
            if placing_building and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
                building_to_place.rect.topleft = map_pos
                if isinstance(building_to_place, House):
                    houses.append(building_to_place)
                    placed_houses.append((building_to_place, time.time()))
                else:
                    towers.append(building_to_place)
                placing_building = False
                building_to_place = None

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
            sprite.update(dt, trees, targeted_trees, reasources, gold_mines, alive_pawns, sheeps)
        elif isinstance(sprite, TNT) or isinstance(sprite, Torch):
            sprite.update(alive_knights, alive_archers)

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

    for sheep in sheeps:
        sheep.update()
        if sheep.health <= 0:
            sheep.spawn_meat()
            sheep.kill()

    for meat in meats:
        meat.draw(display_surface, camera.camera.topleft)
        meat.update()

    for house in houses:
        house.draw(display_surface, camera.camera.topleft)

    for tower in towers:
        tower.draw_tower(display_surface, camera.camera.topleft)

    if not alive_enemies:
        if grace_period_start_time is None:
            grace_period_start_time = time.time()
        current_time = time.time()
        if current_time - grace_period_start_time >= grace_period:
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

    pygame.display.update()

pygame.quit()