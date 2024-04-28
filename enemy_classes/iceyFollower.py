from abstract_classes.enemy import Enemy

class IceyFollower(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (200, 200, 255), 20, 8, 1, 1, player, platform_list)

    def move(self):
        self.apply_standard_x_movement()
        self.apply_standard_y_movement()
        
        if self.counter > 60:
            if self.rect.x < self.player.rect.x and self.x_velocity < 6:
                self.x_velocity += 0.2
            if self.rect.x > self.player.rect.x and self.x_velocity > -6:
                self.x_velocity -= 0.2
        else:
            self.x_velocity = 0

        self.counter += 1