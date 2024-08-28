import tkinter as tk
from translate import Translator
from backend import *
from config import config

def spawn_gameplayoptions_window(master, trans, config):
    win = tk.Toplevel(master)
    win.title(trans.translate("game_options"))
    win.geometry("400x400")

    hits4_checkbox = tk.Checkbutton(win, text = trans.translate("count_4"),
                                    command = hit_on_4,
                                    variable = hits4,
                                    ).grid(column = 0, row = 0 )

    misses2_checkbox = tk.Checkbutton(win, text = trans.translate("count_2"),
                                      command = miss_on_2).grid(column = 0, row = 1)

def hit_on_4():
    print("hi")

def miss_on_2():
    print("hi")
