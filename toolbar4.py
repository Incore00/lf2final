import tkinter as tk
import customtkinter as ctk
import pyglet
from tkfontawesome import icon_to_image
import os
import pygame
from PIL import ImageTk
from datetime import datetime
from threading import Thread
from LeatherWindow import LeatherWindow

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')
fontfile = "VeraMono.ttf"


class Toolbar(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.configure(height=int(parent.winfo_reqheight() * 0.1), width=parent.winfo_reqwidth(), bg='#303030')
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)
        self.rowconfigure(1, weight=1)

        logo = ImageTk.PhotoImage(file='images/logo.png')
        logo_label = tk.Label(self, image=logo, bg='#404040')
        logo_label.photo = logo
        logo_label.grid(column=1, row=1, sticky='nsew', ipadx=5)

        self.settings_icon = icon_to_image("cog", fill='#c7c6c5', scale_to_width=60)
        self.settings_btn = ctk.CTkButton(self, image=self.settings_icon, fg_color='#505050', hover_color='#404040',
                                          compound='top', corner_radius=10, text='Ustawienia',
                                          text_font=('OpenSans.ttf', 18))
        self.settings_btn.grid(column=2, row=1, sticky='nsew')

        self.change_colors_icon = icon_to_image("sync-alt", fill='#c7c6c5', scale_to_width=60)
        self.change_colors_btn = ctk.CTkButton(self, image=self.change_colors_icon,
                                               fg_color='#505050',
                                               hover_color='#404040', compound='top', corner_radius=10,
                                               text='Zmień kolory', text_font=('OpenSans.ttf', 18))
        self.change_colors_btn.grid(column=3, row=1, sticky='nsew')

        self.clock = tk.StringVar()
        tk.Label(self, textvariable=self.clock, bg='#404040', fg='#c7c6c5',
                 font=('OpenSans.ttf', 19)).grid(column=4, row=1, sticky='nsew', ipadx=5)
        Thread(target=self.clockLoop()).start()

        self.load_file_icon = icon_to_image("folder-open", fill='#c7c6c5', scale_to_width=65)
        self.load_file_btn = ctk.CTkButton(self, image=self.load_file_icon, fg_color='#505050',
                                           hover_color='#404040', compound='top', corner_radius=10, text='Wybierz plik',
                                           text_font=('OpenSans.ttf', 18))
        self.load_file_btn.grid(column=5, row=1, sticky='nsew')

        self.save_file_icon = icon_to_image("save", fill='#c7c6c5', scale_to_width=60)
        self.save_file_btn = ctk.CTkButton(self, image=self.save_file_icon, fg_color='#505050',
                                           hover_color='#404040', compound='top', corner_radius=10, text='Zapisz plik',
                                           text_font=('OpenSans.ttf', 18))
        self.save_file_btn.grid(column=6, row=1, sticky='nsew')

        self.exit_icon = icon_to_image("times", fill='#c7c6c5', scale_to_width=50)
        self.exit_btn = ctk.CTkButton(self, image=self.exit_icon, fg_color='#505050',
                                           hover_color='#404040', compound='top', corner_radius=10, text='Zamknij program',
                                           text_font=('OpenSans.ttf', 18))
        self.exit_btn.grid(column=7, row=1, sticky='nsew')

        for widget in self.winfo_children():
            widget.grid(padx=2, pady=2)


    def clockLoop (self):
        clock = datetime.now().strftime('%Y-%m-%d\n%H:%M:%S') + '\nTydzień ' + str(
            datetime.isocalendar(datetime.now())[1])
        self.clock.set(clock)
        self.after(1000, self.clockLoop)






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
        self.leather_info.insert(tk.END, text)

class Leatherpreview(tk.Frame):
    def __init__ (self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack_propagate(0)
        self.grid_propagate(0)
        sw, sh = int(parent.winfo_reqwidth()/1.6) , int(parent.winfo_reqheight()/1.6)
        print(sw, sh)
        self.configure(height=sh, width=sw)

        Thread(target=LeatherWindow(self, self, height=sh, width=sw).pack(side="top", fill="both", expand=True)).start()


class Layerinfo(tk.Frame):
    def __init__ (self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.configure(background='green', width=int(parent.winfo_reqwidth()-(parent.winfo_reqwidth()/1.618)), height=int(parent.winfo_reqheight()*0.865))