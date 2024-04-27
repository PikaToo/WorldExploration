import pygame
from gameObject import GameObject

class Minimap(GameObject):
    def __init__(self, world, boss_statuses):
        self.platforms = []
        self.load_zones = []
        self.boss_zones = []
        
        map_x = 300
        map_y = 100

        # massive loop like that of level creation, but with two more iterations to look
        #  look for each level then each thing in each level to get the whole world.
        for lev_row in world:
            for lev_value in lev_row:
                for row in lev_value:
                    for value in row:
                        # platforms
                        if value == "W":
                            block = pygame.Rect(map_x, map_y, 1, 1)
                            self.platforms.append(block)
                            
                        if value == "L" or value in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]: 
                            x_middle = 16 + map_x - ((map_x - 300) % 40)  # loads/bosses added to list
                            y_middle = 6 + map_y - ((map_y - 100) % 20)
                            block = pygame.Rect(x_middle, y_middle, 8, 8)
                            if value == "L":
                                self.load_zones.append(block)
                            else:
                                if boss_statuses[int(value)]:  # boss only added if alive
                                    self.boss_zones.append(block)
                        map_x += 1
                    map_x -= 40
                    map_y += 1
                map_y -= 20
                map_x += 40
            map_y += 20
            map_x = 300

    def display(self):
        for platform in self.platforms: 
            pygame.draw.rect(GameObject.window, (150, 150, 150), platform)
        for load in self.load_zones:                         # loads/bosses drawn later (after walls) to be on top
            pygame.draw.rect(GameObject.window, (255, 100, 0), load)
        for boss in self.boss_zones:
            pygame.draw.rect(GameObject.window, (255, 0, 0), boss)
        
        player_loc = pygame.Rect(GameObject.world_x * 40 + 315, GameObject.world_y * 20 + 105, 10, 10)    # getting player location
        pygame.draw.rect(GameObject.window, (0, 0, 255), player_loc)                           # player drawn last
