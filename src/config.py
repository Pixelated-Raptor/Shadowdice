#================================================
# Class for creating and interacting with the
# Shadowdice Config file
# Source: https://www.geeksforgeeks.org/how-to-write-a-configuration-file-in-python/
#================================================
import configparser
from os.path import exists

class config():
    CONFIG_NAME = "Shadowdice_config.ini"
    
    def __init__(self):
        if exists(self.CONFIG_NAME):
            print("Exists")    
        else:
            self.create_config()

    def create_config(self):
        new_config = configparser.ConfigParser()

        new_config["Locale"] = {"language": "en"}
        new_config["Gameplay"] = {
            "bla": "blub"
        }

        with open(self.CONFIG_NAME, "w") as f:
            new_config.write(f)
