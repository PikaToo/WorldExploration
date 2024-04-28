from abstract_classes.gameObject import GameObject
from abstract_classes.platforms import Platform
import pygame

class Savepoint(Platform):
    savepoints = []
    def __init__(self, x_pos, y_pos, size):
        super().__init__(x_pos, y_pos, size, (255, 100,))
        Savepoint.savepoints.append(self)

    def draw(self):
        pygame.draw.rect(GameObject.window, self.color, self.rect)
    
    def delete(self):
        Platform.platforms.remove(self)
        Savepoint.savepoints.remove(self)