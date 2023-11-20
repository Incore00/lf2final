import tkinter as tk
import pyglet

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')

class Infobar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.configure(bg='#303030', width=int(parent.winfo_reqwidth()), height=int(parent.winfo_reqheight() * 0.035))
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self.leather_info = tk.Text(self, bg='#505050', fg='#c7c6c5', font=("VeraMono.ttf", 20))
        self.leather_info.grid(column=1, row=1, sticky='nsew')

    def update_info(self, text:str):
        self.leather_info.delete('1.0', 'end')
        self.leather_info.insert(tk.END, text)