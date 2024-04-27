from gameObject import GameObject
from minimap import Minimap
import pygame

class Pauser(GameObject):
    def __init__(self):
        self.holding_escape = True
        self.paused = False
    
    def check_for_pause(self, pressing_escape):
        # toggles pause if pressing but not holding
        if pressing_escape and not self.holding_escape:
            self.paused = not self.paused

        # giving information on this frame to next frame
        #   to see if holding
        self.holding_escape = pressing_escape


    def display(self, world, font):
        # showing pause text
        GameObject.window.blit(font.render("Paused.", False, (255, 255, 255)), (50, 200))
        
        # showing world map
        world_map = Minimap(world, GameObject.boss_statuses)
        world_map.display()

        # showing unlocked abilities
        map_x = 10 
        map_y = 10
        for ability in GameObject.ability_statuses.list_form():
            ability_rect = pygame.Rect(map_x, map_y, 30, 30)
            pygame.draw.rect(GameObject.window, (100, 50, 50), ability_rect)
            if ability:
                ability_rect = pygame.Rect(map_x + 5, map_y + 5, 20, 20)
                pygame.draw.rect(GameObject.window, (200, 100, 100), ability_rect)
            map_x += 50
