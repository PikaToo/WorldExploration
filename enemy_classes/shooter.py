from enemy import Enemy
from bullet import Bullet

class Shooter(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (200, 200, 255), 30, 3, 1, 2, player, platform_list)

    def move(self):
        self.apply_standard_x_movement()
        self.apply_standard_y_movement()
        
        if self.counter > 60:
            x_diff = self.player.rect.x - self.rect.x
            y_diff = self.player.rect.y - self.rect.y

            if not (abs(x_diff) + abs(y_diff)) == 0:  # first making sure no divide by 0 error

                x_vector = x_diff / (abs(x_diff) + abs(y_diff))  # getting how much of x is in x + y
                y_vector = y_diff / (abs(x_diff) + abs(y_diff))  # getting how much of y is in x + y
                Bullet(self.rect.x + 9, self.rect.y + 9, x_vector * 20, y_vector * 20, "enemy", 12, 0, self.damage)
            
            self.counter = 0

        self.counter += 1