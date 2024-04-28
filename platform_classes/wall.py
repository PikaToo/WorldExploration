from abstract_classes.gameObject import GameObject
from abstract_classes.platforms import Platform
import pygame

class Wall(Platform):
    walls = []
    def __init__(self, x_pos, y_pos, size):
        super().__init__(x_pos, y_pos, size, Platform.wall_color)
        Wall.walls.append(self)

    def draw(self):
        pygame.draw.rect(GameObject.window, self.color, self.rect)
    
    def delete(self):
        Platform.platforms.remove(self)
        Wall.walls.remove(self)