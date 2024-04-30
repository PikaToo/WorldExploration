from abstract_classes.enemy import Enemy
from abstract_classes.gameObject import GameObject

class Target(Enemy):
    def __init__(self, x_pos, y_pos, player, platform_list):
        # x pos, y pos, color, size, max health, damage, gold, player, platform_list
        super().__init__(x_pos, y_pos, (255, 0, 0), 20, 8, 1, 1, player, platform_list)
        
        # is a boss: hence stop player from being able to leave
        self.player.exit_status = False 

    def move(self):
        self.apply_standard_x_movement()
        self.apply_standard_y_movement()
 
    # bosses have their own deletion
    def delete(self):
        self.player.exit_status = True
        GameObject.boss_statuses.target = False
        Enemy.enemies.remove(self)
