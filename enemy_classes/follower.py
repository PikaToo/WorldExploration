from enemy import Enemy

class Follower(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        super().__init__(x_pos, y_pos, (100, 50, 0), 20, 5, 1, 1, player, platform_list)

    def move(self):
        self.apply_standard_x_movement()
        self.apply_standard_y_movement()
        
        sight_range = 350
        min_x = self.rect.x - sight_range
        max_x = self.rect.x + self.rect.width + sight_range
        if self.counter > 60 and self.player.rect.x in range(min_x, max_x):
            if self.rect.x < self.player.rect.x and self.x_velocity < 2:
                self.x_velocity += 0.1
            if self.rect.x > self.player.rect.x and self.x_velocity > -2:
                self.x_velocity -= 0.1
        else:
            self.x_velocity = 0

        self.counter += 1