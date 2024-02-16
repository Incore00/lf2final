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
from ezdxf.enums import TextEntityAlignment
from bin import configFile

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')


class Toolbar(tk.Frame):
    def __init__(self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue
        self.filename = None

        self.configure(height=int(parent.winfo_reqheight() * 0.1), width=parent.winfo_reqwidth(), bg='#303030')
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure((1, 2, 3, 4, 5, 6, 7), weight=1)
        self.rowconfigure(1, weight=1)

        self.change_colors_flag = False

        logo = ImageTk.PhotoImage(file='images/logo.png')
        logo_label = tk.Label(self, image=logo, bg='#404040')
        logo_label.photo = logo
        logo_label.grid(column=1, row=1, sticky='nsew', ipadx=5)

        self.settings_icon = icon_to_image("cog", fill='#c7c6c5', scale_to_width=60)
        self.settings_btn = ctk.CTkButton(self, image=self.settings_icon, fg_color='#505050', hover_color='#404040',
                                          compound='top', corner_radius=10, text='Ustawienia',
                                          text_font=('OpenSans.ttf', 18))
        self.settings_btn.grid(column=2, row=1, sticky='nsew')

        self.change_colors_icon_inactive = icon_to_image("sync-alt", fill='#c7c6c5', scale_to_width=60)
        self.change_colors_icon_active = icon_to_image("sync-alt", fill='#000000', scale_to_width=60)
        self.change_colors_btn = ctk.CTkButton(self, image=self.change_colors_icon_inactive,
                                               fg_color='#505050', command=lambda: self.change_colors_func(),
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
                                           command=lambda: self.save_leather_data(),
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

    def change_colors_func(self):
        if self.change_colors_flag == False:
            #configFile.c_layer_color = (0, 0, 0)
            #configFile.bg_layer_color = (255, 255, 255)
            configFile.b_layer_linetype = "lines"
            configFile.g_layer_linetype = "lines"
            configFile.y_layer_linetype = "lines"
            configFile.r_layer_linetype = "lines"
            self.change_colors_flag = True
            self.change_colors_btn.configure(image=self.change_colors_icon_active)
        elif self.change_colors_flag == True:
            #configFile.c_layer_color = (255, 255, 255)
            #configFile.bg_layer_color = (0, 0, 0)
            configFile.b_layer_linetype = "polygon"
            configFile.g_layer_linetype = "polygon"
            configFile.y_layer_linetype = "polygon"
            configFile.r_layer_linetype = "polygon"
            self.change_colors_flag = False
            self.change_colors_btn.configure(image=self.change_colors_icon_inactive)
        linetypes = [configFile.b_layer_linetype, configFile.g_layer_linetype, configFile.y_layer_linetype, configFile.r_layer_linetype]
        self.queue.put(['main_change_colors', linetypes])
        self.queue.put(['preview_reload'])
        self.queue.put(['main_reload'])

    def save_leather_data (self):
        leather_data = self.parent.leather_preview.lw_prev.save_leather_data()
        c_layer_points = leather_data[0]
        h_layer_items = leather_data[1]
        b_layer_items = leather_data[2]
        g_layer_items = leather_data[3]
        y_layer_items = leather_data[4]
        r_layer_items = leather_data[5]
        text_layer_items = leather_data[6]

        print('get red', r_layer_items)

        new_doc = ezdxf.new()
        msp = new_doc.modelspace()

        new_doc.layers.add(name="72", color=7)

        msp.add_text("MARK_1", dxfattribs={"layer": "72", }).set_placement((text_layer_items[0]), align=TextEntityAlignment.BOTTOM_LEFT)
        msp.add_text("MARK_2", dxfattribs={"layer": "72"}).set_placement((text_layer_items[1]), align=TextEntityAlignment.BOTTOM_LEFT)

        msp.add_polyline2d(c_layer_points, close=True, dxfattribs={"layer": "1"})
        for item in h_layer_items:
            msp.add_polyline2d(item, close=True, dxfattribs={"layer": "11"})
        for item in b_layer_items:
            msp.add_polyline2d(item, close=True, dxfattribs={"layer": "51"})
        for item in g_layer_items:
            msp.add_polyline2d(item, close=True, dxfattribs={"layer": "52"})
        for item in y_layer_items:
            msp.add_polyline2d(item, close=True, dxfattribs={"layer": "53"})
        for item in r_layer_items:
            msp.add_polyline2d(item, close=True, dxfattribs={"layer": "54"})

        #new_doc.saveas(self.filename)
        new_doc.saveas("testowy_pliczek.dxf")

    def load_leather_data (self, file=None):
        if file == None:
            file = filedialog.askopenfile()
            if file != None:
                print(file)
                self.filename = file.name
            else:
                pass


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

        if file != None:
            try:
                leather = ezdxf.readfile(file.name)
                self.active_file = file.name
            except:
                leather = ezdxf.readfile(file)
                self.active_file = file
            msp = leather.modelspace()
            for layer in leather.layers:
                print('layer color:', layer.color)
            for item in msp:
                print('msp - item', item, 'item - type', item.dxf.get('layer'))
                if 'TEXT' in str(item):
                    # text -> layer 72
                    #print(item)
                    #print(item.dxf.get('layer'))
                    print(item.get_placement())
                    print(item.plain_text())
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
        else:
            pass
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

        if str(c_layer_points) != '[]':
            leather_data = c_layer_points, h_layer_items, b_layer_items, g_layer_items, y_layer_items, r_layer_items, text_layer_items

            self.queue.put(['preview_load_data', leather_data])
            self.queue.put(['main_load_data', leather_data])
            self.parent.infobar.update_info(file.name)

            self.parent.layer_info.load_data(len(h_layer_items),len(b_layer_items),len(g_layer_items),len(y_layer_items),len(r_layer_items))





