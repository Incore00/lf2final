import tkinter as tk
import pyglet
import customtkinter as ctk
from tkfontawesome import icon_to_image


pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')

class leather_tools(tk.Frame):
    def __init__(self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure((1, 2, 3, 4, 5), weight=1)
        #self.rowconfigure(1, weight=1)

        self.configure(height=int(parent.winfo_reqheight() * 0.1), width=int(parent.winfo_reqwidth() * 0.767), bg='#303030')

        self.to_do_bar = ctk.CTkLabel(self, text='Załaduj plik', height=int(parent.winfo_reqheight() * 0.),
                                      width=int(parent.winfo_reqwidth() * 0.767), text_font=('OpenSans.ttf', 30))
        self.to_do_bar.grid(column=1, row=1, sticky='nsew')