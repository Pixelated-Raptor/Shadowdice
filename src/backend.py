from SixSidedDie import *
from config import config

die = SixSidedDie()
app_config = config()

HITS = app_config.hits
MISSES = app_config.misses

def bk_throw(dice_pool):
    return(die.RollNTimes(dice_pool))
    
def bk_pre_edge():
    print("pre edge")

def bk_post_edge():
    print("post edge")

def bk_edge_roll():
    print("edge_roll")

def bk_roll_for_edge():
    print("Rolling for edge")
    
def bk_reroll_misses():
    print("reroll misses")

def bk_evaluate_roll(result):
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
