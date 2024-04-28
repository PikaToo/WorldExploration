from enemy import Enemy

class Bird(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (200, 200, 255), 25, 3, 1, 2, player, platform_list)

    def move(self):
        self.apply_standard_x_movement()
        
        self.rect.y += self.y_velocity
        for platform in self.platform_list:  # unique bounce-wall gravity
            if self.rect.colliderect(platform.rect):
                if self.y_velocity < 0:
                    self.rect.top = platform.rect.bottom
                    self.y_velocity = 0
                    self.x_velocity *= 0.5
                if self.y_velocity > 0:
                    self.rect.bottom = platform.rect.top
                    self.y_velocity = -10

        x_diff = self.player.rect.x - self.rect.x                # moving towards player
        y_diff = self.player.rect.y - self.rect.y
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

