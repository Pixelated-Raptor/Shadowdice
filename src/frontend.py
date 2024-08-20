#================================================
# Imports
#================================================
import tkinter as tk
from tkinter.messagebox import showerror, showwarning, showinfo
from translate import Translator
from backend import *
from config import config

#================================================
# Setup and Event-Handling
#================================================
app_config = config()

app = tk.Tk()
app.title("Shadowdice")
app.geometry("550x650")
app.resizable(width = False, height = False)
app.option_add("*tearOff", False)
app.columnconfigure(0, weight = 2)
app.rowconfigure(1, weight = 1)
app.columnconfigure(1, weight = 1)
app.columnconfigure(2, weight = 1)

def on_close():
    print("bye")    
    app.destroy()
    
app.protocol("WM_DELETE_WINDOW", on_close)

trans = Translator("../lang")
trans.set_locale(app_config.lang)

edge = tk.IntVar(value = 1)
edge_left = tk.IntVar(value = edge.get())
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
    draw_result(dice_frame, result)

def regain_edge():
    print("Regain 1 Edge")

def pre_edge():
    print("pre edge")

def post_edge():
    print("post edge")

def edge_roll():
    print("edge roll")

def roll_for_edge():
    print("rolling for edge")
    
def reroll_misses():
    print("reroll misses")

def change_language(lang):
    app_config.change_language(lang)    
    trans.set_locale(lang)
    showinfo(message = trans.translate("restart_app"))

#================================================
# UI-Functions
#================================================
def draw_result(frame, result):
    for widget in frame.winfo_children():
        widget.destroy()

    res = ""
    for i in result:
        res = res + str(i) + " "

    tk.Label(master = frame, text = res).grid(column = 0, row = 0)
        
def write_to_history():
    print("todo")
    
#================================================
# Widgets
#================================================
menubar = tk.Menu(app)
app.config(menu = menubar)
menu_options = tk.Menu(menubar)
menubar.add_cascade(menu = menu_options,
                    label = trans.translate("options"))

language_menu = tk.Menu(menu_options, tearoff = 0)
language_menu.add_command(label = trans.translate("english"),
                          command = lambda: change_language("en"))

language_menu.add_command(label = trans.translate("german"),
                          command = lambda: change_language("de"))

menu_options.add_cascade(label = trans.translate("language"), menu = language_menu)

menu_options.add_command(label = trans.translate("game_options"),
                         command = but_func)

your_throw = tk.Label(master = app, text = trans.translate("your_throw"),
                      height = 2, font = big_font)

dice_frame = tk.Frame(master = app, width = 250,
                       borderwidth = 2, relief = "groove")
dice_frame.grid_propagate(0)

# Add validation to only allow numbers
edge_entry = tk.Spinbox(master = app, from_ = 1, to = 99, increment = 1, width = 2,
                        textvariable = edge, font = regular_font)
edge_label = tk.Label(master = app, text = trans.translate("edge"), font = regular_font)
edge_left = tk.Entry(master = app, width = 2, state = "readonly", textvariable = edge_left,
                     font = regular_font)
edge_left_label = tk.Label(master = app, text = trans.translate("edge_left"), font = regular_font)

regain_edge_btn = tk.Button(master = app, text = trans.translate("regain_edge"),
                            command = regain_edge, font = regular_font)

history_frame = tk.Frame(master = app, width = 200, height = 300,
                   borderwidth = 2, relief = "groove")
history_frame.grid_propagate(0)

dice_pool_spinbox = tk.Spinbox(master = app, from_ = 1, to = 99, increment = 1,
                               width = 2, textvariable = dice_pool, 
                               font = regular_font)

throw_btn = tk.Button(master = app, text = trans.translate("throw"), command = throw,
                      font = regular_font)

pre_edge_btn = tk.Button(master = app, text = trans.translate("pre-edge"), command = pre_edge,
                         font = regular_font, width = 12)

post_edge_btn = tk.Button(master = app, text = trans.translate("post-edge"),
                          command = post_edge, font = regular_font, width = 12)

edge_roll_btn = tk.Button(master = app, text = trans.translate("edge-roll"),
                          command = edge_roll, font = regular_font)

roll_for_edge_btn = tk.Button(master = app, text = trans.translate("roll_for_edge"), 
                              command = roll_for_edge, font = regular_font)

reroll_misses_btn = tk.Button(master = app, text = trans.translate("reroll_misses"),
                              command = reroll_misses, font = regular_font)
    
#================================================
# Layout new
#================================================
your_throw.grid(column = 0, row = 0)
dice_frame.grid(column = 0, row = 1, rowspan = 13, sticky = "nsew")
edge_entry.grid(column = 1, row = 1, sticky = "e")
edge_label.grid(column = 2, row = 1, sticky = "w")
edge_left.grid(column = 1, row = 2, sticky = "e")
edge_left_label.grid(column = 2, row = 2, sticky = "w")
regain_edge_btn.grid(column = 1, row = 3, columnspan = 2)
history_frame.grid(column = 1, row = 4, columnspan = 2, rowspan = 4, sticky = "nsew")
dice_pool_spinbox.grid(column = 1, row = 8, sticky = "e")
throw_btn.grid(column = 2, row = 8, sticky = "w")
pre_edge_btn.grid(column = 1, row = 9, columnspan = 2, sticky = "we")
post_edge_btn.grid(column = 1, row = 10, columnspan = 2, sticky = "we")
edge_roll_btn.grid(column = 1, row = 11, columnspan = 2, sticky = "we")
roll_for_edge_btn.grid(column = 1, row = 12, columnspan = 2, sticky = "we")
reroll_misses_btn.grid(column = 1, row = 13, columnspan = 2, sticky = "we")

#================================================
# mainloop
#================================================
app.mainloop()
