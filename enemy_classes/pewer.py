from abstract_classes.enemy import Enemy
from bullet import Bullet

class Pewer(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (200, 200, 255), 40, 15, 2, 3, player, platform_list)

    def move(self):
        self.apply_standard_x_movement()
        self.apply_standard_y_movement()

        if self.counter > 120:
            self_pos_x = self.rect.x + 20
            player_x = self_pos_x + 10
            player_x_distance = self.player.rect.x - player_x
            self_pos_y = self.rect.y + 20 
            player_y = self.player.rect.y - 10
            player_y_distance = player_y - self_pos_y
            
            # initial x velocity based on distance away.
            x_vector = (player_x_distance/60)
            
            # done using suvat, u = (0.5at^2 - s)/t
            y_vector = (player_y_distance-540)/60
            
            # bullets still always some off. probably due to pygame rounding and some calculation
            #   errors on my side.
            Bullet(self.rect.x + 10, self.rect.y + 10, x_vector, y_vector, "enemy", 20, 0.3, self.damage)
            self.counter = 0

        self.counter += 1