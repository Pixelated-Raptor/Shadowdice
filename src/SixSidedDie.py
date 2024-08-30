import random
from PIL import Image

class SixSidedDie:
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
        for x in range(1, len(self.NUM2WORDS) + 1):
            self.dot_die_assets[x] = Image.open(self.DOT_DIE + self.NUM2WORDS[x] + ".png")
            self.num_die_assets[x] = Image.open(self.NUM_DIE + self.NUM2WORDS[x] + ".png")
            #self.dot_die_col_assets[x] = Image.open(self.DOT_DIE_COL + self.NUM2WORDS[x] + ".png")
            #self.num_die_col_assets[x] = Image.open(self.NUM_DIE_COL + self.NUM2WORDS[x] + ".png")

        self.IMG_SIZE = self.dot_die_assets[1].size[0]

    def get_die(self, style, number):
        match style:
            case "Dotted":
                return self.dot_die_assets[number]
            case "Numbered":
                return self.num_die_assets[number]
            case "Dotted Coloured":
                return self.num_die_col_assets[number]
            case "Numbered Coloured":
                return self.dot_die_col_assets[number]
            case _:
                return self.dot_die_assets[number]
        
    def Roll(self):
        return random.choice(self.VALUES)

    def RollNTimes(self, n):
        result = []
        for i in range(n):
            result.append(self.Roll())

        if(type(result) is not list):
            result = [result]
            
        return result
