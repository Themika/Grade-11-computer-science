import pygame 
class State:
    IDLE = 'idle'
    PATROL = 'patrol'
    ATTACK = 'attack'
class Knight(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.IDLE
        self.patrol_points = [(100, 100), (200, 200)]
        self.current_patrol_point = 0
        self.target = None

    def movement(self):
        if self.state == State.PATROL:
            self.patrol()
        elif self.state == State.ATTACK:
            self.chase_target()
    def draw(self, surface):
        pass
    def update(self):
        self.movement()

    def selection(self):
        pass

    def attack(self):
        pass

    def patrol(self):
        target_point = self.patrol_points[self.current_patrol_point]
        self.move_towards(target_point)
        if self.rect.center == target_point:
            self.current_patrol_point = (self.current_patrol_point + 1) % len(self.patrol_points)

    def chase_target(self):
        if self.target:
            self.move_towards(self.target.rect.center)

    def move_towards(self, target):
        dx, dy = target[0] - self.rect.centerx, target[1] - self.rect.centery
        dist = (dx**2 + dy**2) ** 0.5
        if dist != 0:
            dx, dy = dx / dist, dy / dist
        self.rect.x += dx * 2  # Adjust speed as necessary
        self.rect.y += dy * 2  # Adjust speed as necessary