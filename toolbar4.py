import tkinter as tk
import customtkinter as ctk
import pyglet
from tkfontawesome import icon_to_image

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')
fontfile = "VeraMono.ttf"


class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(height=int(parent.winfo_reqheight() * 0.1), width=parent.winfo_reqwidth(), bg='#303030')
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure((1), weight=1)
        self.rowconfigure(1, weight=1)

        toolbar_container = tk.Frame(self, height=int(parent.winfo_reqheight() * 0.1), width=parent.winfo_reqwidth(),
                                     bg='#303030')
        toolbar_container.pack_propagate(0)
        toolbar_container.grid_propagate(0)
        toolbar_container.columnconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)
        toolbar_container.rowconfigure(1, weight=1)
        toolbar_container.grid(column=1, row=1, sticky='nsew')


class Infobar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg='#303030')
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.leather_info = tk.Text(self, bg='#505050', fg='#c7c6c5', font=("VeraMono.ttf", 20))
        self.leather_info.insert(tk.END, "LEATHER123123")
        self.leather_info.grid(column=1, row=1, sticky='nsew')

        self.load_file_icon = icon_to_image("folder-open", fill='#c7c6c5', scale_to_width=60)
        self.load_btn = ctk.CTkButton(self, image=self.load_file_icon, fg_color='#505050',
                                      hover_color='#404040', command=lambda: self.load_leather()
                                      , compound='top', corner_radius=10, text='Załaduj plik',
                                      text_font=('OpenSans.ttf', 18))
