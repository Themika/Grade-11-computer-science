import pygame
import random
import time
from utils.camera import Camera
from allies.knight import Knight
from allies.archer import Archer
from enemy.torch import Torch
from enemy.TNT import TNT
from utils.rps_manager import RPSManager
from buildings.House import House
from buildings.Tower import Tower

pygame.init()
WINDOW_HEIGHT, WINDOW_WIDTH = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
running = True
pygame.display.set_caption("Protector of the Realm")

# Load the cursor image
cursor_image = pygame.image.load('Tiny_Swords_Assets/UI/Pointers/01.png')
cursor_image = pygame.transform.scale(cursor_image, (64, 64))  # Scale the image if necessary
cursor_data = pygame.cursors.Cursor((0, 0), cursor_image)
pygame.mouse.set_cursor(cursor_data)

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

def draw_grid(surface, camera):
    for x in range(0, 2000, 100):
        for y in range(0, 2000, 100):
            rect = pygame.Rect(x, y, 100, 100)
            adjusted_rect = rect.move(camera.camera.topleft)
            pygame.draw.rect(surface, (200, 200, 200), adjusted_rect, 1)

def draw_grid_coordinates(surface, camera):
    font = pygame.font.SysFont(None, 24)
    for x in range(0, 2000, 100):
        for y in range(0, 2000, 100):
            adjusted_x, adjusted_y = x + camera.camera.topleft[0], y + camera.camera.topleft[1]
            text_surface = font.render(f'({x}, {y})', True, (255, 255, 255))
            surface.blit(text_surface, (adjusted_x + 5, adjusted_y + 5))

def spawn_wave(wave, all_sprites, projectiles, houses, towers):
    for _ in range(1 + wave * 1):  # Increase the number of enemies with each wave
        enemy_tnt = TNT(projectiles)
        enemy_tnt.rect.topleft = (random.randint(0, 500), random.randint(0, 500))
        all_sprites.add(enemy_tnt)
        
        enemy_torch = Torch()
        enemy_torch.rect.topleft = (random.randint(0, 500), random.randint(0, 500))
        all_sprites.add(enemy_torch)
        
    for house in houses:
        house.update_construction_status(wave_ended=True)
        for _ in range(2):  # Spawn 2 archers and 2 knights per house
            archer = Archer()
            house.spawn_archer(archer)
            all_sprites.add(archer)
            # knight = Knight()
            # house.spawn_knight(knight)
            # all_sprites.add(knight)
    for tower in towers:
        if tower.wave_counter is None:
            tower.wave_counter = wave + 2  # Set the wave counter to the current wave + 2
        if wave >= tower.wave_counter:
            tower.update_construction_status(wave_ended=True)


