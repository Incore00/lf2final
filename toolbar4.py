import tkinter as tk
import customtkinter as ctk
import pyglet
from tkfontawesome import icon_to_image
import os
import pygame
from PIL import ImageTk
from datetime import datetime
from threading import Thread

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

        self.load_file_icon = icon_to_image("folder-open", fill='#c7c6c5', scale_to_width=60)
        self.load_file_btn = ctk.CTkButton(self, image=self.load_file_icon, fg_color='#505050',
                                           hover_color='#404040', compound='top', corner_radius=10, text='Załaduj plik',
                                           text_font=('OpenSans.ttf', 18))
        self.load_file_btn.grid(column=5, row=1, sticky='nsew')

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
        self.screen_width, self.screen_height = int(parent.winfo_reqwidth()/1.6) , int(parent.winfo_reqheight()/1.6)
        print(self.screen_width, self.screen_height)

        self.configure(background='brown', width=self.screen_width, height=self.screen_height)

        os.environ['SDL_WINDOWID'] = str(self.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        window_size = (int(parent.winfo_reqwidth()/1.618), int(parent.winfo_reqheight()/1.618))
        self.screen = pygame.display.set_mode(window_size)
        self.main_surface = pygame.Surface(window_size)



        self.pygame_loop()

    def pygame_loop (self):
        pygame.display.flip()

        self.update()
        self.after(1, self.pygame_loop)

class Layerinfo(tk.Frame):
    def __init__ (self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.configure(background='green', width=int(parent.winfo_reqwidth()-(parent.winfo_reqwidth()/1.618)), height=int(parent.winfo_reqheight()*0.865))