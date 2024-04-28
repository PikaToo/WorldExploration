from abstract_classes.enemy import Enemy
from abstract_classes.gameObject import GameObject
from bullet import Bullet
from random import randint

class Harmer(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (200, 200, 255), 25, 20, 1, 25, player, platform_list)
        self.player.exit_status = False

    def move(self):
        self.apply_standard_x_movement()
        self.apply_standard_y_movement()
        
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
            Bullet(self.rect.x + 9, self.rect.y + 9, randint(-5, 5), -5, "enemy", 12, 0.3, self.damage)
        if self.counter == 110:                 # reset
            self.counter = 0
        
        self.counter += 1
        
    def delete(self):
        self.player.exit_status = True
        GameObject.boss_statuses.harmer = False
        Enemy.enemies.remove(self)
