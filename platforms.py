import pygame
from abstract_classes.gameObject import GameObject

background_color_palette = [
    [0, 5,  (0, 0, 0),     0, 4,   (100, 100, 100)],    # tutorial colors
    [6, 8,  (0, 10, 0),    5, 9,   (50, 60, 50)   ],    # grass colors
    [9, 12, (0, 0, 10),    10, 12, (50, 50, 60)   ]     # ice colors
]

# platform: all walls and other hard surfaces
class Platform(GameObject):
    wall_color = (255, 100, 100)
    platforms = []

    def __init__(self, x_pos, y_pos, size, platform_type):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.type = platform_type
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

    # draws self based on current stage's wall color
    def draw(self):
        if self.type == "platform":               # these 2 platforms are just drawn in respective colors
            pygame.draw.rect(GameObject.window, Platform.wall_color, self.rect)
        if self.type == "load":
            pygame.draw.rect(GameObject.window, (255, 100, 0), self.rect)
        if self.type == "upgrade":                # upgrade (unlock token) decides if it should exist
            # checks world location and if the ability is not unlocked before revealing self
            if GameObject.world_y == 2 and GameObject.world_x == 1 and not GameObject.ability_statuses.double_jump:
                pygame.draw.rect(GameObject.window, (200, 200, 0), self.rect)
            elif GameObject.world_y == 3 and GameObject.world_x == 0 and not GameObject.ability_statuses.dash:
                pygame.draw.rect(GameObject.window, (200, 200, 0), self.rect)
            elif GameObject.world_y == 3 and GameObject.world_x == 5 and not GameObject.ability_statuses.blaster:
                pygame.draw.rect(GameObject.window, (200, 200, 0), self.rect)
            elif GameObject.world_y == 8 and GameObject.world_x == 0 and not GameObject.ability_statuses.health_increase:
                pygame.draw.rect(GameObject.window, (200, 200, 0), self.rect)
            else:
                self.delete()
    
    def delete(self):
        Platform.platforms.remove(self)
