from gameObject import GameObject
from persistentTextBox import PersistentTextBox

import pygame
pygame.font.init()
font = pygame.font.SysFont('arial', 40)
medium_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 20)

class UiManager(GameObject):
    def __init__(self, healthManager, goldManager):
        # tied to a healthManager and goldManager
        #  displays what they state 
        self.healthManager = healthManager
        self.goldManager = goldManager

        self.save_box = PersistentTextBox("Your progress has been saved.", medium_font, (255, 255, 100))
        self.exit_box = PersistentTextBox("Exit is closed until the boss is defeated.", medium_font, (255, 100, 100)) 

    def enable_save_text(self):
        self.save_box.enable()

    def enable_exit_text(self):
        self.exit_box.enable()

    def display(self):
        # drawing health
        self.healthManager.healthOverlay.display()
        
        # drawing gold
        gold_text = str(self.goldManager.current_gold())+"g"
        gold_font_object = small_font.render(gold_text, True, (255, 255, 50))
        GameObject.window.blit(gold_font_object, (5, 575))
        
        # drawing current stage
        #  need to calculate the stage from the given world x, world y
        stage_text = (chr(65 + GameObject.world_x) + str('%02d' % (GameObject.world_y + 1)))
        stage_font_object = small_font.render(stage_text, True, (255, 255, 255))
        GameObject.window.blit(stage_font_object, (1171, 575))

        # drawing save/exit text boxes- these handle on their own if they are meant to be shown or not
        self.save_box.display()
        self.exit_box.display()
