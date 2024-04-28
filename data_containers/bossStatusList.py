# boss status list : a struct that contains information on whether each boss is alive
class BossStatusList(object):
    def __init__(self, statuses = []):
        # default value of True
        self.target = True
        self.harmer = True

        # can also initialize with given values
        #   used in loading
        if len(statuses) >= 2:
            self.target = statuses[0]
            self.harmer = statuses[1] 

    # returns statuses in easily iterable list form
    def list_form(self):
        return [self.target, self.harmer]
    
    # removes a specified boss 
    def remove_boss(self, boss):
        if boss == "Target":
            self.target = False
        if boss == "Harmer":
            self.harmer = False