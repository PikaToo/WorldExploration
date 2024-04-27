import pygame
from gameObject import GameObject

# platform: all walls and other hard surfaces
class Platform(GameObject):
    wall_color = (255, 100, 100)
    ability_statuses = [False, False, False, False, False]

    platforms = []

    def __init__(self, x_pos, y_pos, size, platform_type):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.type = platform_type
        Platform.platforms.append(self)

    # draws platforms b:ased on current stage's wall color
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
