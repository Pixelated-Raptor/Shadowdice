#================================================
# Imports
#================================================
import tkinter as tk
from translate import Translator

#================================================
# Setup
#================================================
app = tk.Tk()
app.title("Shadowdice")
app.geometry("450x600")
app.resizable(width = False, height = False)
app.option_add("*tearOff", False)

trans = Translator("../lang")
trans.set_locale("de")

edge = ""
edge_left = ""
dice_pool = ""
#================================================
# Buttonfunctions
#================================================
def but_func():
    print("Button pressed")

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

your_throw = tk.Label(text = trans.translate("your_throw"))

dice_frame = tk.Frame(width = 200, height = 550,
                      borderwidth = 2, relief = "groove")

# Add validation to only allow numbers
edge_entry = tk.Entry(width = 2, textvariable = edge)
edge_label = tk.Label(text = trans.translate("edge"))

edge_left = tk.Entry(width = 2, state = "readonly", textvariable = edge_left)
edge_left_label = tk.Label(text = trans.translate("edge_left"))

history_frame = tk.Frame(width = 200, height = 200,
                   borderwidth = 2, relief = "groove")

dice_pool_up_btn = tk.Button(text = "up", command = but_func)
dice_pool_entry = tk.Entry(width = 2, textvariable = dice_pool)
dice_pool_down_btn = tk.Button(text = "down", command = but_func)
throw_btn = tk.Button(text = trans.translate("throw"), command = but_func)

pre_edge_btn = tk.Button(text = trans.translate("pre-edge"), command = but_func)
post_edge_btn = tk.Button(text = trans.translate("post-edge"), command = but_func)

edge_roll_btn = tk.Button(text = trans.translate("edge-roll"), command = but_func)
reroll_misses_btn = tk.Button(text = trans.translate("reroll_misses"), command = but_func)

but = tk.Button(master = app,
                text = trans.translate("throw"),
                command = but_func)

#================================================
# Layout
#================================================
#but.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
your_throw.grid(column = 0, row = 0)
dice_frame.grid(column = 0, row = 1, rowspan = 8)
edge_entry.grid(column = 2, row = 1)
edge_label.grid(column = 3, row = 1)
edge_left.grid(column = 2, row = 2)
edge_left_label.grid(column = 3, row = 2)
history_frame.grid(column = 3, row = 3)
dice_pool_up_btn.grid(column = 2, row = 4)
dice_pool_entry.grid(column = 2, row = 5)
throw_btn.grid(column = 3, row = 5)
dice_pool_down_btn.grid(column = 2, row = 6)
pre_edge_btn.grid(column = 2, row = 7)
post_edge_btn.grid(column = 3, row = 7)
edge_roll_btn.grid(column = 2, row = 8)
reroll_misses_btn.grid(column = 2, row = 9)

#================================================
# mainloop
#================================================
app.mainloop()
