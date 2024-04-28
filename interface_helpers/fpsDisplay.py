from abstract_classes.gameObject import GameObject
import pygame
from pygame.locals import * # for FPS key presses (backspace)

class FpsDisplay(GameObject):
    def __init__(self):
        self.show = False
        self.list = [60, 60, 60, 60]
        self.previous_backspace = True

    def display(self, fpsClock, font):
        key = pygame.key.get_pressed()

        # toggling FPS display with backspace
        if key[K_BACKSPACE] and not self.previous_backspace:
            self.show = not self.show
        
        # getting average FPS for use in drawing
        if self.show:
            self.list.append(int(fpsClock.get_fps()))
            del self.list[0]
            average_FPS = sum(self.list) / len(self.list)
            if average_FPS < 30:
                color = (255, 0, 0)
            elif average_FPS < 45:
                color = (255, 255, 0)
            else:
                color = (255, 255, 255)
            GameObject.window.blit(font.render(f"FPS: {average_FPS}", True, color), pygame.Rect(GameObject.window_width - 200, 0, 0, 0))

        self.previous_backspace = key[K_BACKSPACE]
