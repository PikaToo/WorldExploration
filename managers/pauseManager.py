from abstract_classes.gameObject import GameObject
from interface_helpers.minimap import Minimap
import pygame

pygame.font.init()
font = pygame.font.SysFont('arial', 40)
medium_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 20)

class PauseManager(GameObject):
    def __init__(self):
        self.holding_escape = True

        # can pause by either having chosen to do or hitting an upgrade
        self.manually_paused = False
        self.upgrader_paused = False

    def check_for_pause(self, pressing_escape, platform_list, player):
        # first checking for manual pausing
        if pressing_escape and not self.holding_escape and not self.upgrader_paused:
            self.manually_paused = not self.manually_paused

        # next checking for upgrader pausing 
        # enter upgrader pause by hitting platform
        for platform in platform_list:
            if platform.type == "upgrade" and player.rect.colliderect(platform.rect):
                self.upgrader_paused = True
        
        # exist upgrader pause by pressing escape
        if pressing_escape:
            self.upgrader_paused = False

        # giving information on this frame to next frame
        self.holding_escape = pressing_escape


    def display(self, world, font, medium_font, small_font):
        if self.manually_paused:
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

        if self.upgrader_paused:
            if GameObject.world_y == 2 and GameObject.world_x == 1:
                GameObject.ability_statuses.double_jump = True
                text1 = "Unlocked double jump."
                text2 = "Press W while in the air to use."
            elif GameObject.world_y == 3 and GameObject.world_x == 0:
                GameObject.ability_statuses.dash = True
                text1 = "Unlocked dash."
                text2 = "Press space to use."
            elif GameObject.world_y == 3 and GameObject.world_x == 5:
                GameObject.ability_statuses.blaster = True
                text1 = "Unlocked blaster."
                text2 = "Press arrow keys or click the mouse to use."
            elif GameObject.world_y == 8 and GameObject.world_x == 0:
                GameObject.ability_statuses.health_increase = True
                text1 = "Health has been increased."
                text2 = "You now have more health."
            else:
                text1 = ""
                text2 = ""

            GameObject.window.blit(font.render(text1, False, (255, 255, 255)), (50, 200))
            GameObject.window.blit(medium_font.render(text2, False, (255, 255, 255)), (50, 280))
            GameObject.window.blit(small_font.render("Press Escape to leave this menu.", False, (255, 255, 255)),
                        (50, 400))
