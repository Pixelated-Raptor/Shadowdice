import random
from PIL import Image

class SixSidedDie:
    """
    Class representing a six sided die.
    Also handles the die assets using PIL.Image.
    """
    VALUES = [1, 2, 3, 4, 5, 6]

    DOT_DIE = "../Assets/Black_Die_Dotted/"
    NUM_DIE = "../Assets/Black_Die_Numbered/"
    DOT_DIE_COL = "../Assets/Coloured_Die_Dotted/"
    NUM_DIE_COL = "../Assets/Coloured_Die_Numbered/"

    IMG_SIZE = None
    
    NUM2WORDS = {
        1: "one", 2: "two", 3: "three",
        4: "four", 5: "five", 6: "six"
    }
    
    dot_die_assets = {}
    num_die_assets = {}
    dot_die_col_assets = {}
    num_die_col_assets = {}

    def __init__(self):
        for x in self.VALUES:
            self.dot_die_assets[x] = Image.open(self.DOT_DIE + self.NUM2WORDS[x] + ".png")
            self.num_die_assets[x] = Image.open(self.NUM_DIE + self.NUM2WORDS[x] + ".png")
            self.dot_die_col_assets[x] = Image.open(self.DOT_DIE_COL + self.NUM2WORDS[x] + ".png")
            self.num_die_col_assets[x] = Image.open(self.NUM_DIE_COL + self.NUM2WORDS[x] + ".png")

        self.IMG_SIZE = self.dot_die_assets[1].size[0]

    def get_die_asset(self, config, number):
        """ Return requested die asset depending on user settings. """
        match config.dice_style:
            case "dotted":
                return self.dot_die_assets[number]
            case "numbered":
                return self.num_die_assets[number]
            case "dotted coloured":
                if(number == 4 and number in config.hits):
                    return self.dot_die_col_assets[number]
                elif(number == 4):
                    return self.dot_die_assets[number]
        
                if(number == 2 and number in config.misses):
                    return self.dot_die_col_assets[number]
                elif(number == 2):
                    return self.dot_die_assets[number]

                return self.dot_die_col_assets[number]
            case "numbered coloured":
                if(number == 4 and number in config.hits):
                    return self.num_die_col_assets[number]
                elif(number == 4):
                    return self.num_die_assets[number]
        
                if(number == 2 and number in config.misses):
                    return self.num_die_col_assets[number]
                elif(number == 2):
                    return self.num_die_assets[number]

                return self.num_die_col_assets[number]
            
    def Roll(self):
        """ Emulates a single die throw by choosing a random value from self.VALUES. """
        return random.choice(self.VALUES)

    def RollNTimes(self, n):
        result = []
        for i in range(n):
            result.append(self.Roll())

        if(type(result) is not list):
            result = [result]
            
        return result
