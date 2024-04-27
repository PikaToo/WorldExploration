import pygame
from gameObject import GameObject
from random import randint

# overlay manager : handles the health and level display UI elements
class HealthOverlay(GameObject):
    def __init__(self):
        self.damage_counter = 0 
        self.healing_counter = 0
        self.bar_rumble = 0

        self.current_health = 0
        self.max_health = 0

        self.damage = 0

    def take_damage(self, damage):
        if self.damage_counter <= 0 and self.healing_counter <= 0:
            self.damage_counter = 20
            self.damage = damage

    def restore_damage(self, damage):
        if self.damage_counter <= 0 and self.healing_counter <= 0:
            self.healing_counter = 20
            self.damage = damage

    def update(self, current_health, max_health):
        self.bar_rumble = 0

        # counting down timers and rumbling if so
        if self.damage_counter > 0:
            self.bar_rumble = randint(-3, 3)
            self.damage_counter -= 1
        
        if self.healing_counter > 0:
            self.bar_rumble = randint(-2, 2)
            self.healing_counter -= 1
        
        self.current_health = current_health
        self.max_health = max_health


    def display(self):
        # health circles
        for i in range(1, self.max_health + 1): 
            individual_rumble = self.bar_rumble * randint(-1, 1)      # rumble, off-sets all values
            x_pos = i*25 + 40
            y_pos = 585
            x_pos_rumble = x_pos + individual_rumble
            y_pos_rumble = y_pos + individual_rumble

            # background circle
            pygame.draw.circle(GameObject.window, (100, 50, 50), (x_pos, y_pos), 12)

            # taking damage
            if self.damage_counter > 0:

                # full inner circle
                if i <= self.current_health:
                    pygame.draw.circle(GameObject.window, (255, 80, 80), (x_pos_rumble, y_pos_rumble), 10)

                # shrinking inner circle where damage taken
                if self.current_health < i <= self.current_health + self.damage:
                    pygame.draw.circle(GameObject.window, (255, 50, 50), (x_pos_rumble, y_pos_rumble), 0.5 * self.damage_counter)
            
            # restoring damage
            elif self.healing_counter > 0:
                # full inner circle
                if i <= self.current_health - self.damage:
                    pygame.draw.circle(GameObject.window, (255, 80, 80), (x_pos_rumble, y_pos_rumble), 10)
                
                # enlarging inner circle where damage restored
                if self.current_health - self.damage < i <= self.current_health:
                    pygame.draw.circle(GameObject.window, (255, 50, 50), (x_pos, y_pos), 10 - (0.5 * self.healing_counter))

            # no damage: full inner circle if health present
            elif i <= self.current_health:
                pygame.draw.circle(GameObject.window, (255, 80, 80), (x_pos_rumble, y_pos_rumble), 10)
