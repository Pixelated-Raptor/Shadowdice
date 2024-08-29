#================================================
# Class for the frontend of Shadowdice.
# Handles Rendering and Events
#================================================

import tkinter as tk
from tkinter.messagebox import showerror, showwarning, showinfo
from translate import Translator
from backend import backend
from config import config
from gameplayoptions_window import gameplayoptions

class frontend():
    app_config = None; app = None
    trans = None; edge_attribut = None
    edge_left = None; dice_pool = None
    result = None;

    big_font = ("Arial", 16)
    regular_font = ("Arial", 12)

    gameplayoptions = None
    logic = None

    # Widgets
    menubar = None; menu_options = None
    language_menu = None; your_throw = None
    dice_frame = None; edge_attribut_spin = None    
    edge_attribut_label = None; edge_left_entry = None
    edge_left_label = None; regain_edge_btn = None
    history_frame = None; dice_pool_spin = None
    throw_btn = None; pre_edge_btn = None
    post_edge_btn = None; edge_roll_btn = None
    roll_for_edge_btn = None; reroll_misses_btn = None
    
    def __init__(self):
        self.app_config = config()

        self.trans = Translator("../lang")
        self.trans.set_locale(self.app_config.lang)

        self.app = tk.Tk()
        self.app.title("Shadowdice")
        self.app.geometry("550x650")
        self.app.resizable(width=False, height=False)
        self.app.option_add("*tearOff", False)
        self.app.columnconfigure(0, weight=2)
        self.app.rowconfigure(1, weight=1)
        self.app.columnconfigure(1, weight=1)
        self.app.columnconfigure(2, weight=1)
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

        self.logic = backend()
        self.gameplayoptions = gameplayoptions(self.app, self.trans, self.app_config)
        
        self.edge_attribut = tk.IntVar(value=self.app_config.edge)
        self.edge_left = tk.IntVar(value=self.app_config.edge_left)
        self.dice_pool = tk.IntVar(value=1)
    
    def on_close(self):
        self.app_config.write_on_close(self.edge_attribut.get(), self.edge_left.get())
        self.app.destroy()

    def placeholder_func(self):
        print("Button pressed")

    def throw(self):
        self.result = self.logic.throw(self.dice_pool.get())        
        print(self.result)
        print(self.logic.evaluate_roll(self.result, self.app_config.hits,
                                       self.app_config.misses))
        print("---")
        self.draw_result()
        
    def regain_edge(self):
        if self.edge_left.get() < self.edge_attribut.get():
            self.edge_left.set(self.edge_left.get() + 1)
        elif self.edge_left.get() > self.edge_attribut.get():
            self.edge_left.set(self.edge_attribut.get())

    def pre_edge(self):
        print("pre edge")

    def post_edge(self):
        print("post edge")

    def edge_roll(self):
        if(self.edge_left.get() > 0):
            self.result = self.logic.edge_roll(
                self.app_config.use_full_edge,
                self.edge_attribut.get(),
                self.edge_left.get()
            )
            self.logic.evaluate_roll(
                self.result,
                self.app_config.hits,
                self.app_config.misses
            )
            self.edge_left.set(self.edge_left.get() - 1)
            
            print(self.result)
            print(self.logic.evaluate_roll(self.result, self.app_config.hits,
                                       self.app_config.misses))
            print("---")
            self.draw_result()
        
    def roll_for_edge(self):
        #In cases when the Gamemaster wants to know how lucky
        #the player is. Does not consume edge.
        self.result = self.logic.roll_for_edge(self.edge_attribut.get())
        self.logic.evaluate_roll(self.result,
                                 self.app_config.hits,
                                 self.app_config.misses)
        
        print(self.result)
        print(self.logic.evaluate_roll(self.result, self.app_config.hits,
                                       self.app_config.misses))
        print("---")
        self.draw_result()
            
    def reroll_misses(self):
        #Only allow rerolling if there are any misses
        hits = 0
        for x in self.app_config.hits:
            hits += self.result.count(x)

        if(hits != len(self.result)):        
            if(self.edge_left.get() > 0):
                #Extract hits from current pool as to not lose them
                temp = [x for x in self.result if x in self.app_config.hits] 
                
                self.result = self.logic.reroll_misses(self.result, self.app_config.hits)
                self.logic.evaluate_roll(self.result,
                                         self.app_config.hits,
                                         self.app_config.misses)
                self.result = temp + self.result
                self.edge_left.set(self.edge_left.get() - 1)
                
                print(self.result)
                print(self.logic.evaluate_roll(self.result, self.app_config.hits,
                                               self.app_config.misses))
                print("---")
                self.draw_result()

    def change_language(self, lang):
        self.app_config.change_language(lang)
        self.trans.set_locale(lang)
        showinfo(message=self.trans.translate("restart_app"))

    def spawn_gameplayoptions(self):
        #spawn_gameplayoptions_window(self.app, self.trans, self.app_config)
        self.gameplayoptions.spawn_gameplayoptions()

    ###########################################################################
    def init_widgets(self):
        self.menubar = tk.Menu(self.app)
        self.app.config(menu=self.menubar)
        self.menu_options = tk.Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_options,
                                 label=self.trans.translate("options"))
        self.language_menu = tk.Menu(self.menu_options, tearoff=0)
        self.language_menu.add_command(label=self.trans.translate("english"),
                                       command=lambda: self.change_language("en"))
        self.language_menu.add_command(label=self.trans.translate("german"),
                                       command=lambda: self.change_language("de"))
        self.menu_options.add_cascade(label=self.trans.translate("language"),
                                      menu=self.language_menu)
        self.menu_options.add_command(label=self.trans.translate("game_options"),
                                      command=self.spawn_gameplayoptions)
        self.your_throw = tk.Label(master=self.app, text=self.trans.translate("your_throw"),
                                   height=2, font=self.big_font)
        self.dice_frame = tk.Frame(master=self.app, width=250,
                                   borderwidth=2, relief="groove")
        self.dice_frame.grid_propagate(0)
        self.edge_attribut_spin = tk.Spinbox(master=self.app, from_=1, to=99,
                                             increment=1, width=2,
                                             textvariable=self.edge_attribut,
                                             font=self.regular_font)
        self.edge_attribut_label = tk.Label(master=self.app,
                                            text=self.trans.translate("edge"),
                                            font=self.regular_font)
        self.edge_left_entry = tk.Entry(master=self.app, width=2, state="readonly",
                                        textvariable=self.edge_left, font=self.regular_font)
        self.edge_left_label = tk.Label(master=self.app, text=self.trans.translate("edge_left"),
                                        font=self.regular_font)
        self.regain_edge_btn = tk.Button(master=self.app,
                                         text=self.trans.translate("regain_edge"),
                                         command=self.regain_edge, font=self.regular_font)
        self.history_frame = tk.Frame(master=self.app, width=200, height=300,
                                      borderwidth=2, relief="groove")
        self.history_frame.grid_propagate(0)
        self.dice_pool_spin = tk.Spinbox(master=self.app, from_=1, to=99, increment=1,
                                         width=2, textvariable=self.dice_pool,
                                         font=self.regular_font)
        self.throw_btn = tk.Button(master=self.app, text=self.trans.translate("throw"),
                                   command=self.throw, font=self.regular_font)
        self.pre_edge_btn = tk.Button(master=self.app, text=self.trans.translate("pre-edge"),
                                      command=self.pre_edge, font=self.regular_font, width=12)
        self.post_edge_btn = tk.Button(master=self.app, text=self.trans.translate("post-edge"),
                                       command=self.post_edge, font=self.regular_font)
        self.edge_roll_btn = tk.Button(master=self.app, text=self.trans.translate("edge-roll"),
                                       command=self.edge_roll, font=self.regular_font)
        self.roll_for_edge_btn = tk.Button(master=self.app,
                                           text=self.trans.translate("roll_for_edge"),
                                           command=self.roll_for_edge, font=self.regular_font)
        self.reroll_misses_btn = tk.Button(master=self.app,
                                           text=self.trans.translate("reroll_misses"),
                                           command=self.reroll_misses, font=self.regular_font)
        
        
    def layout(self):
        self.your_throw.grid(column = 0, row = 0)
        self.dice_frame.grid(column = 0, row = 1, rowspan = 13, sticky = "nsew")
        self.edge_attribut_spin.grid(column = 1, row = 1, sticky = "e")
        self.edge_attribut_label.grid(column = 2, row = 1, sticky = "w")
        self.edge_left_entry.grid(column = 1, row = 2, sticky = "e")
        self.edge_left_label.grid(column = 2, row = 2, sticky = "w")
        self.regain_edge_btn.grid(column = 1, row = 3, columnspan = 2)
        self.history_frame.grid(column = 1, row = 4, columnspan = 2, rowspan = 4, sticky = "nsew")
        self.dice_pool_spin.grid(column = 1, row = 8, sticky = "e")
        self.throw_btn.grid(column = 2, row = 8, sticky = "w")
        self.pre_edge_btn.grid(column = 1, row = 9, columnspan = 2, sticky = "we")
        self.post_edge_btn.grid(column = 1, row = 10, columnspan = 2, sticky = "we")
        self.edge_roll_btn.grid(column = 1, row = 11, columnspan = 2, sticky = "we")
        self.roll_for_edge_btn.grid(column = 1, row = 12, columnspan = 2, sticky = "we")
        self.reroll_misses_btn.grid(column = 1, row = 13, columnspan = 2, sticky = "we")
        
    def draw_result(self):
        for widget in self.dice_frame.winfo_children():
            widget.destroy()

        res = ""
        for i in self.result:
            res = res + str(i) + " "

        tk.Label(master=self.dice_frame, text=res).grid(column = 0, row = 0)
        
    def write_to_history(self):
        print("todo")
        
    ###########################################################################
    def start(self):
        self.init_widgets()
        self.layout()
        self.app.mainloop()
        
############################################
front = frontend()
front.start()
