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

edge = 1
edge_left = 1
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

but = tk.Button(master = app,
                text = trans.translate("throw"),
                command = but_func)

#================================================
# Layout
#================================================
but.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)
your_throw.grid(column = 0, row = 0)
dice_frame.grid(column = 0, row = 1, rowspan = 8)
edge_entry.grid(column = 2, row = 1)
edge_label.grid(column = 3, row = 1)
edge_left.grid(column = 2, row = 2)
edge_left_label.grid(column = 3, row = 2)
#history_frame.grid(column = 2, row = 3)

#================================================
# mainloop
#================================================
app.mainloop()
