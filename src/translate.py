import json
import glob
import os
from string import Template

class Translator():
    """
    Class used for translating text in Shadowdice.

    Translations are found in json files.
    Based on: https://phrase.com/blog/posts/python-localization/ 
    """
    def __init__(self, translation_folder, default_locale="en"):
        self.data = {}
        self.locale = "en"

        files = glob.glob(os.path.join(translation_folder, f"*.json"))
        for file in files:
            loc = os.path.splitext(os.path.basename(file))[0]

            with open(file, mode="r", encoding="utf8") as f:
                self.data[loc] = json.load(f)

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            self.locale = "en"

    def get_locale(self):
        return self.locale

    def translate(self, key, **kwargs):
        if self.locale not in self.data:
            return key

        text = self.data[self.locale].get(key, key)

        return Template(text).safe_substitute(**kwargs)
