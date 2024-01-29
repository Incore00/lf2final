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

        self.back_icon = icon_to_image("undo", fill='#c7c6c5', scale_to_width=40)
        self.back_btn = ctk.CTkButton(self, image=self.back_icon, fg_color='#505050', hover_color='#404040',
                                          compound='left', corner_radius=10, text='Cofnij', text_font=('OpenSans.ttf', 18))
        self.back_btn.grid(column=1, row=1, padx=2, pady=2, sticky='nsew')

        self.add_flaw_icon = icon_to_image("draw-polygon", fill='#c7c6c5', scale_to_width=40)
        self.add_flaw_btn = ctk.CTkButton(self, image=self.add_flaw_icon, fg_color='#505050', hover_color='#404040',
                                          compound='left', corner_radius=10, text='Rysuj skaze', text_font=('OpenSans.ttf', 18))
        self.add_flaw_btn.grid(column=2, row=1, padx=2, pady=2, sticky='nsew')

        self.layer_icon = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=40)
        self.layer_btn = ctk.CTkButton(self, image=self.layer_icon, fg_color='#505050', hover_color='#404040',
                                      compound='left', corner_radius=10, text='Warstwa', text_font=('OpenSans.ttf', 18))
        self.layer_btn.grid(column=3, row=1, padx=2, pady=2, sticky='nsew')

        self.move_flaw_icon = icon_to_image("arrows-alt", fill='#c7c6c5', scale_to_width=40)
        self.move_flaw_btn = ctk.CTkButton(self, image=self.move_flaw_icon, fg_color='#505050', hover_color='#404040',
                                        compound='left', corner_radius=10, text='Przesuń skazę',
                                        text_font=('OpenSans.ttf', 18))
        self.move_flaw_btn.grid(column=4, row=1, padx=2, pady=2, sticky='nsew')

        self.delete_icon = icon_to_image("eraser", fill='#c7c6c5', scale_to_width=40)
        self.delete_btn = ctk.CTkButton(self, image=self.delete_icon, fg_color='#505050', hover_color='#404040',
                                       compound='left', corner_radius=10, text='Usuń skazę',
                                       text_font=('OpenSans.ttf', 18))
        self.delete_btn.grid(column=5, row=1, padx=2, pady=2, sticky='nsew')





        #for widget in self.winfo_children():
        #    widget.grid(padx=10, pady=10)