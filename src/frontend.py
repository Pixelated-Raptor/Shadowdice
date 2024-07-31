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

but = tk.Button(master = app,
                text = trans.translate("throw"),
                command = but_func)

#================================================
# Layout
#================================================
but.place(relx = 0.5, rely = 0.5, anchor = tk.CENTER)

#================================================
# mainloop
#================================================
app.mainloop()
