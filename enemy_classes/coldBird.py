from enemy import Enemy
from bullet import Bullet
from random import randint

class ColdBird(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (200, 200, 255), 30, 6, 1, 2, player, platform_list)

    def move(self):
        if self.counter == -1:                          # initial movement
            x = randint(0, 1)
            if x == 0:
                x = -1
            self.x_velocity = 4*x
        if self.counter == 100:                          # shooting
            Bullet(self.rect.x + 9, self.rect.y + 9, 0, 0, "enemy", 12, 0.3, self.damage)
            self.counter = 0

        # x-movement
        self.rect.x += self.x_velocity
        for platform in self.platform_list:
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
        for platform in self.platform_list:
            if self.rect.colliderect(platform.rect):
                if self.y_velocity > 0:
                    self.rect.bottom = platform.rect.top
                if self.y_velocity < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_velocity = 10
