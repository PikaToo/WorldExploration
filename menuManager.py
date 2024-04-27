from gameObject import GameObject
import pygame
from pygame.locals import *
import sys
from abilityStatusList import AbilityStatusList

class MenuManager():
    def __init__(self):
        self.main_menu = MainMenu()
        self.load_menu = LoadMenu() 
        self.menu_shown = "Main"

    def display(self, events, font):
        # if we're meant to show the main menu, show it and get what we show next frame
        if self.menu_shown == "Main":
            self.menu_shown = self.main_menu.display(font)

        # if we're meant to show the load menu, show it and get what we show next frame
        elif self.menu_shown == "Load":
            self.menu_shown = self.load_menu.display(events, font)

        # in other cases we don't display anything
    

    # gives the load data present if there is any
    def load_data(self):
        # print(self.menu_shown)
        # if showing a menu, no data
        if self.menu_shown == "Main" or self.menu_shown == "Load":
            return None
        
        # if on new game, give default data
        if self.menu_shown == "New Game":
            return (0, [True, True, True, True, True, True, True, True, True, True], AbilityStatusList(), 0)

        # else give load data
        return self.menu_shown

class MainMenu(GameObject):
    def __init__(self):
        # getting locations of all buttons
        x_location = 340                                                # used to easily change their x later if needed
        self.new_rect = pygame.Rect(x_location, 500, 185, 50)
        self.load_rect = pygame.Rect(x_location + 300, 500, 185, 50)
        self.back_new_rect = pygame.Rect(x_location - 5, 495, 195, 60)
        self.back_load_rect = pygame.Rect(x_location + 295,  495, 195, 60)

    def display(self, font):
        mouse_x, mouse_y = pygame.mouse.get_pos()                   # getting mouse pos for collision checks later
        mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)

        GameObject.window.fill((0, 0, 0))

        load_back_color = new_back_color = (30, 30, 30)             # setting background color for both buttons

        if mouse_rect.colliderect(self.new_rect):                        # if button collides, changes back color
            new_back_color = (200, 200, 50)
            if pygame.mouse.get_pressed()[0]:                       # ends screen if new is clicked
                return "New Game" 
        if mouse_rect.colliderect(self.load_rect):                       # switches to load screen if load is clicked
            load_back_color = (200, 200, 50)
            if pygame.mouse.get_pressed()[0]:
                return "Load"

        # drawing the back of the buttons
        pygame.draw.rect(GameObject.window, new_back_color, self.back_new_rect)
        pygame.draw.rect(GameObject.window, load_back_color, self.back_load_rect)

        # drawing the buttons
        pygame.draw.rect(GameObject.window, (50, 50, 50), self.new_rect)
        pygame.draw.rect(GameObject.window, (50, 50, 50), self.load_rect)

        # drawing the text on buttons
        GameObject.window.blit(font.render(" New Game", True, (255, 255, 255)), self.new_rect)
        GameObject.window.blit(font.render(" Load Game", True, (255, 255, 255)), self.load_rect)

        # game title
        large_font = pygame.font.SysFont('arial', 150)
        GameObject.window.blit(large_font.render("World Explorer", True, (200, 200, 255)), pygame.Rect(50, 50, 195, 60))
        pygame.draw.rect(GameObject.window, (0, 0, 255), pygame.Rect(950, 100, 100, 100))

        return "Main" # if nothing happened, stay here

class LoadMenu(GameObject):
    def __init__(self):
        self.code = ""
        # temp_code = 9901 1111 1111 1111 0000 0000
        # self.code = "990011111111111100000000"
        # self.code = "980011111111100000000000"
        self.code = "980011111111111000000000"
        self.message = "Enter your load code."

    # function that runs when asked to input a load: used after main menu. 
    def display(self, events, font):       
        for evt in events:   # text entry is best handled this way instead of get_pressed() as per Pygame documentation
            if evt.type == KEYDOWN:
                if str(evt.unicode) in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"] and len(self.code) < 24:
                    self.code = self.code + str(evt.unicode)          # types numbers
                if evt.key == K_BACKSPACE:
                    self.code = self.code[:-1]                        # backspaces
                if evt.key == K_RETURN:
                    if len(self.code) != 24:                     # code must be 20 characters to work
                        self.code = ""
                        self.message = "Invalid load code."
                    else:
                        # processes the save data
                        s_point = int(self.code[0] + self.code[1])                        # name[0 -> 1] used for save point.
                                                                                # 2 values
                        # initial values for the loading loop
                        s_ability_list = []
                        s_boss_list = []

                        i = 2
                        while i <= 19:
                            if i <= 11:
                                if int(self.code[i]) == 1:                   # name[2 -> 11] used for bosses
                                    s_boss_list.append(True)            # 10 values
                                else:
                                    s_boss_list.append(False)
                            elif i <= 19:                               # name[12 -> 19] used for abilities
                                if int(self.code[i]) == 1:                   # 8 values
                                    s_ability_list.append(True)
                                else:
                                    s_ability_list.append(False)
                            i += 1

                        s_gold = int(self.code[20] + self.code[21] + self.code[22] + self.code[23])     # name[20 - 23] used for gold
                        save_point = (s_point, s_boss_list, AbilityStatusList(s_ability_list), s_gold)

                        return save_point

        # formatting the load code to make it more legible
        formatted_code = ""
        iteration = 0
        for character in self.code:
            iteration += 1
            formatted_code += character
            if iteration % 4 == 0:              # can't just check length of the formatted_code since it changes
                formatted_code += "  "

        # drawing everything
        GameObject.window.fill((0, 0, 0))
        message_font = font.render(self.message, True, (255, 255, 255))
        message_rect = message_font.get_rect()
        message_rect.x = 400
        message_rect.y = 200
        GameObject.window.blit(message_font, message_rect)
        message_rect.x = 300
        message_rect.y = 250
        GameObject.window.blit(font.render(formatted_code, True, (200, 200, 200)), message_rect)

        # we continue loading until we return a save point
        return "Load"