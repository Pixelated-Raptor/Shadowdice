#================================================
# Class for creating and interacting with the
# Shadowdice Config file
# Source: https://www.geeksforgeeks.org/how-to-write-a-configuration-file-in-python/
#================================================
import configparser
from os.path import exists

class config():
    CONFIG_NAME = "Shadowdice_config.ini"
    lang = ""
    edge = 1
    edge_left = edge
    hits = []
    misses = []
    use_full_edge = None
    dice_style = None    
    dice_style_options = ["dotted", "dotted coloured", "numbered", "numbered coloured"]
    highlight_hits = None
    highlight_misses = None
    
    def __init__(self):
        if exists(self.CONFIG_NAME):
            self.read_config()
        else:
            self.create_config()

    def change_language(self, lang):
        conf = configparser.ConfigParser()
        conf.read(self.CONFIG_NAME)

        conf["Locale"]["language"] = lang
        with open(self.CONFIG_NAME, "w") as f:
            conf.write(f)
    
    def create_config(self):
        new_config = configparser.ConfigParser()

        new_config["Locale"] = {"language": "en"}
        new_config["Die"] = {
            "dice style": "Dotted",
            "highlight hits": "False",
            "highlight misses": "False"
        }
        new_config["Gameplay"] = {
            "edge": 1,
            "edge left": 1,
            "use full edge": "True",
            "hits": "5,6",
            "misses": "1"
        }

        with open(self.CONFIG_NAME, "w") as f:
            new_config.write(f)

        self.read_config()

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_NAME)
        
        self.lang = config["Locale"]["language"]
        
        self.dice_style = config["Die"]["dice style"]
        
        self.highlight_hits = config["Die"]["highlight hits"]
        self.highlight_hits = bool(False) if self.highlight_hits == "False" else bool(True)
        self.highlight_misses = config["Die"]["highlight misses"]
        self.highlight_misses = bool(False) if self.highlight_misses == "False" else bool(True)
        
        self.edge = int(config["Gameplay"]["edge"])
        self.edge_left = int(config["Gameplay"]["edge left"])
        self.use_full_edge = config["Gameplay"]["use full edge"]
        self.use_full_edge = bool(False) if self.use_full_edge == "False" else bool(True)
        
        # Hits and Misses need to be converted back to int
        self.hits = list(config["Gameplay"]["hits"].split(","))
        self.hits = [int(x) for x in self.hits]
        self.misses = list(config["Gameplay"]["misses"].split(","))
        self.misses = [int(x) for x in self.misses]

        #Plausibility Checks
        if self.edge_left > self.edge:
            self.edge_left = self.edge

    def write_on_close(self, edge, edge_left):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_NAME)

        config["Die"]["dice style"] = self.dice_style
        config["Gameplay"]["edge"] = str(edge)
        config["Gameplay"]["edge left"] = str(edge_left)
        config["Gameplay"]["use full edge"] = str(self.use_full_edge)
        config["Gameplay"]["hits"] = ",".join([str(x) for x in self.hits])
        config["Gameplay"]["misses"] = ",".join([str(x) for x in self.misses])

        with open(self.CONFIG_NAME, "w") as f:
            config.write(f)
    
    def restore_defaults(self):
        print("ToDo")

    def hit_on_4(self, checked):
        if(4 in self.hits):
            self.hits.remove(4)
        else:
            self.hits.append(4)
            
    def miss_on_2(self, checked):
        if(2 in self.misses):
            self.misses.remove(2)
        else:
            self.misses.append(2)

    def edge_usage(self, state):
        if(type(state.get()) is bool):
            self.use_full_edge = state.get()
        else:
            self.use_full_edge = True

    def change_die_style(self, style):
        print(style)
        self.dice_style = style
