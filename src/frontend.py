#================================================
# Imports
#================================================
import customtkinter
from SixSidedDie import SixSidedDie
from translate import Translator

#================================================
# Setup
#================================================
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("450x600")

translator = Translator("../lang")
translator.set_locale("en")
#================================================
# Buttonfunctions
#================================================
def button_function():
    print("button pressed")

throw_btn_text = translator.translate("throw")
throw_btn= customtkinter.CTkButton(master=app, text=throw_btn_text, command=button_function)

#================================================
# Layout
#================================================
button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

#================================================
# mainloop
#================================================
app.mainloop()
