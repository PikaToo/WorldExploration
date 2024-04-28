from gameObject import GameObject

class GoldManager(GameObject):
    def __init__(self):
        pass

    def gain_gold(self, gold):
        GameObject.gold += gold
    
    def lose_gold(self, gold):
        GameObject.gold -= gold

    def current_gold(self):
        return GameObject.gold

    def set_gold(self):
        GameObject.gold = self.gold

    def display_overlay(self, font):
        GameObject.window.blit(font.render((str(self.gold)+"g"), False, (255, 255, 50)), (5, 575))