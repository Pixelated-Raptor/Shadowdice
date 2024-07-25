#================================================
# Translator Class
# Source: https://phrase.com/blog/posts/python-localization/
#================================================
import json
import glob
import os

class Translator():
    def __init__(self, translation_folder, default_locale='en'):
        self.data = {}
        self.locale = 'en'

        files = glob.glob(os.path.join(translation_folder, f'*.json'))
        for file in files:
            loc = os.path.splitext(os.path.basename(file))[0]

            with open(file, mode='r', encoding='utf8') as f:
                self.data[loc] = json.load(f)

    def set_locale(self, loc):
        if loc in self.data:
            self.locale = loc
        else:
            print('Invalid locale')

    def get_locale(self):
        return self.locale

    def translate(self, key):
        if self.locale not in self.data:
            return key

        text = self.data[self.locale].get(key, key)

        return text        

