    import pygame
    import random
    import math

    # Initialize pygame
    pygame.init()

    # Screen dimensions
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Top-Down Shooter")

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Player class
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.speed = 5
            self.health = 100
            self.weapon = None

        def update(self, keys):
            if keys[pygame.K_w]:
                self.rect.y -= self.speed
            if keys[pygame.K_s]:
                self.rect.y += self.speed
            if keys[pygame.K_a]:
                self.rect.x -= self.speed
            if keys[pygame.K_d]:
                self.rect.x += self.speed

        def shoot(self):
            if self.weapon:
                self.weapon.shoot(self.rect.center)

    # Weapon classes
    class Weapon:
        def __init__(self, player):
            self.player = player

        def shoot(self, position):
            pass

    class Pistol(Weapon):
        def shoot(self, position):
            bullet = Bullet(position, (0, -10))
            all_sprites.add(bullet)
            bullets.add(bullet)

    class Shotgun(Weapon):
        def shoot(self, position):
            for angle in range(-30, 31, 15):
                rad = math.radians(angle)
                bullet = Bullet(position, (10 * math.sin(rad), -10 * math.cos(rad)))
                all_sprites.add(bullet)
                bullets.add(bullet)

    class MachineGun(Weapon):
        def shoot(self, position):
            for _ in range(3):
                bullet = Bullet(position, (0, -10))
                all_sprites.add(bullet)
                bullets.add(bullet)

    class LaserGun(Weapon):
        def shoot(self, position):
            bullet = Bullet(position, (0, -20))
            all_sprites.add(bullet)
            bullets.add(bullet)

    class RocketLauncher(Weapon):
        def shoot(self, position):
            bullet = Bullet(position, (0, -5), explosive=True)
            all_sprites.add(bullet)
            bullets.add(bullet)

    # Bullet class
    class Bullet(pygame.sprite.Sprite):
        def __init__(self, position, velocity, explosive=False):
            super().__init__()
            self.image = pygame.Surface((10, 10))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(center=position)
            self.velocity = velocity
            self.explosive = explosive

        def update(self):
            self.rect.x += self.velocity[0]
            self.rect.y += self.velocity[1]
            if self.rect.bottom < 0:
                self.kill()

    # Enemy classes
    class Enemy(pygame.sprite.Sprite):
        def __init__(self, position):
            super().__init__()
            self.image = pygame.Surface((50, 50))
            self.image.fill(WHITE)
            self.rect = self.image.get_rect(center=position)
            self.health = 50

        def update(self):
            pass

    class FastEnemy(Enemy):
        def update(self):
            self.rect.y += 5

    class TankEnemy(Enemy):
        def __init__(self, position):
            super().__init__(position)
            self.health = 200

    class ShooterEnemy(Enemy):
        def update(self):
            if random.random() < 0.01:
                bullet = Bullet(self.rect.center, (0, 10))
                all_sprites.add(bullet)
                enemy_bullets.add(bullet)

    class KamikazeEnemy(Enemy):
        def update(self, *args):
            self.rect.y += 3
            if self.rect.colliderect(player.rect):
                player.health -= 20
                self.kill()

    class TeleportEnemy(Enemy):
        def update(self):
            if random.random() < 0.01:
                self.rect.x = random.randint(0, WIDTH)
                self.rect.y = random.randint(0, HEIGHT // 2)

    # Initialize player and groups
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    # Game loop
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        keys = pygame.key.get_pressed()
        player.update(keys)
        all_sprites.update(keys)

        # Spawn enemies
        if random.random() < 0.02:
            enemy_type = random.choice([FastEnemy, TankEnemy, ShooterEnemy, KamikazeEnemy, TeleportEnemy])
            enemy = enemy_type((random.randint(0, WIDTH), 0))
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Check collisions
        for bullet in bullets:
            hits = pygame.sprite.spritecollide(bullet, enemies, True)
            for hit in hits:
                bullet.kill()

        for bullet in enemy_bullets:
            if pygame.sprite.collide_rect(bullet, player):
                player.health -= 10
                bullet.kill()

        # Draw everything
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()