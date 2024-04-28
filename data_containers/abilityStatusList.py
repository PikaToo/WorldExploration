# ability status list : a struct that contains information on all abilities obtained so far
class AbilityStatusList(object):
    def __init__(self, statuses = []):
        # default value of False
        self.double_jump = False
        self.dash = False
        self.blaster = False
        self.health_increase = False

        # can also initialize with given values
        #   used in loading
        if len(statuses) >= 4:
            self.double_jump = statuses[0]
            self.dash = statuses[1]
            self.blaster = statuses[2]
            self.health_increase = statuses[3]
        

    # returns statuses in easily iterable list form
    #   used in pauser
    def list_form(self):
        return [self.double_jump, self.dash, self.blaster, self.health_increase]