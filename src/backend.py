#================================================
# Class for handling the logic with dice throwing
#================================================
from SixSidedDie import *
from config import config

class backend():
    die = None
    
    def __init__(self):
        self.die = SixSidedDie()
        
    def throw(self, dice_pool):
        return(self.die.RollNTimes(dice_pool))
    
    def pre_edge(self):
        print("pre edge")
    
    def post_edge(self):
        print("post edge")
    
    def edge_roll(self):
        print("edge_roll")
    
    def roll_for_edge(self):
        print("Rolling for edge")
        
    def reroll_misses(self):
        print("reroll misses")
    
    def evaluate_roll(self, result, HITS, MISSES):
        hits = 0
        misses = 0
        glitch = False
        critical_glitch = False
    
        for i in result:
            if i in HITS:
                hits += 1
            elif i in MISSES:
                misses += 1
                
        if misses > (len(result) / 2) and hits > 0:
            glitch = True
        elif misses > (len(result) / 2) and hits == 0:
            critical_glitch = True
    
        return(hits, misses, glitch,critical_glitch)
