import pygame
import random
from entity import Entity       # enemies are entities 
from bullet import Bullet       # enemies can make bullets

class Enemy(Entity):

    # list of all enemies
    enemies = []

    def __init__(self, x_pos, y_pos, color, size, counter, enemy_ai, enemy_health, boss, other, damage):
        super().__init__(x_pos, y_pos, size, color, 0, 0)   # x, y velocities start at 0
        self.counter = counter
        self.ai = enemy_ai
        self.max_health = enemy_health
        self.current_health = enemy_health
        self.color = color
        self.boss = boss
        self.other = other
        self.damage = damage

        self.gold = 0
        if self.ai == "Target" or self.ai == "Follower" or self.ai == "Icey Follower":
            self.gold = 1
        if self.ai == "Bird" or self.ai == "Shooter" or self.ai == "Cold Bird":
            self.gold = 2
        if self.ai == "Pewer (Cannon)":
            self.gold = 3
        if self.ai == "Harmer":
            self.gold = 25
        
        Entity.enemies.append(self)

    def move(self, player_rect, platform_list):
        # enemy movement based on AI

        if self.ai == "Target":  # target is the first enemy (and a boss). does nothing, is a demonstration
            pass

        if self.ai == "Follower":
            sight_range = 350
            min_x = self.rect.x - sight_range
            max_x = self.rect.x + self.rect.width + sight_range
            if self.counter > 0 and player_rect.x in range(min_x, max_x):
                if self.rect.x < player_rect.x and self.x_velocity < 2:
                    self.x_velocity += 0.1
                if self.rect.x > player_rect.x and self.x_velocity > -2:
                    self.x_velocity -= 0.1
            else:
                self.x_velocity = 0

        if self.ai == "Shooter":
            if self.counter > 60:
                x_diff = player_rect.x - self.rect.x
                y_diff = player_rect.y - self.rect.y

                if not (abs(x_diff) + abs(y_diff)) == 0:  # first making sure no divide by 0 error

                    x_vector = x_diff / (abs(x_diff) + abs(y_diff))  # getting how much of x is in x + y
                    y_vector = y_diff / (abs(x_diff) + abs(y_diff))  # getting how much of y is in x + y
                    Bullet(self.rect.x + 9, self.rect.y + 9, x_vector * 20, y_vector * 20, "enemy", 12, 0, self.damage)
                
                self.counter = 0

        if self.ai == "Bird":
            self.rect.y += self.y_velocity
            for platform in platform_list:  # unique bounce-wall gravity
                if self.rect.colliderect(platform.rect):
                    if self.y_velocity < 0:
                        self.rect.top = platform.rect.bottom
                        self.y_velocity = 0
                        self.x_velocity *= 0.5
                    if self.y_velocity > 0:
                        self.rect.bottom = platform.rect.top
                        self.y_velocity = -10

            x_diff = player_rect.x - self.rect.x                # moving towards player
            y_diff = player_rect.y - self.rect.y
            if not (abs(x_diff) + abs(y_diff)) == 0 and self.counter > -40:  # first making sure no divide by 0 error
                x_vector = x_diff / (abs(x_diff) + abs(y_diff))  # getting how much of x is in x + y
                y_vector = y_diff / (abs(x_diff) + abs(y_diff))  # getting how much of y is in x + y

                self.x_velocity += x_vector / 2            # moving by vector
                self.y_velocity += y_vector / 2
                if self.x_velocity > 5:                    # terminal velocities
                    self.x_velocity = 5
                if self.x_velocity < -5:
                    self.x_velocity = -5
                if self.y_velocity > 5:
                    self.y_velocity = 5
                if self.y_velocity < -5:
                    self.y_velocity = -5

        if self.ai == "Harmer":
            if -5 < self.counter < 0:                       # initial movement
                self.x_velocity += 2
            if self.rect.x >= 1140 or self.rect.x <= 35:    # bouncing off sides
                self.x_velocity *= -4
                self.y_velocity = -20
            if self.x_velocity > 8:                    # terminal velocities
                self.x_velocity -= 1
            if self.x_velocity < -8:
                self.x_velocity += 1
            if self.counter > 100:                          # shooting
                Bullet(self.rect.x + 9, self.rect.y + 9, random.randint(-5, 5), -5, "enemy", 12, 0.3, self.damage)
            if self.counter == 110:                 # reset
                self.counter = 0

        if self.ai == "Icey Follower":
            if self.counter > 0:
                if self.rect.x < player_rect.x and self.x_velocity < 6:
                    self.x_velocity += 0.2
                if self.rect.x > player_rect.x and self.x_velocity > -6:
                    self.x_velocity -= 0.2
            else:
                self.x_velocity = 0
        
        if self.ai == "Cold Bird":
            if self.counter == -1:                          # initial movement
                x = random.randint(0, 1)
                if x == 0:
                    x = -1
                self.x_velocity = 4*x
            if self.counter == 100:                          # shooting
                Bullet(self.rect.x + 9, self.rect.y + 9, 0, 0, "enemy", 12, 0.3, self.damage)
                self.counter = 0

            # x-movement
            self.rect.x += self.x_velocity
            for platform in platform_list:
                if self.rect.colliderect(platform.rect):
                    if self.x_velocity > 0:
                        self.rect.right = platform.rect.left
                        self.x_velocity = -4
                if self.rect.colliderect(platform.rect):  # checks again to avoid double-trigger
                    if self.x_velocity < 0:
                        self.rect.left = platform.rect.right
                        self.x_velocity = 4

            # y-movement (gravity + flapping)
            self.rect.y += self.y_velocity
            flapping = self.other
            if self.y_velocity > 3:
                flapping = True
            if self.y_velocity < -3:
                flapping = False
            if flapping:
                self.y_velocity -= 0.5
            if not flapping:
                self.y_velocity += 0.3
            self.other = flapping

            # y-movement (collisions)
            for platform in platform_list:
                if self.rect.colliderect(platform.rect):
                    if self.y_velocity > 0:
                        self.rect.bottom = platform.rect.top
                    if self.y_velocity < 0:
                        self.rect.top = platform.rect.bottom
                        self.y_velocity = 10


        if self.ai == "Pewer (Cannon)":
            if self.counter > 120:
                self_pos_x = self.rect.x + 20
                player_x = self_pos_x + 10
                player_x_distance = player_rect.x - player_x
                self_pos_y = self.rect.y + 20 
                player_y = player_rect.y - 10
                player_y_distance = player_y - self_pos_y
                
                # initial x velocity based on distance away.
                x_vector = (player_x_distance/60)
                
                # done using suvat, u = (0.5at^2 - s)/t
                y_vector = (player_y_distance-540)/60
                
                # bullets still always some off. probably due to pygame rounding and some calculation
                #   errors on my side.
                Bullet(self.rect.x + 10, self.rect.y + 10, x_vector, y_vector, "enemy", 20, 0.3, self.damage)
                self.counter = 0
            
        # default x-movement
        if self.ai != "Cold Bird":
            self.rect.x += self.x_velocity
            for platform in platform_list:
                if self.rect.colliderect(platform.rect):
                    if self.x_velocity > 0:
                        self.rect.right = platform.rect.left
                    if self.x_velocity < 0:
                        self.rect.left = platform.rect.right

        # default y-movement
        if self.ai != "Bird" and self.ai != "Cold Bird":  # normal gravity + collision
            enemy_on_ground = False
            self.rect.y += self.y_velocity
            for platform in platform_list:  # same as for player, but no double jumps
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

        self.counter += 1
    
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
        Entity.enemies.remove(self)
