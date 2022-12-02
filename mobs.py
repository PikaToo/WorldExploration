import pygame
import random
import math


class Mob:
    def __init__(self, enemy):
        self.rect = enemy[0]
        self.acceleration = enemy[1]
        self.counter = enemy[2]
        self.ai = enemy[3]
        self.healths = enemy[4]
        self.color = enemy[5]
        self.boss_status = enemy[6]

        self.gold = 0
        self.fired = False
        self.fire_info = (0, 0, 0, 0, 0, 0, 0)

        self.other = enemy[7]       # used for some enemies that need other values retained

        m = 0
        if self.boss_status != -1:
            m = self.rect.width
        bar_height = 5 + (self.healths[1] / 5)
        bar_position = (self.rect.x - 5 - m, self.rect.y - bar_height - 2 - (m/4))
        bar_span = (self.rect.width + 10 + (2*m), bar_height + (m/4))
        bar_percent = (self.healths[0] / self.healths[1])
        back_color = (200, 200, 255)
        front_color = (100, 0, 0)
        self.bar = bar_position, bar_span, bar_percent, back_color, front_color

        self.gold = 1
        if self.ai == "Target" or self.ai == "Follower" or self.ai == "Icey Follower":
            pass
        if self.ai == "Bird" or self.ai == "Shooter" or self.ai == "Cold Bird":
            self.gold = 2
        if self.ai == "Pewer (Cannon)":
            self.gold = 3
        if self.ai == "Harmer":
            self.gold = 25

        if not -40 < self.rect.x < 1200 or not -40 < self.rect.y < 600:
            self.healths[0] -= 1

    def movement(self, player_rect, platforms):
        # enemy movement based on AI

        if self.ai == "Target":  # target is the first enemy (and a boss). does nothing, is a demonstration
            pass

        if self.ai == "Follower":
            sight_range = 350
            min_x = self.rect.x - sight_range
            max_x = self.rect.x + self.rect.width + sight_range
            if self.counter > 0 and player_rect.x in range(min_x, max_x):
                if self.rect.x < player_rect.x and self.acceleration[0] < 2:
                    self.acceleration[0] += 0.1
                if self.rect.x > player_rect.x and self.acceleration[0] > -2:
                    self.acceleration[0] -= 0.1
            else:
                self.acceleration[0] = 0

        if self.ai == "Shooter":
            if self.counter > 60:
                x_diff = player_rect[0] - self.rect.x
                y_diff = player_rect[1] - self.rect.y

                if not (abs(x_diff) + abs(y_diff)) == 0:  # first making sure no divide by 0 error

                    x_vector = x_diff / (abs(x_diff) + abs(y_diff))  # getting how much of x is in x + y
                    y_vector = y_diff / (abs(x_diff) + abs(y_diff))  # getting how much of y is in x + y
                    self.fired = True
                    self.fire_info = self.rect.x + 9, self.rect.y + 9, x_vector * 20, y_vector * 20, "enemy", 12, 0
                self.counter = 0

        if self.ai == "Bird":
            self.rect.y += self.acceleration[1]
            for platform in platforms:  # unique bounce-wall gravity
                if self.rect.colliderect(platform[0]):
                    if self.acceleration[1] < 0:
                        self.rect.top = platform[0].bottom
                        self.acceleration[1] = 0
                        self.acceleration[0] *= 0.5
                    if self.acceleration[1] > 0:
                        self.rect.bottom = platform[0].top
                        self.acceleration[1] = -10

            x_diff = player_rect.x - self.rect.x                # moving towards player
            y_diff = player_rect.y - self.rect.y
            if not (abs(x_diff) + abs(y_diff)) == 0 and self.counter > -40:  # first making sure no divide by 0 error
                x_vector = x_diff / (abs(x_diff) + abs(y_diff))  # getting how much of x is in x + y
                y_vector = y_diff / (abs(x_diff) + abs(y_diff))  # getting how much of y is in x + y

                self.acceleration[0] += x_vector / 2            # moving by vector
                self.acceleration[1] += y_vector / 2
                if self.acceleration[0] > 5:                    # terminal velocities
                    self.acceleration[0] = 5
                if self.acceleration[0] < -5:
                    self.acceleration[0] = -5
                if self.acceleration[1] > 5:
                    self.acceleration[1] = 5
                if self.acceleration[1] < -5:
                    self.acceleration[1] = -5

        if self.ai == "Harmer":
            if -5 < self.counter < 0:                       # initial movement
                self.acceleration[0] += 2
            if self.rect.x >= 1140 or self.rect.x <= 35:    # bouncing off sides
                self.acceleration[0] *= -4
                self.acceleration[1] = -20
            if self.acceleration[0] > 8:                    # terminal velocities
                self.acceleration[0] -= 1
            if self.acceleration[0] < -8:
                self.acceleration[0] += 1
            if self.counter > 100:                          # shooting
                self.fired = True
                self.fire_info = self.rect.x + 9, self.rect.y + 9, random.randint(-5, 5), -5, "enemy", 12, 0.3
            if self.counter == 110:                 # reset
                self.counter = 0

        if self.ai == "Icey Follower":
            if self.counter > 0:
                if self.rect.x < player_rect.x and self.acceleration[0] < 6:
                    self.acceleration[0] += 0.2
                if self.rect.x > player_rect.x and self.acceleration[0] > -6:
                    self.acceleration[0] -= 0.2
            else:
                self.acceleration[0] = 0
        
        if self.ai == "Cold Bird":
            if self.counter == -1:                          # initial movement
                x = random.randint(0, 1)
                if x == 0:
                    x = -1
                self.acceleration[0] = 4*x
            if self.counter == 100:                          # shooting
                self.fired = True
                self.fire_info = self.rect.x + 9, self.rect.y + 9, 0, 0, "enemy", 12, 0.3
                self.counter = 0

            # x-movement
            self.rect.x += self.acceleration[0]
            for platform in platforms:
                if self.rect.colliderect(platform[0]):
                    if self.acceleration[0] > 0:
                        self.rect.right = platform[0].left
                        self.acceleration[0] = -4
                if self.rect.colliderect(platform[0]):  # checks again to avoid double-trigger
                    if self.acceleration[0] < 0:
                        self.rect.left = platform[0].right
                        self.acceleration[0] = 4

            # y-movement (gravity + flapping)
            self.rect.y += self.acceleration[1]
            flapping = self.other
            if self.acceleration[1] > 3:
                flapping = True
            if self.acceleration[1] < -3:
                flapping = False
            if flapping:
                self.acceleration[1] -= 0.5
            if not flapping:
                self.acceleration[1] += 0.3
            self.other = flapping

            # y-movement (collisions)
            for platform in platforms:
                if self.rect.colliderect(platform[0]):
                    if self.acceleration[1] > 0:
                        self.rect.bottom = platform[0].top
                    if self.acceleration[1] < 0:
                        self.rect.top = platform[0].bottom
                        self.acceleration[1] = 10


        if self.ai == "Pewer (Cannon)":
            if self.counter > 120:
                self_pos_x = self.rect.x + 20
                player_x = self_pos_x + 10
                player_x_distance = player_rect[0] - player_x
                self_pos_y = self.rect.y + 20 
                player_y = player_rect[1] - 10
                player_y_distance = player_y - self_pos_y
                
                # initial x velocity based on distance away.
                x_vector = (player_x_distance/60)
                
                # done using suvat, u = (0.5at^2 - s)/t
                y_vector = (player_y_distance-540)/60
                
                # bullets still always some off. probably due to pygame rounding and some calculation
                # errors on my side.

                self.fired = True
                self.fire_info = self.rect.x + 10, self.rect.y + 10, x_vector, y_vector, "enemy", 20, 0.3
                self.counter = 0
            
        # default x-movement
        if self.ai != "Cold Bird":
            self.rect.x += self.acceleration[0]
            for platform in platforms:
                if self.rect.colliderect(platform[0]):
                    if self.acceleration[0] > 0:
                        self.rect.right = platform[0].left
                    if self.acceleration[0] < 0:
                        self.rect.left = platform[0].right

        # default y-movement
        if self.ai != "Bird" and self.ai != "Cold Bird":  # normal gravity + collision
            enemy_on_ground = False
            self.rect.y += self.acceleration[1]
            for platform in platforms:  # same as for player, but no double jumps
                if self.rect.bottom == platform[0].top \
                    and self.rect.left in range (platform[0].left - self.rect.width, platform[0].right):
                    enemy_on_ground = True
                if self.rect.colliderect(platform[0]):
                    if self.acceleration[1] > 0:
                        self.rect.bottom = platform[0].top
                        enemy_on_ground = True
                    if self.acceleration[1] < 0:
                        self.rect.top = platform[0].bottom
            if not enemy_on_ground:
                self.acceleration[1] += 0.6
            if enemy_on_ground:
                self.acceleration[1] = 0

        self.counter += 1
