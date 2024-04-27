from gameObject import GameObject
from pygame.locals import * # for pause key presses
import pygame               # for drawing

class Upgrader(GameObject):
    def __init__(self):
        self.upgrading = False
    
    def check_for_pause(self, pressing_escape, platform_list, player):
        # enter menu by hitting platform
        for platform in platform_list:
            if platform.type == "upgrade" and player.rect.colliderect(platform.rect):
                self.upgrading = True
        
        # leave menu by pressing escape
        if pressing_escape:
            self.upgrading = False

    def display(self, font, medium_font, small_font):
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