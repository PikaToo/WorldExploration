from gameObject import GameObject
from abilityStatusList import AbilityStatusList
from bossStatusList import BossStatusList

# save manager : handles all saving and loading 
class SaveManager(GameObject):
    def __init__(self):
        # storing default save file information to start
        self.world_x = 0
        self.world_y = 0
        self.boss_statuses = BossStatusList()
        self.ability_statuses = AbilityStatusList()
        self.gold = 0
        self.player_position = (100, 550)

    # overwrites old save data with new data from GameObject
    def save_data(self, player):
        self.world_x = GameObject.world_x        
        self.world_y = GameObject.world_y
        self.boss_statuses = GameObject.boss_statuses
        self.ability_statuses = GameObject.ability_statuses
        self.gold = GameObject.gold
        self.player_position = player.get_position()
    
    # overwrites GameObject data with previously saved data
    def load_data(self, player):
        GameObject.world_x = self.world_x
        GameObject.world_y = self.world_y
        GameObject.boss_statuses = self.boss_statuses
        GameObject.ability_statuses = self.ability_statuses
        GameObject.gold = self.gold

        # moves player to desired location
        player.set_position(self.player_position)

        #TODO: also needs to remake world

    # used to load
    def load_from_code(self, code, player):
        # code of 0 to 1 used to find world position
        world_position = int(code[0] + code[1])
        
        if world_position == 0:
            self.world_x = 0
            self.world_y = 0
        if world_position == 1:
            self.world_x = 0
            self.world_y = 8
        if world_position == 2:
            self.world_x = 2
            self.world_y = 7
        if world_position == 97:
            self.world_x = 5
            self.world_y = 3
        if world_position == 98:
            self.world_x = 0
            self.world_y = 8
        if world_position == 99:
            self.world_x = 4
            self.world_y = 11
        

        # parsing ability and boss list
        s_ability_list = []
        s_boss_list = []

        i = 2
        while i <= 19:
            if i <= 11:
                # code [2 -> 11] is used for bosses
                if int(code[i]) == 1:
                    s_boss_list.append(True)
                else:
                    s_boss_list.append(False)
            
            # code [12 -> 19] is used for abilities
            elif i <= 19:
                if int(code[i]) == 1:
                    s_ability_list.append(True)
                else:
                    s_ability_list.append(False)
            i += 1

        self.boss_statuses = BossStatusList(s_boss_list)
        self.ability_statuses = AbilityStatusList(s_ability_list)

        # gold stored as string across 4 characters
        self.gold = int(code[20] + code[21] + code[22] + code[23])

        # loading data
        self.load_data(player)
        