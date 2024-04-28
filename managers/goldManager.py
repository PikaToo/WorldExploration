from abstract_classes.gameObject import GameObject

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
