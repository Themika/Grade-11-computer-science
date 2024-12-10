import pygame 

class State:
    IDLE = 'idle'
    PATROL = 'patrol'
    RUN = 'run'
    ATTACK_1 = 'attack_1'
    ATTACK_2 = 'attack_2'
    ATTACK_3 = "attack_3"
    ATTACK_4 = "attack_4"
    ATTACK_5 = "attack_5"
    SEARCH = 'search'  # New search state
    WATCH = "watch"
    POS = "pos"

class Archer(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.state = State.PATROL 
        self.patrol_points = self.generate_random_patrol_points(5, 2000, 2000)  # Generate 5 random patrol points within a 2000x2000 area
        self.current_patrol_point = 0
        self.target_idle_time = 600000
        self.idle_duration_at_target = 6 
        
    def movement(self):
        pass
    def update(self):
        pass
    def selection(self):
        pass
    def attack(self):
        pass