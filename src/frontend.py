#================================================
# Imports
#================================================
import tkinter as tk
from translate import Translator
from backend import *

#================================================
# Setup
#================================================
app = tk.Tk()
app.title("Shadowdice")
app.geometry("550x650")
app.resizable(width = False, height = False)
app.option_add("*tearOff", False)

trans = Translator("../lang")
trans.set_locale("de")

edge = ""
edge_left = ""
dice_pool = tk.IntVar(value = 1)

big_font = ("Arial", 16)
regular_font = ("Arial", 12)
#================================================
# Buttonfunctions
#================================================
def but_func():
    print("Button pressed")

def throw():
    result = bk_throw(dice_pool.get())
    print(result)
    print(evaluate_roll(result))
    print("---")

def pre_edge():
    print("pre edge")

def post_edge():
    print("post edge")

def edge_roll():
    print("edge roll")
    
def reroll_misses():
    print("reroll misses")
    
#================================================
# Widgets
#================================================
menubar = tk.Menu(app)
app.config(menu = menubar)
menu_options = tk.Menu(menubar)
menubar.add_cascade(menu = menu_options,
                    label = trans.translate("options"))

menu_options.add_command(label = trans.translate("language"), 
                         command = but_func)

your_throw = tk.Label(text = trans.translate("your_throw"), height = 2, font = big_font)
dice_frame = tk.Frame(width = 250, height = 500,
                      borderwidth = 2, relief = "groove")

# Add validation to only allow numbers
edge_entry = tk.Entry(width = 2, textvariable = edge, font = regular_font)
edge_label = tk.Label(text = trans.translate("edge"), font = regular_font)
edge_left = tk.Entry(width = 2, state = "readonly", textvariable = edge_left,
                     font = regular_font)
edge_left_label = tk.Label(text = trans.translate("edge_left"), font = regular_font)

history_frame = tk.Frame(width = 200, height = 200,
                   borderwidth = 2, relief = "groove")

dice_pool_spinbox = tk.Spinbox(from_ = 1, to = 99, increment = 1,
                               width = 2, textvariable = dice_pool, 
                               font = regular_font)

throw_btn = tk.Button(text = trans.translate("throw"), command = throw,
                      font = regular_font)

pre_edge_btn = tk.Button(text = trans.translate("pre-edge"), command = pre_edge,
                         font = regular_font, width = 12)
post_edge_btn = tk.Button(text = trans.translate("post-edge"), command = post_edge,
                          font = regular_font, width = 12)

edge_roll_btn = tk.Button(text = trans.translate("edge-roll"), command = edge_roll,
                          font = regular_font)
reroll_misses_btn = tk.Button(text = trans.translate("reroll_misses"), command = reroll_misses,                            font = regular_font)

#================================================
# Layout
#================================================
your_throw.grid(column = 0, row = 0)
dice_frame.grid(column = 0, row = 1, rowspan = 11)
edge_entry.grid(column = 1, row = 1)
edge_label.grid(column = 2, row = 1, sticky = "w")
edge_left.grid(column = 1, row = 2)
edge_left_label.grid(column = 2, row = 2, sticky = "w")
history_frame.grid(column = 1, row = 3, rowspan = 4, columnspan = 2)
dice_pool_spinbox.grid(column = 1, row = 7, sticky = "e")
throw_btn.grid(column = 2, row = 7, sticky = "w")
pre_edge_btn.grid(column = 1, row = 8, stick = "ew")
post_edge_btn.grid(column = 2, row = 8, stick = "ew")
edge_roll_btn.grid(column = 1, row = 9, rowspan = 2, columnspan = 2, sticky = "ew")
reroll_misses_btn.grid(column = 1, row = 10, rowspan = 2, columnspan = 2, sticky = "ew")

#================================================
# mainloop
#================================================
app.mainloop()
