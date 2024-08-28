import random

class SixSidedDie:
    SIDES = 6
    values = []

    def __init__(self):
        valueRange = range(1, self.SIDES+1)
        for x in valueRange:
           self.values.append(x)

    def Roll(self):
        return random.choice(self.values)

    def RollNTimes(self, n):
        result = []
        for i in range(n):
            result.append(self.Roll())

        if(type(result) is not list):
            result = [result]
            
        return result
