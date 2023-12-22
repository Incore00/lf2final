import os
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import pyglet
from tkfontawesome import icon_to_image
from PIL import ImageTk
from datetime import datetime
from threading import Thread
import ezdxf

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')


class Toolbar(tk.Frame):
    def __init__(self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue

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
                                           command=lambda: self.load_leather_data(),
                                           hover_color='#404040', compound='top', corner_radius=10, text='Wybierz plik',
                                           text_font=('OpenSans.ttf', 18))
        self.load_file_btn.grid(column=5, row=1, sticky='nsew')

        self.save_file_icon = icon_to_image("save", fill='#c7c6c5', scale_to_width=60)
        self.save_file_btn = ctk.CTkButton(self, image=self.save_file_icon, fg_color='#505050',
                                           hover_color='#404040', compound='top', corner_radius=10, text='Zapisz plik',
                                           text_font=('OpenSans.ttf', 18))
        self.save_file_btn.grid(column=6, row=1, sticky='nsew')

        self.exit_icon = icon_to_image("times", fill='#c7c6c5', scale_to_width=50)
        self.exit_btn = ctk.CTkButton(self, image=self.exit_icon, fg_color='#505050', command=self.parent.parent.destroy,
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

    def load_leather_data (self, file=None):
        if file == None:
            file = filedialog.askopenfile()
            print(file)

        c_layer = []
        c_layer_points = []
        b_layer = []
        b_layer_items = []
        g_layer = []
        g_layer_items = []
        y_layer = []
        y_layer_items = []
        r_layer = []
        r_layer_items = []
        h_layer = []
        h_layer_items = []
        text_layer_items = []

        if file != 'NotNone':
            try:
                leather = ezdxf.readfile(file.name)
                self.active_file = file.name
            except:
                leather = ezdxf.readfile(file)
                self.active_file = file
            msp = leather.modelspace()
            for item in msp:
                #print(item)
                if 'TEXT' in str(item):
                    # text -> layer 72
                    #print(item)
                    #print(item.dxf.get('layer'))
                    #print(item.get_placement())
                    #print(item.plain_text())
                    text_layer_items.append([item.get_placement()[1][0],item.get_placement()[1][1]])
                    #print(text_layer_items)
                if 'POLYLINE' in str(item):
                    if str(item.dxf.get('layer')) == '51':
                        b_layer.append(item)
                    elif str(item.dxf.get('layer')) == '52':
                        g_layer.append(item)
                    elif str(item.dxf.get('layer')) == '53':
                        y_layer.append(item)
                    elif str(item.dxf.get('layer')) == '54':
                        r_layer.append(item)
                    elif str(item.dxf.get('layer')) == '11':
                        h_layer.append(item)
                    elif str(item.dxf.get('layer')) == '1':
                        c_layer.append(item)

        try:
            for item in c_layer:
                for point in item.points():
                    c_layer_points.append((point[0], point[1]))
        except:
            raise Exception("Błąd podczas odczytu punktów warstwy konturu")

        try:
            for item in b_layer:
                item_list = []
                for point in item.points():
                    item_list.append((point[0], point[1]))
                b_layer_items.append(item_list)
        except:
            raise Exception("Błąd podczas odczytu punktów warstwy niebieskiej")
        try:
            for item in g_layer:
                item_list = []
                for point in item.points():
                    item_list.append((point[0], point[1]))
                g_layer_items.append(item_list)
        except:
            raise Exception("Błąd podczas odczytu punktów warstwy zielonej")
        try:
            for item in y_layer:
                item_list = []
                for point in item.points():
                    item_list.append((point[0], point[1]))
                y_layer_items.append(item_list)
        except:
            raise Exception("Błąd podczas odczytu punktów warstwy żółtej")
        try:
            for item in r_layer:
                item_list = []
                for point in item.points():
                    item_list.append((point[0], point[1]))
                r_layer_items.append(item_list)
        except:
            raise Exception("Błąd podczas odczytu punktów warstwy czerwonej")
        try:
            for item in h_layer:
                item_list = []
                for point in item.points():
                    item_list.append((point[0], point[1]))
                h_layer_items.append(item_list)
        except:
            raise Exception("Błąd podczas odczytu punktów warstwy dziur")

        leather_data = c_layer_points, h_layer_items, b_layer_items, g_layer_items, y_layer_items, r_layer_items, text_layer_items

        self.queue.put(['preview_load_data', leather_data])
        self.queue.put(['main_load_data', leather_data])
        self.parent.infobar.update_info(file.name)

        self.parent.layer_info.load_data(len(h_layer_items),len(b_layer_items),len(g_layer_items),len(y_layer_items),len(r_layer_items))





