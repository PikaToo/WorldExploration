import pygame
from abstract_classes.entity import Entity       # enemies are entities 

class Enemy(Entity):

    # list of all enemies
    enemies = []

    def __init__(self, x_pos, y_pos, color, size, max_enemy_health, damage, gold, player, platform_list):
        super().__init__(x_pos, y_pos, size, color, 0, 0)   # x, y velocities start at 0
        self.max_health = max_enemy_health
        self.current_health = max_enemy_health
        self.color = color
        self.damage = damage
        self.counter = 0
        self.gold = gold
        self.player = player
        self.platform_list = platform_list
        
        Enemy.enemies.append(self)

    def apply_standard_x_movement(self):
        self.rect.x += self.x_velocity
        for platform in self.platform_list:
            if self.rect.colliderect(platform.rect):
                if self.x_velocity > 0:
                    self.rect.right = platform.rect.left
                if self.x_velocity < 0:
                    self.rect.left = platform.rect.right


    def apply_standard_y_movement(self):
        enemy_on_ground = False
        self.rect.y += self.y_velocity
        for platform in self.platform_list:  # same as for player, but no double jumps
            if self.rect.bottom == platform.rect.top \
                and self.rect.left in range (platform.rect.left - self.rect.width, platform.rect.right):
                enemy_on_ground = True
            if self.rect.colliderect(platform.rect):
                if self.y_velocity > 0:
                    self.rect.bottom = platform.rect.top
                    enemy_on_ground = True
                if self.y_velocity < 0:
                    self.rect.top = platform.rect.bottom
        if not enemy_on_ground:
            self.y_velocity += 0.6
        if enemy_on_ground:
            self.y_velocity = 0
    

    def draw_health_bar(self):
        # getting health bar rect
        bar_height = 5 + (self.max_health / 5)
        bar_x_pos = self.rect.x - 5
        bar_y_pos = self.rect.y - 2 - bar_height 
        bar_x_width = self.rect.width + 10
        bar_y_width = bar_height 

        back_bar = pygame.Rect(bar_x_pos, bar_y_pos, bar_x_width, bar_y_width)
        front_bar = pygame.Rect(bar_x_pos, bar_y_pos, bar_x_width * self.current_health / self.max_health, bar_y_width)

        # drawing
        pygame.draw.rect(Entity.window, (200, 200, 255), back_bar)
        pygame.draw.rect(Entity.window, (100, 0, 0), front_bar)        


    def delete(self):
        Enemy.enemies.remove(self)
