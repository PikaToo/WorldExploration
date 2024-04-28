import pygame
from platform_classes.wall import Wall       # entities need to know wall locations
from abstract_classes.gameObject import GameObject

class Entity(GameObject):
    def __init__(self, x_pos, y_pos, size, color, x_velocity, y_velocity):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.color = color
        self.size = size

    # checks for collision against walls
    def colliding_with_walls(self):
        for wall in Wall.walls:
            if self.rect.colliderect(wall.rect):
                return True
        return False

    # returns true if entity is inside world bounds
    def in_bounds(self): 
        in_vertical_bounds = 0 < self.rect.y < GameObject.window_height - self.size 
        in_horizontal_bounds = 0 < self.rect.x < GameObject.window_width - self.size
        return in_vertical_bounds and in_horizontal_bounds

    def draw(self):
        pygame.draw.rect(GameObject.window, self.color, self.rect)