from abstract_classes.gameObject import GameObject
from abstract_classes.platforms import Platform
import pygame

class Upgradepoint(Platform):
    upgradepoints = []
    def __init__(self, x_pos, y_pos, size):
        # checking if allowed to be made
        if (GameObject.world_y == 2 and GameObject.world_x == 1 and not GameObject.ability_statuses.double_jump)    \
        or (GameObject.world_y == 3 and GameObject.world_x == 0 and not GameObject.ability_statuses.dash)           \
        or (GameObject.world_y == 3 and GameObject.world_x == 5 and not GameObject.ability_statuses.blaster)        \
        or (GameObject.world_y == 8 and GameObject.world_x == 0 and not GameObject.ability_statuses.health_increase):            
            super().__init__(x_pos, y_pos, size, (200, 200, 0))
            Upgradepoint.upgradepoints.append(self)

    def draw(self):
        pygame.draw.rect(GameObject.window, self.color, self.rect)
    
    def delete(self):
        Platform.platforms.remove(self)
        Upgradepoint.upgradepoints.remove(self)