environment = []
people = []
env_params = {"s1": 6, "s2": 8, "s3": 20, "s4": 30, "b1": 45, "b2": 60, "b3": 80}

class person:
    def __init__(self, name='NameNotSet', age=0):
        self.name = name
        self.location = []
        self.moveNum = 0
        self.schedule = []
        self.scheduleFinal = []
        self.movePath = []
        self.infectedBy = []
        self.infectedIn = []
        self.infected = False
        self.infectedType = [0]
        self.infectedTypeNum = 0
        self.lockeddown = False
        self.lockdowndays = 0
        self.immune = False
        self.bathroomCount = 0
        self.infectedOdds = self.infectedType[self.infectedTypeNum]
        self.vaccine = 0
        self.cohort = 0
        self.recentContacts = []


