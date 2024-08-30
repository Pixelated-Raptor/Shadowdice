#================================================
# Class for handling the logic with dice throwing
#================================================
from SixSidedDie import *
from config import config
from PIL import ImageTk, Image

class backend():
    die = None
    
    def __init__(self):
        self.die = SixSidedDie()
        
    def throw(self, dice_pool):
        return(self.die.RollNTimes(dice_pool))
    
    def pre_edge(self, use_full_edge, pool, edge_attribut, edge_left):
        result = []
        if(use_full_edge):
            result = self.throw(pool + edge_attribut)
        else:
            result = self.throw(pool + edge_left)

        result += self.apply_exploding_sixes(result)

        return result
    
    def post_edge(self, use_full_edge, edge_attribut, edge_left):
        result = []
        if(use_full_edge):
            result = self.throw(edge_attribut)
        else:
            result = self.throw(edge_left)

        result += self.apply_exploding_sixes(result)

        return result
        
    def edge_roll(self, use_full_edge, edge_attribut, edge_left):
        #Use either the full edge attribut or only edge left as dice pool
        result = []
        if(use_full_edge):
            result = self.throw(edge_attribut)
        else:
            result = self.throw(edge_left)

        result += self.apply_exploding_sixes(result)

        return result

        
    def roll_for_edge(self, edge):
        return(self.throw(edge))
        
    def reroll_misses(self, pool, hits):
        new_pool = 0
        for x in hits:
            new_pool += pool.count(x)
        
        new_pool = len(pool) - new_pool

        result = self.throw(new_pool)
        result += self.apply_exploding_sixes(result)

        return result
        
    def apply_exploding_sixes(self, pool):
        sixes = pool.count(6)
        res = []
        while sixes != 0:
            temp = self.throw(sixes)
            sixes = temp.count(6)
            res += temp
        
        return res
            
    def evaluate_roll(self, result, HITS, MISSES):
        hits = 0
        misses = 0
        glitch = False
        critical_glitch = False

        print("Eva Hits: " + str(HITS))
        print("Eva Misses: " + str(MISSES))
   
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

    def merge_die(self, result):
        #Path to files here
        one = Image.open("../Assets/Black_Die_Dotted/One_Dot.png")   
        two = Image.open("../Assets/Black_Die_Dotted/Two_Dot.png")   
        three = Image.open("../Assets/Black_Die_Dotted/Three_Dot.png")   
        four = Image.open("../Assets/Black_Die_Dotted/Four_Dot.png")   
        five = Image.open("../Assets/Black_Die_Dotted/Five_Dot.png")   
        six = Image.open("../Assets/Black_Die_Dotted/Six_Dot.png")   
        
        num2words = {
            1: one, 2: two, 3: three,
            4: four, 5: five, 6: six
        }
        #Determine dimensions of resulting image
        if(len(result) == 1):
            width = one.size[0]
            columns = 1
        elif(len(result) == 2):
            width = one.size[0] * 2
            columns = 2
        else:
            width = one.size[0] * 3
            columns = 3

        rows = -(-len(result) // 3)
        height = rows * one.size[1]
        
        #Stitch images
        image = Image.new("RGBA", (width, height))
        x = 0; y = 0; index = 0
        
        for i in range(len(result)):
            for row in range(rows):
                for column in range(columns):
                    if index < len(result):
                        im = num2words[result[index]]
                        image.paste(im, (x, y))
                        x += one.size[0]
                        index += 1

                x = 0
                y += one.size[1]


        image = image.resize((int(width*0.17), int(height*0.17)))
        image = ImageTk.PhotoImage(image=image)
        return image
