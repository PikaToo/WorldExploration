import pygame
from abstract_classes.gameObject import GameObject

background_color_palette = [
    [0, 5,  (0, 0, 0),     0, 4,   (100, 100, 100)],    # tutorial colors
    [6, 8,  (0, 10, 0),    5, 9,   (50, 60, 50)   ],    # grass colors
    [9, 12, (0, 0, 10),    10, 12, (50, 50, 60)   ]     # ice colors
]

# platform: all walls, savepoints, and upgradepoints 
class Platform(GameObject):
    wall_color = (255, 100, 100)
    platforms = []

    def __init__(self, x_pos, y_pos, size, color):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.color = color
        Platform.platforms.append(self)

    # sets wall color based on current location and returns background color 
    @staticmethod
    def update_color():
        for value in background_color_palette:
            # checking if in y range
            if value[0] <= GameObject.world_y <= value[1]:     # first half is background color
                background_color = value[2]
            if value[3] <= GameObject.world_y <= value[4]:     # second half is wall color
                Platform.wall_color = value[5]
        
        return background_color 