import pygame

# platform: all walls and other hard surfaces
class Platform(object):
    window = None
    world_x = 0
    world_y = 0
    wall_color = (255, 100, 100)
    ability_statuses = [False, False, False, False, False]

    platforms = []

    def __init__(self, x_pos, y_pos, size, platform_type):
        self.rect = pygame.Rect(x_pos, y_pos, size, size)
        self.type = platform_type
        Platform.platforms.append(self)

    # draws platforms based on current stage's wall color
    def draw(self):
        if self.type == "platform":               # these 2 platforms are just drawn in respective colors
            pygame.draw.rect(Platform.window, Platform.wall_color, self.rect)
        if self.type == "load":
            pygame.draw.rect(Platform.window, (255, 100, 0), self.rect)
        if self.type == "upgrade":                # upgrade (unlock token) decides if it should exist
            # checks world location and if the ability is not unlocked before revealing self
            if Platform.world_y == 2 and Platform.world_x == 1 and not Platform.ability_statuses[0]:
                pygame.draw.rect(Platform.window, (200, 200, 0), self.rect)
            elif Platform.world_y == 3 and Platform.world_x == 0 and not Platform.ability_statuses[1]:
                pygame.draw.rect(Platform.window, (200, 200, 0), self.rect)
            elif Platform.world_y == 3 and Platform.world_x == 5 and not Platform.ability_statuses[2]:
                pygame.draw.rect(Platform.window, (200, 200, 0), self.rect)
            elif Platform.world_y == 8 and Platform.world_x == 0 and not Platform.ability_statuses[3]:
                pygame.draw.rect(Platform.window, (200, 200, 0), self.rect)
            else:
                self.delete()
    
    def delete(self):
        Platform.platforms.remove(self)
