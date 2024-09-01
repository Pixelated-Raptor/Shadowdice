#================================================
# Class for the Optionswindow of Shadowdice.
# Toggles additional gameplayoptions.
#================================================
import tkinter as tk
from translate import Translator
from backend import *
from config import config

class gameplayoptions():
    win = None; hits4_check = None
    miss2_check = None; app_config = None
    trans = None; master = None;
    hits4_state = None; miss2_state = None
    use_full_edge_state = None
    use_full_edge_check = None
    die_style_label = None
    die_style_listbox = None

    big_font = ("Arial", 16)
    regular_font = ("Arial", 12)

    def __init__(self, master, trans, config):
        self.app_config = config
        self.trans = trans
        self.master = master
        
        self.hits4_state = tk.BooleanVar(master=self.win)
        self.miss2_state = tk.BooleanVar(master=self.win)
        self.use_full_edge_state = tk.BooleanVar(master=self.win)

        # Checks the checkboxes if these were activated before
        if(4 in self.app_config.hits):
            self.hits4_state.set(1)
        else:
            self.hits4_state.set(0)

        if(2 in self.app_config.misses):
            self.miss2_state.set(1)
        else:
            self.miss2_state.set(0)

        if(self.app_config.use_full_edge):
            self.use_full_edge_state.set(1)
        else:
            self.use_full_edge_state.set(0)
        
    def hit_on_4(self):
        self.app_config.hit_on_4(self.hits4_state.get())

    def miss_on_2(self):
        self.app_config.miss_on_2(self.miss2_state.get())

    def use_full_edge(self):
        self.app_config.edge_usage(self.use_full_edge_state)

    def change_die_style(self, die_list, selection):
        self.app_config.change_die_style(
            self.app_config.dice_style_options[selection[0]]
        )

    def spawn_gameplayoptions(self):
        self.win = tk.Toplevel(self.master)
        self.win.title(self.trans.translate("game_options"))
        self.win.geometry("400x400")
        self.win.resizable(width=False, height=False)

        self.win.columnconfigure(0, weight=1)

        self.init_widgets()
        self.layout()

    def init_widgets(self):
        die_dict = {
            self.app_config.dice_style_options[0]: self.trans.translate("dotted"),
            self.app_config.dice_style_options[1]: self.trans.translate("dotted_coloured"),
            self.app_config.dice_style_options[2]: self.trans.translate("numbered"),
            self.app_config.dice_style_options[3]: self.trans.translate("numbered_coloured"),
        }
        die_list_trans = []
        for x in die_dict:
            die_list_trans.append(die_dict[x])

        #Conversion needed for usage in a listbox
        die_list_StringVar = tk.StringVar(value=die_list_trans)
        
        self.hits4_check = tk.Checkbutton(master=self.win, text=self.trans.translate("count_4"),
                                          command=self.hit_on_4,
                                          variable=self.hits4_state,
                                          font=self.regular_font)
        self.miss2_check = tk.Checkbutton(master=self.win, text=self.trans.translate("count_2"),
                                          command=self.miss_on_2,
                                          variable=self.miss2_state,
                                          font=self.regular_font)
        self.use_full_edge_check = tk.Checkbutton(master=self.win, 
                                                  text=self.trans.translate("use_full_edge"),
                                                  command=self.use_full_edge,
                                                  variable=self.use_full_edge_state,
                                                  font=self.regular_font)
        self.die_style_label = tk.Label(master=self.win,
                                        text=self.trans.translate("choose_style"),
                                        font=self.regular_font)
        self.die_style_listbox = tk.Listbox(master=self.win, height=4,
                                            listvariable=die_list_StringVar,
                                            font=self.regular_font)
        self.die_style_listbox.select_set(0)
        self.die_style_listbox.bind("<<ListboxSelect>>", lambda x: self.change_die_style(
                                    die_list_trans,
                                    self.die_style_listbox.curselection())) 
        
    def layout(self):
        self.hits4_check.grid(column=0, row=0, stick="w")
        self.miss2_check.grid(column=0, row=1, stick="w")
        self.use_full_edge_check.grid(column=0, row=2, stick="w")
        self.die_style_label.grid(column=0, row=3, stick="w")
        self.die_style_listbox.grid(column=0, row=4, stick="w")
