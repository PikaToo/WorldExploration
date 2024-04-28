import pygame
from abstract_classes.gameObject import GameObject

# fader: used to handle fade-ins and fade-outs
class FadeManager(GameObject):
    def __init__(self):
        self.fade_screen = pygame.Surface((1200, 600))
        self.fade_screen.fill((0, 0, 0))
        self.alpha = 255

    # shows current fade screen
    def display(self):
        self.fade_screen.set_alpha(self.alpha)
        GameObject.window.blit(self.fade_screen, (0, 0))

    # increases alpha by 20 (capped at 255)
    def darken_fade(self):
        self.alpha += 20
        self.alpha = min(self.alpha, 255)

    # decreases alpha by 20 (capped at 0)
    def lighten_fade(self):
        self.alpha -= 20
        self.alpha = max(self.alpha, 0)
    
    # sets fade to darkest value
    def set_darkest_fade(self):
        self.alpha = 255
    
    # returns if at darkest value
    def at_darkest(self):
        return (self.alpha == 255)