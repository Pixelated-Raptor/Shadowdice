import tkinter as tk
from tkinter.messagebox import showerror, showwarning, showinfo
from translate import Translator
from backend import backend
from config import config
from gameplayoptions_window import gameplayoptions
import re

class Shadowdice():
    """
    Main class of Shadowdice. Handles GUI and a bit of logic.

    Delegates most of the logic to backend.py
    Delegates gameplay options to gameplayoptions_window.py
    Delegates persistent saving of options to config.py 
    Delegates UI-Text and translations to translate.py
    """

    # Other custom classes
    app_config = None; trans = None
    gameplayoptions = None; logic = None

    # Read from config at startup    
    edge_attribut = None
    edge_left = None; 
    
    # Shadowdice itself
    app = None
    
    # Additional variables and constants for the UI
    dice_pool = None
    result = None;

    big_font = ("Arial", 16)
    regular_font = ("Arial", 12)

    HISTORY_SIZE = 12
    TRANSLATION_PATH = "_internal/lang"
    ICON = "_internal/Assets/icon.ico"
    
    # Widgets
    menubar = None; menu_options = None
    language_menu = None; your_throw = None
    dice_canvas = None; edge_attribut_spin = None    
    edge_attribut_label = None; edge_left_entry = None
    edge_left_label = None; regain_edge_btn = None
    history_frame = None; dice_pool_spin = None
    throw_btn = None; pre_edge_btn = None
    post_edge_btn = None; edge_roll_btn = None
    roll_for_edge_btn = None; reroll_misses_btn = None
    die_image = None; dice_canvas_scrollbar = None
    summary = []

    # To make sure only numbers are entered into entries
    validate = None
    
    def __init__(self):
        self.app_config = config()
        self.trans = Translator(self.TRANSLATION_PATH)
        self.trans.set_locale(self.app_config.lang)
        self.app = tk.Tk()
        self.app.title("Shadowdice")
        self.app.iconbitmap(self.ICON)
        self.app.geometry("600x650")
        self.app.resizable(width=False, height=False)
        self.app.option_add("*tearOff", False)
        self.app.columnconfigure(0, weight=2)
        self.app.rowconfigure(1, weight=1)
        self.app.columnconfigure(2, weight=1)
        self.app.columnconfigure(3, weight=1)
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)

        self.validate = (self.app.register(self.validate_entry), "%P")
        
        self.logic = backend()
        self.gameplayoptions = gameplayoptions(self.app, self.trans, self.app_config)
        
        self.edge_attribut = tk.IntVar(value=self.app_config.edge)
        self.edge_left = tk.IntVar(value=self.app_config.edge_left)
        self.dice_pool = tk.IntVar(value=6)
    
    def on_close(self):
        """ Writes the current state of edge to the config file. """
        self.app_config.write_on_close(self.edge_attribut.get(), self.edge_left.get())
        self.app.destroy()

    def throw(self):
        """ Throw as many dice as there are in the pool and then write the result. """
        self.result = self.logic.throw(self.dice_pool.get())        
        self.draw_result()
        
    def regain_edge(self):
        """ Increment the edge left without going above the full edge attribut. """
        
        if self.edge_left.get() < self.edge_attribut.get():
            self.edge_left.set(self.edge_left.get() + 1)
            self.grey_out_button()
        elif self.edge_left.get() > self.edge_attribut.get():
            self.edge_left.set(self.edge_attribut.get())

    def pre_edge(self):
        """ Throws a new pool of dice with additional edge dice. """
        #Set your dice pool, then click pre edge to throw with edge dice
        if(self.edge_left.get() > 0):
            self.result = self.logic.pre_edge(
                            self.app_config.use_full_edge,
                            self.dice_pool.get(),
                            self.edge_attribut.get(),
                            self.edge_left.get())

            self.edge_left.set(self.edge_left.get() - 1)

            self.grey_out_button()
            
            self.draw_result()

    def post_edge(self):
        """
        Throws edge die after a pool has been thrown and adding
        the result to the original diepool.
        """
        if(self.edge_left.get() > 0):
            self.result += self.logic.post_edge(
                                self.app_config.use_full_edge,
                                self.edge_attribut.get(),
                                self.edge_left.get())

            self.edge_left.set(self.edge_left.get() - 1)

            self.grey_out_button()
            
            self.draw_result()

    def edge_roll(self):
        """ Only throw the edge die. Consumes edge. """
        if(self.edge_left.get() > 0):
            self.result = self.logic.edge_roll(
                            self.app_config.use_full_edge,
                            self.edge_attribut.get(),
                            self.edge_left.get())
            
            self.logic.evaluate_roll(
                            self.result,
                            self.app_config.hits,
                            self.app_config.misses
            )
            self.edge_left.set(self.edge_left.get() - 1)

            self.grey_out_button()
            
            self.draw_result()
        
    def roll_for_edge(self):
        """
        Throw a pool equal to your full edge attribut.
        Exploding sixes are not applied here.
        Does not consume edge.
        """
        self.result = self.logic.roll_for_edge(self.edge_attribut.get())
        self.logic.evaluate_roll(self.result,
                                 self.app_config.hits,
                                 self.app_config.misses)
        
        self.draw_result()
            
    def reroll_misses(self):
        """
        If there are any dice that are not a hit in the result,
        reroll them.
        """
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
                
                self.grey_out_button()
                    
                self.draw_result()

    def change_language(self, lang):
        """ Changes the language and redraws the UI. """
        self.app_config.change_language(lang)
        self.trans.set_locale(lang)
        for widget in self.app.winfo_children():
            widget.destroy()

        self.init_widgets()
        self.layout()

    def spawn_gameplayoptions(self):
        self.gameplayoptions.spawn_gameplayoptions()

    def bind_to_mousewheel(self, event):
        self.dice_canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def unbind_from_mousewheel(self, event):
        self.dice_canvas.unbind_all("<Mousewheel>")

    def on_mousewheel(self, event):
        #Source: https://stackoverflow.com/a/37858368
        self.dice_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def validate_entry(self, input):
        """ Validated that user input is a number. """
        pattern = r"[1-9][0-9]?"

        if re.fullmatch(pattern, input) is None:
            return False

        return True

    def on_invalid_entry(self, entry):
        """ Color text red on invalid input. """
        entry["foreground"] = "red"

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
        self.dice_canvas = tk.Canvas(master=self.app, width=250, background="white",
                                   borderwidth=2, relief="groove", 
                                   scrollregion=(0, 0, 3325, 3325))
        self.dice_canvas_scrollbar = tk.Scrollbar(master=self.app, orient=tk.VERTICAL, command=self.dice_canvas.yview)
        self.dice_canvas["yscrollcommand"] = self.dice_canvas_scrollbar.set
        self.dice_canvas.bind("<Enter>", self.bind_to_mousewheel)
        self.dice_canvas.bind("<Leave>", self.unbind_from_mousewheel)
        self.dice_canvas.grid_propagate(0)
        self.edge_attribut_spin = tk.Spinbox(master=self.app, from_=1, to=99,
                                             increment=1, width=2,
                                             textvariable=self.edge_attribut,
                                             font=self.regular_font,
                                             validate="key",
                                             validatecommand=self.validate)
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
                                      borderwidth=2, relief="groove", background="white")
        self.history_frame.grid_propagate(0)
        self.history_frame.bind("<Destroy>", self.re_init_history)
        self.dice_pool_spin = tk.Spinbox(master=self.app, from_=1, to=99, increment=1,
                                         width=2, textvariable=self.dice_pool,
                                         font=self.regular_font,
                                         validate="key",
                                         validatecommand=self.validate)
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
        
        if(self.edge_left.get() == 0):
            self.grey_out_button()
        
    def layout(self):
        self.your_throw.grid(column=0,row=0)
        self.dice_canvas.grid(column=0,row=1,rowspan=13,sticky="nsew")
        self.dice_canvas_scrollbar.grid(column=1,row=1,rowspan=13,sticky="ns")
        self.edge_attribut_spin.grid(column=2,row=1,sticky="e")
        self.edge_attribut_label.grid(column=3,row=1,sticky="w")
        self.edge_left_entry.grid(column=2,row=2,sticky="e")
        self.edge_left_label.grid(column=3,row=2,sticky="w")
        self.regain_edge_btn.grid(column=2,row=3,columnspan=2)
        self.history_frame.grid(column=2,row=4,columnspan=2,rowspan=4,sticky="nsew")
        self.dice_pool_spin.grid(column=2,row=8,sticky="e")
        self.throw_btn.grid(column=3,row=8,sticky="w")
        self.pre_edge_btn.grid(column=2,row=9,columnspan=2,sticky="we")
        self.post_edge_btn.grid(column=2,row=10,columnspan=2,sticky="we")
        self.edge_roll_btn.grid(column=2,row=11,columnspan=2,sticky="we")
        self.roll_for_edge_btn.grid(column=2,row=12,columnspan=2,sticky="we")
        self.reroll_misses_btn.grid(column=2,row=13,columnspan=2,sticky="we")
        
    def draw_result(self):
        """ Dynamically creates an images from png-files to visualize the result. """
        for widget in self.dice_canvas.winfo_children():
            widget.destroy()

        self.die_image = self.logic.merge_die(self.result, self.app_config)
        self.dice_canvas.create_image((0,0), image=self.die_image, anchor=tk.NW)

        self.write_to_history()
        
    def re_init_history(self, event):
        """ self.history_frame breaks after language change without this. """
        self.summary = []

    def grey_out_button(self):
        """ Grays out buttons if edge_left is at 0. """        
        if(self.edge_left.get() == 0):
            self.pre_edge_btn["state"] = "disabled"    
            self.post_edge_btn["state"] = "disabled"
            self.edge_roll_btn["state"] = "disabled"
            self.reroll_misses_btn["state"] = "disabled"
        else:
            self.pre_edge_btn["state"] = "normal"    
            self.post_edge_btn["state"] = "normal"
            self.edge_roll_btn["state"] = "normal"
            self.reroll_misses_btn["state"] = "normal"
        
    def write_to_history(self):
        """
        Chooses a fitting summary depending on the result and writes
        it to self.history_frame.
        Only the last 12 results are kept.
        """
        hits, misses, glitch, crit_glitch = self.logic.evaluate_roll(
                                                self.result, self.app_config.hits,
                                                self.app_config.misses)
        text = ""
        
        if(hits == 1 and glitch is False):
            text = self.trans.translate("one_Hit", hits=hits, n=len(self.result))
        elif(hits > 1 and glitch is False):
            text = self.trans.translate("n_Hits", hits=hits, n=len(self.result))
        elif(glitch):
            text = self.trans.translate("glitch", hits=hits, n=len(self.result))
        elif(crit_glitch):
            text = self.trans.translate("critical_glitch", n=len(self.result))
        else:
            text = self.trans.translate("no_Hits", n=len(self.result))

        self.summary.append(tk.Label(master=self.history_frame,
                                    text=text, font=self.regular_font,
                                    background="white"))

        if(len(self.summary) > self.HISTORY_SIZE):
            self.summary[0].destroy()
            self.summary.pop(0)
        
        for i in range(0, len(self.summary)):
            self.summary[i].grid(column=0, row=i, sticky="w")
            
    def start(self):
        self.init_widgets()
        self.layout()
        self.app.mainloop()
        
