import pygame
from gameObject import GameObject

# persistent text box : object that displays text over its time period 
#   when triggered
class PersistentTextBox(GameObject):
    def __init__(self, text, font, color, x_position = 700, y_position = 566):
        # default position is at bottom right of screen
        self.position = (x_position, y_position)
        self.text = font.render(text, True, color)
        self.show_timer = 0
    
    # turns on text box 
    def enable(self):
        self.show_timer = 100
    
    # displays and then ticks down counter
    def display(self):
        if self.show_timer > 0:
            self.text.set_alpha(self.show_timer * 10)
            GameObject.window.blit(self.text, self.position)
            self.show_timer -= 1
    