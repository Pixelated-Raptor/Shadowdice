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
        new_config["Gameplay"] = {
            "edge": 1,
            "edge left": 1
        }

        with open(self.CONFIG_NAME, "w") as f:
            new_config.write(f)

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_NAME)
        
        self.lang = config["Locale"]["language"]
        self.edge = config["Gameplay"]["edge"]
        self.edge_left = config["Gameplay"]["edge left"]

        #Plausibility Checks
        if self.edge_left > self.edge:
            self.edge_left = self.edge

    def write_on_close(self, edge, edge_left):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_NAME)

        config["Gameplay"]["edge"] = str(edge)
        config["Gameplay"]["edge left"] = str(edge_left)

        with open(self.CONFIG_NAME, "w") as f:
            config.write(f)
    
    def restore_defaults(self):
        print("ToDo")
