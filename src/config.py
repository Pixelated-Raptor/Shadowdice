import configparser
from os.path import exists

class config():
    """
    Class for creating and interacting with the Shadowdice config file.
    
    Based on: https://www.geeksforgeeks.org/how-to-write-a-configuration-file-in-python/
    """
    CONFIG_NAME = "Shadowdice_config.ini"
    lang = ""
    edge = 1
    edge_left = edge
    hits = []
    misses = []
    use_full_edge = None
    dice_style = None    
    dice_style_options = ["dotted", "dotted coloured", "numbered", "numbered coloured"]
    
    def __init__(self):
        """ Create a new config file if none is found. """
        if exists(self.CONFIG_NAME):
            self.read_config()
        else:
            self.create_config()

    def change_language(self, lang):
        """ Change the language and write it to the config. """
        conf = configparser.ConfigParser()
        conf.read(self.CONFIG_NAME)

        conf["Locale"]["language"] = lang
        with open(self.CONFIG_NAME, "w") as f:
            conf.write(f)
    
    def create_config(self):
        """ Creates a default config file. """
        new_config = configparser.ConfigParser()

        new_config["Locale"] = {"language": "en"}
        new_config["Die"] = {
            "dice style": "Dotted"
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
        """
        Read the config and load settings into memory.
        Assume defaults if config file has been messed with.
        """
        config = configparser.ConfigParser()
        try:
            config.read(self.CONFIG_NAME)
        except:
            self.create_config()
            
        # Translator class checks for plausibility and assumes english as default
        self.lang = config["Locale"]["language"]
        
        self.dice_style = config["Die"]["dice style"]
        if self.dice_style not in self.dice_style_options:
            self.dice_style = self.dice_style_options[0]
        
        self.edge = config["Gameplay"]["edge"]
        try:
            self.edge = int(self.edge)
        except:
            self.edge = 3
            
        self.edge_left = config["Gameplay"]["edge left"]
        try:
            self.edge_left = int(self.edge_left)
        except:
            self.edge_left = 3
            
        # Edge left cannot be higher than the edge attribut
        if self.edge_left > self.edge:
            self.edge_left = self.edge
            
        self.use_full_edge = config["Gameplay"]["use full edge"]
        self.use_full_edge = bool(False) if self.use_full_edge == "False" else bool(True)
        
        # Hits and Misses need to be converted back to int
        try:
            self.hits = list(config["Gameplay"]["hits"].split(","))
            self.hits = [int(x) for x in self.hits]
        except:
            self.hits = [5, 6]

        try:
            self.misses = list(config["Gameplay"]["misses"].split(","))
            self.misses = [int(x) for x in self.misses]
        except:
            self.misses = [1]


    def write_on_close(self, edge, edge_left):
        """ Write parts of the config when Shadowdice is closed. """
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

    def hit_on_4(self, checked):
        """ Changes wether or not 4 is counted as a hit. """
        if(4 in self.hits):
            self.hits.remove(4)
        else:
            self.hits.append(4)
            
    def miss_on_2(self, checked):
        """ Changes wether or not 2 is counted as a miss. """
        if(2 in self.misses):
            self.misses.remove(2)
        else:
            self.misses.append(2)

    def edge_usage(self, state):
        """
        Changes wether any edge action uses the full edge
        attribut or only the edge left.
        """
        if(type(state.get()) is bool):
            self.use_full_edge = state.get()
        else:
            self.use_full_edge = True

    def change_die_style(self, style):
        """ Changes the looks of the die. """
        self.dice_style = style
