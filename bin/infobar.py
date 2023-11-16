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
        self.leather_info.insert(tk.END, "LEATHER123123")
        self.leather_info.grid(column=1, row=1, sticky='nsew')

        print("id2", self.winfo_id())

        #self.load_file_icon = icon_to_image("folder-open", fill='#c7c6c5', scale_to_width=60)
        #self.load_btn = ctk.CTkButton(self, image=self.load_file_icon, fg_color='#505050',
        #                              hover_color='#404040', command=lambda: self.load_leather()
        #                              , compound='top', corner_radius=10, text='Załaduj plik',
        #                              text_font=('OpenSans.ttf', 18))

    def update_info(self, text:str):
        self.leather_info.delete('1.0', 'end')
        self.leather_info.insert(tk.END, text)