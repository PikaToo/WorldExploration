# game object: an object that is used by the game 
#   gives the object access to the world state, the window, etc. 
class GameObject(object):
    window = None

    window_width = 0
    window_height = 0
    
    world_x = 0
    world_y = 0

    ability_statuses = []
    boss_statuses = []

    def __init__(self):
        pass

    # setter methods used by main
    @staticmethod
    def set_window(window):
        GameObject.window = window
    
    @staticmethod
    def set_window_size(window_width, window_height):
        GameObject.window_width = window_width
        GameObject.window_height = window_height

    @staticmethod
    def set_world_coordinates(world_x, world_y):
        GameObject.world_x = world_x
        GameObject.world_y = world_y
    
    @staticmethod
    def set_ability_statuses(ability_statuses):
        GameObject.ability_statuses = ability_statuses
    
    @staticmethod
    def set_boss_statuses(boss_statuses):
        GameObject.boss_statuses = boss_statuses