def get_nearest_archer(tower, archers):
    nearest_archer = None
    min_distance = float('inf')
    for archer in archers:
        if not archer.on_tower:  # Check if the archer is not on a tower
            distance = ((archer.rect.centerx - tower.rect.centerx) ** 2 + (archer.rect.centery - tower.rect.centery) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                nearest_archer = archer
    return nearest_archer


player = Player()
camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
all_sprites = pygame.sprite.Group(player)
projectiles = pygame.sprite.Group()
houses = []
towers = []

# Create a House instance
house = House(x=1000, y=500, finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Blue.png',construction_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Construction.png')

# Add the house to the all_sprites group and houses list
all_sprites.add(house)
houses.append(house)

for _ in range(20):
    archer = Archer()
    house.spawn_archer(archer)
    all_sprites.add(archer)

for _ in range(50):
    knight = Knight()
    house.spawn_knight(knight)
    all_sprites.add(knight)

wave = 1
grace_period = 60  # 3 minutes in seconds
grace_period_start_time = None
spawn_wave(wave, all_sprites, projectiles, houses,towers)

rps_manager = RPSManager()
clock = pygame.time.Clock()

# Variable to track if a house or tower is being placed
placing_building = False
building_to_place = None
placed_houses = []

# Flag to alternate between house and tower
place_house_next = True

while running:
    dt = clock.tick(60) / 1000  # Amount of seconds between each loop
    keys = pygame.key.get_pressed()
    alive_allies = [allies for allies in all_sprites if isinstance(allies, Knight) or isinstance(allies, Archer) and allies.health > 0]
    alive_enemies = [enemy for enemy in all_sprites if isinstance(enemy, Torch) or isinstance(enemy, TNT) and enemy.health > 0]
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and grace_period_start_time is not None:
            print("TOWER")
            for tower in towers:
                if tower.rect.collidepoint(map_pos):
                    nearest_archer = get_nearest_archer(tower, alive_allies)
                    if nearest_archer:
                        tower.place_unit(nearest_archer)
                        break
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP and grace_period_start_time is None:
            rps_manager.handle_event(event, camera, alive_allies, alive_enemies)
            mouse_pos = pygame.mouse.get_pos()
            map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
        elif event.type == pygame.MOUSEWHEEL and grace_period_start_time is not None:
            # Start placing a house or tower if the scroll wheel is used during the grace period
            placing_building = True
            if place_house_next:
                building_to_place = House(x=0, y=0, finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Blue.png', construction_image_path="Tiny_Swords_Assets/Factions/Knights/Buildings/House/House_Construction.png")
            else:
                building_to_place = Tower(x=0, y=0, width=100, height=200, construction_image_path="Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Construction.png" ,finished_image_path='Tiny_Swords_Assets/Factions/Knights/Buildings/Tower/Tower_Blue.png',total_waves=wave)
            place_house_next = not place_house_next  # Alternate the flag
        elif event.type == pygame.MOUSEBUTTONUP:
            if placing_building and event.button == 1:
                # Place the building on left mouse button release
                mouse_pos = pygame.mouse.get_pos()
                map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
                building_to_place.rect.topleft = map_pos
                all_sprites.add(building_to_place)
                if isinstance(building_to_place, House):
                    houses.append(building_to_place)
                    placed_houses.append((building_to_place, time.time()))  # Track the house placement time
                else:
                    towers.append(building_to_place)
                placing_building = False
                building_to_place = None
    # Update the camera
    camera.update(player)
    # Render the scene
    display_surface.fill('darkgray')
    draw_grid(display_surface, camera)
    draw_grid_coordinates(display_surface, camera)
    camera.custom_draw(display_surface, all_sprites)
    
    rps_manager.draw_marker(display_surface)
    rps_manager.draw_ui(display_surface, camera.camera.topleft)  # Draw the UI elements last to ensure they are on top

    
    alive_knights = [ally for ally in all_sprites if isinstance(ally, Knight)]
    alive_archers = [ally for ally in all_sprites if isinstance(ally, Archer)]
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            sprite.update(keys)
        elif isinstance(sprite, Archer):
            sprite.draw(display_surface, camera.camera.topleft)
            sprite.update(dt, alive_enemies)
        elif isinstance(sprite, Knight):
            sprite.update(dt, alive_enemies, alive_knights)
        elif isinstance(sprite, TNT) or isinstance(sprite, Torch):
            sprite.update(alive_knights, alive_archers)

    # Update and draw projectiles
    projectiles.update(dt, alive_knights, alive_archers)
    for projectile in projectiles:
        projectile.draw(display_surface, camera.camera.topleft)

    # Check if all enemies are dead
    if not alive_enemies:
        if grace_period_start_time is None:
            grace_period_start_time = time.time()
        current_time = time.time()
        if current_time - grace_period_start_time >= grace_period:
            wave += 1
            spawn_wave(wave, all_sprites, projectiles, houses,towers)
            grace_period_start_time = None

    # Display wave and grace period timer
    font = pygame.font.SysFont(None, 36)
    wave_text = font.render(f'Wave: {wave}', True, (255, 255, 255))
    display_surface.blit(wave_text, (10, 10))
    if grace_period_start_time is not None:
        grace_period_text = font.render(f'Grace Period: {max(0, int(grace_period - (time.time() - grace_period_start_time)))}s', True, (255, 255, 255))
        display_surface.blit(grace_period_text, (10, 50))

    # Draw the building being placed
    if placing_building and building_to_place is not None:
        mouse_pos = pygame.mouse.get_pos()
        map_pos = (mouse_pos[0] - camera.camera.x, mouse_pos[1] - camera.camera.y)
        building_to_place.rect.topleft = map_pos
        if isinstance(building_to_place, House):
            building_to_place.draw(display_surface)
        else:
            building_to_place.draw_tower(display_surface)

    # Check if it's time to spawn knights and archers for placed houses
    for house, placement_time in placed_houses[:]:
        if time.time() - placement_time >= 60:  # 1 minute delay
            for _ in range(2):
                archer = Archer()
                house.spawn_archer(archer)
                all_sprites.add(archer)
                # knight = Knight()
                # house.spawn_knight(knight)
                # all_sprites.add(knight)
            placed_houses.remove((house, placement_time))

    pygame.display.update()

pygame.quit()
