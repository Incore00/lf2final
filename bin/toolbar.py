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
from tkinter import ttk
from tkinter.colorchooser import askcolor

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
                                          text_font=('OpenSans.ttf', 18), command =lambda: self.show_settings())
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

        self.current_topwindow = tk.Label(self)

        self.code = ''
        self.leather_name = ''
        self.code_flag = False

        self.parent.parent.bind('<Key>', self.get_key)

    def get_key (self, event):
        if self.code_flag == False:
            self.code += str(event.char)
        else:
            self.code_flag = False
            self.code = ''
        if len(self.code) >= 24 and event.keysym == 'Return':
            self.leather_name = self.code[-25:]
            self.load_scanned_leather(self.leather_name)
            self.code = ''
            self.code_flag = True

    def load_scanned_leather (self, leather_name):
        data = leather_name[:-1]
        path_list = configFile.leather_path_list
        for path in path_list:
            path = path + "\\" + data + ".DXF"
            try:
                self.load_leather_data(path)
                print('Load file success', path)
            except:
                print("Cant load file in: " + path)
                pass

    def clockLoop (self):
        clock = datetime.now().strftime('%Y-%m-%d\n%H:%M:%S') + '\nTydzień ' + str(
            datetime.isocalendar(datetime.now())[1])
        self.clock.set(clock)
        self.after(1000, self.clockLoop)

    def show_settings(self):
        self.current_topwindow.destroy()
        self.current_topwindow = Settings(self.parent, self.queue)

    def change_colors_func(self):
        if self.change_colors_flag == False:
            configFile.bg_layer_color = configFile.second_bg_layer_color
            configFile.c_layer_color = configFile.second_c_layer_color
            configFile.h_layer_color = configFile.second_h_layer_color
            configFile.b_layer_color = configFile.second_b_layer_color
            configFile.b_layer_linetype = configFile.second_b_layer_linetype
            configFile.g_layer_color = configFile.second_g_layer_color
            configFile.g_layer_linetype = configFile.second_g_layer_linetype
            configFile.y_layer_color = configFile.second_y_layer_color
            configFile.y_layer_linetype = configFile.second_y_layer_linetype
            configFile.r_layer_color = configFile.second_r_layer_color
            configFile.r_layer_linetype = configFile.second_r_layer_linetype
            self.change_colors_flag = True
            self.change_colors_btn.configure(image=self.change_colors_icon_active)
        elif self.change_colors_flag == True:
            configFile.bg_layer_color = configFile.first_bg_layer_color
            configFile.c_layer_color = configFile.first_c_layer_color
            configFile.h_layer_color = configFile.first_h_layer_color
            configFile.b_layer_color = configFile.first_b_layer_color
            configFile.b_layer_linetype = configFile.first_b_layer_linetype
            configFile.g_layer_color = configFile.first_g_layer_color
            configFile.g_layer_linetype = configFile.first_g_layer_linetype
            configFile.y_layer_color = configFile.first_y_layer_color
            configFile.y_layer_linetype = configFile.first_y_layer_linetype
            configFile.r_layer_color = configFile.first_r_layer_color
            configFile.r_layer_linetype = configFile.first_r_layer_linetype
            self.change_colors_flag = False
            self.change_colors_btn.configure(image=self.change_colors_icon_inactive)
        linetypes = [configFile.b_layer_linetype,
                     configFile.g_layer_linetype,
                     configFile.y_layer_linetype,
                     configFile.r_layer_linetype]
        colors = [configFile.bg_layer_color,
                  configFile.h_layer_color,
                  configFile.c_layer_color,
                  configFile.b_layer_color,
                  configFile.g_layer_color,
                  configFile.y_layer_color,
                  configFile.r_layer_color]
        self.queue.put(['main_change_colors', linetypes, colors])
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
        file_types = [("Pliki DXF", "*.DXF"),
                      ("Wszystkie pliki", "*.*")]
        if file == None:
            file = filedialog.askopenfile(filetypes=file_types, multiple=False)
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
                self.filename = file.name
            except:
                leather = ezdxf.readfile(file)
                self.active_file = file
                self.filename = file
            msp = leather.modelspace()
            for item in msp:
                #print('msp - item', item, 'item - type', item.dxf.get('layer'))
                if 'TEXT' in str(item):
                    # text -> layer 72
                    #print(item)
                    #print(item.dxf.get('layer'))
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
            try:
                self.parent.infobar.update_info(file.name)
            except:
                self.parent.infobar.update_info(file)
            self.parent.layer_info.load_data(len(h_layer_items),len(b_layer_items),len(g_layer_items),len(y_layer_items),len(r_layer_items))


class Settings(tk.Toplevel):
    def __init__(self, parent, queue, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue

        self.colorpicker = tk.Label(self)

        self.geometry('%dx%d%+d+%d' % (1600, 900, 160, 90))
        self.attributes('-topmost', 'true')
        self.resizable(False, False)
        self.overrideredirect(True)
        self.configure(bg='#303030')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(1, weight=1)
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.settings_notebook = ttk.Notebook(self)
        self.ogolne_tab = ctk.CTkFrame(self.settings_notebook, bg_color='#303030')
        self.display_tab = ctk.CTkFrame(self.settings_notebook)
        self.calibration_tab = ctk.CTkFrame(self.settings_notebook)

        self.display_tab.columnconfigure((1,2,3), weight =1)
        self.display_tab.rowconfigure((1, 2, 3), weight=1)

        self.settings_notebook.add(self.ogolne_tab, text='       Ogólne       ')
        self.settings_notebook.add(self.display_tab, text='      Wyświetlanie      ')
        self.settings_notebook.add(self.calibration_tab, text='      Kalibracja      ')
        self.settings_notebook.grid(row=1, column=1, columnspan=3, sticky='nsew')

        self.save_btn = ctk.CTkButton(self, text = 'Zapisz', fg_color='#505050', hover_color='#606060', text_font=('OpenSans.ttf', 20))
        self.save_btn.grid(row=2, column=1, sticky='e', padx=10, pady=10)
        self.ok_btn = ctk.CTkButton(self, text='   OK   ', fg_color='#505050', hover_color='#606060',
                                      text_font=('OpenSans.ttf', 20))
        self.ok_btn.grid(row=2, column=2, sticky='e', padx=10, pady=10)
        self.anuluj_btn = ctk.CTkButton(self, text='Anuluj', fg_color='#505050', hover_color='#606060',
                                    text_font=('OpenSans.ttf', 20), command = lambda:self.anuluj_btn_func())
        self.anuluj_btn.grid(row=2, column=3, sticky='e', padx=10, pady=10)
        ######## OGOLNE TAB
        ##### SCIEZKI
        self.ramka_sciezki = tk.LabelFrame(self.ogolne_tab, text='Lokalizacje plików skór', font=('OpenSans.ttf', 13), bg='#303030', fg='#c7c6c5')
        self.sciezki_entry_list = []
        self.sciezki_button_list = []
        self.sciezki_checkbox_list = []

        tk.Label(self.ramka_sciezki, text='Ścieżki do folderów zawierających skany skór:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=1, columnspan=3, sticky='nsew', padx=10, pady=10)
        tk.Label(self.ramka_sciezki, text='Domyślne dla opcji\n"wybierz plik', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=4, sticky='nsew', padx=10, pady=10)
        self.check_var = tk.IntVar(self)
        for index, path in enumerate(configFile.leather_path_list):
            row_index = index + 2
            tk.Label(self.ramka_sciezki, text='Ścieżka %s:' %str(index+1), bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=index+1, column=1, sticky='nsew', padx=10, pady=10)
            self.sciezki_entry_list.append(ctk.CTkEntry(self.ramka_sciezki, width=400, justify=tk.LEFT, text_font=('OpenSans.ttf', 13)))
            self.sciezki_entry_list[index].grid(row=row_index, column=2, sticky='nsew', padx=10, pady=10)
            self.sciezki_entry_list[index].insert(0, path)
            self.sciezki_button_list.append(ctk.CTkButton(self.ramka_sciezki, text='Zmień ścieżkę', text_font=('OpenSans.ttf', 14),
                                              fg_color='#505050', hover_color='#404040', command=lambda x = self.sciezki_entry_list[index]: self.change_path(x)))
            self.sciezki_button_list[index].grid(row=row_index, column=3, sticky='nsew', padx=10, pady=10)
            self.sciezki_checkbox_list.append(ctk.CTkCheckBox(self.ramka_sciezki, onvalue=0,variable=self.check_var))
            self.sciezki_checkbox_list[index].grid(row=row_index, column=4, sticky='nsew', padx=10, pady=10)


        self.ramka_sciezki.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        ######## DISPLAY TAB
        self.ramka_cursor = tk.LabelFrame(self.display_tab, text='Opcje kursora', font=('OpenSans.ttf', 13), bg='#303030', fg='#c7c6c5')
        self.ramka_cursor.columnconfigure((1,2,3), weight=1)
        self.ramka_cursor.rowconfigure((1,2), weight=1)
        tk.Label(self.ramka_cursor, text='Średnica kursora:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.cursor_radius_entry = ctk.CTkEntry(self.ramka_cursor, width=50, justify=tk.CENTER, text_font=('OpenSans.ttf', 14))
        self.cursor_radius_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.cursor_radius_entry.insert(0, configFile.cursor_radius)
        tk.Label(self.ramka_cursor, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1, column=3, sticky='w', padx=3, pady=10)

        tk.Label(self.ramka_cursor, text='Kolor kursora:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew', padx=10, pady=10)
        self.probka_koloru_cursora = tk.Label(self.ramka_cursor, text=' ', bg=self.rgb_to_hex(*configFile.cursor_color),
                                      fg=self.rgb_to_hex(*configFile.cursor_color), font=('OpenSans.ttf', 14))
        self.probka_koloru_cursora.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_cursor_btn = ctk.CTkButton(self.ramka_cursor, text='Zmień kolor', text_font=('OpenSans.ttf', 14),
                                              fg_color='#505050', hover_color='#404040', command=lambda x = self.probka_koloru_cursora: self.change_obj_color(x))
        self.change_color_cursor_btn.grid(row=2, column=3, sticky='nsew', padx=10, pady=10)
        self.ramka_cursor.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)


        self.ramka_flaw_menu = tk.LabelFrame(self.display_tab, text='Opcje menu na skazie', font=('OpenSans.ttf', 13), bg='#303030', fg='#c7c6c5')
        self.ramka_flaw_menu.columnconfigure((1, 2, 3), weight=1)
        self.ramka_flaw_menu.rowconfigure((1, 2, 3, 4, 5), weight=1)

        tk.Label(self.ramka_flaw_menu, text='Szerokość menu:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.szerokosc_menu_skazy_entry = ctk.CTkEntry(self.ramka_flaw_menu, width=70, justify=tk.CENTER, text_font=('OpenSans.ttf', 14))
        self.szerokosc_menu_skazy_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.szerokosc_menu_skazy_entry.insert(0, configFile.flaw_dropdown_menu_x_size)
        tk.Label(self.ramka_flaw_menu, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                           column=3,
                                                                                                           sticky='w',
                                                                                                           padx=3,
                                                                                                           pady=10)

        tk.Label(self.ramka_flaw_menu, text='Wysokość menu:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew')
        self.wysokosc_menu_skazy_entry = ctk.CTkEntry(self.ramka_flaw_menu, width=70, justify=tk.CENTER,
                                                       text_font=('OpenSans.ttf', 14))
        self.wysokosc_menu_skazy_entry.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.wysokosc_menu_skazy_entry.insert(0, configFile.flaw_dropdown_menu_y_size)
        tk.Label(self.ramka_flaw_menu, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=2,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)

        tk.Label(self.ramka_flaw_menu, text='Kolor tła menu:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=3, column=1, sticky='nsew')
        self.probka_koloru_tla_menu_skazy = tk.Label(self.ramka_flaw_menu, text=' ', bg=self.rgb_to_hex(*configFile.flaw_dropdown_menu_color),
                                              fg=self.rgb_to_hex(*configFile.flaw_dropdown_menu_color), font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_menu_skazy.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_flaw_tlo_btn = ctk.CTkButton(self.ramka_flaw_menu, text='Zmień kolor', text_font=('OpenSans.ttf', 14),
                                              fg_color='#505050', hover_color='#404040',
                                              command=lambda x = self.probka_koloru_tla_menu_skazy: self.change_obj_color(x))
        self.change_color_flaw_tlo_btn.grid(row=3, column=3, sticky='nsew', padx=10, pady=10)

        tk.Label(self.ramka_flaw_menu, text='Kolor tła\nopcji menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=4, column=1, sticky='nsew')
        self.probka_koloru_tla_opcji_menu_skazy = tk.Label(self.ramka_flaw_menu, text=' ',
                                                     bg=self.rgb_to_hex(*configFile.flaw_dropdown_menu_option_color),
                                                     fg=self.rgb_to_hex(*configFile.flaw_dropdown_menu_option_color),
                                                     font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_opcji_menu_skazy.grid(row=4, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_flaw_tlo_opcji_btn = ctk.CTkButton(self.ramka_flaw_menu, text='Zmień kolor',
                                                       text_font=('OpenSans.ttf', 14),
                                                       fg_color='#505050', hover_color='#404040',
                                                       command=lambda x = self.probka_koloru_tla_opcji_menu_skazy: self.change_obj_color(x))
        self.change_color_flaw_tlo_opcji_btn.grid(row=4, column=3, sticky='nsew', padx=10, pady=10)

        tk.Label(self.ramka_flaw_menu, text='Kolor czcionki\nopcji menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=5, column=1, sticky='nsew')
        self.probka_koloru_czcionki_menu_skazy = tk.Label(self.ramka_flaw_menu, text=' ',
                                                           bg=self.rgb_to_hex(
                                                               *configFile.flaw_dropdown_menu_font_color),
                                                           fg=self.rgb_to_hex(
                                                               *configFile.flaw_dropdown_menu_font_color),
                                                           font=('OpenSans.ttf', 14))
        self.probka_koloru_czcionki_menu_skazy.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_flaw_font_btn = ctk.CTkButton(self.ramka_flaw_menu, text='Zmień kolor',
                                                             text_font=('OpenSans.ttf', 14),
                                                             fg_color='#505050', hover_color='#404040',
                                                             command=lambda x = self.probka_koloru_czcionki_menu_skazy: self.change_obj_color(x))
        self.change_color_flaw_font_btn.grid(row=5, column=3, sticky='nsew', padx=10, pady=10)

        self.ramka_flaw_menu.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)


        self.ramka_menu = tk.LabelFrame(self.display_tab, text='Opcje menu bez skazy', font=('OpenSans.ttf', 13),
                                             bg='#303030', fg='#c7c6c5')
        self.ramka_menu.columnconfigure((1, 2, 3), weight=1)
        self.ramka_menu.rowconfigure((1, 2, 3, 4, 5), weight=1)
        tk.Label(self.ramka_menu, text='Szerokość menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.szerokosc_menu_entry = ctk.CTkEntry(self.ramka_menu, width=70, justify=tk.CENTER,
                                                       text_font=('OpenSans.ttf', 14))
        self.szerokosc_menu_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.szerokosc_menu_entry.insert(0, configFile.dropdown_menu_x_size)
        tk.Label(self.ramka_menu, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)

        tk.Label(self.ramka_menu, text='Wysokość menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew')
        self.wysokosc_menu_entry = ctk.CTkEntry(self.ramka_menu, width=70, justify=tk.CENTER,
                                                      text_font=('OpenSans.ttf', 14))
        self.wysokosc_menu_entry.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.wysokosc_menu_entry.insert(0, configFile.dropdown_menu_y_size)
        tk.Label(self.ramka_menu, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=2,
                                                                                                         column=3,
                                                                                                         sticky='w',
                                                                                                         padx=3,
                                                                                                         pady=10)

        tk.Label(self.ramka_menu, text='Kolor tła menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=3, column=1, sticky='nsew')
        self.probka_koloru_tla_menu = tk.Label(self.ramka_menu, text=' ',
                                                     bg=self.rgb_to_hex(*configFile.dropdown_menu_color),
                                                     fg=self.rgb_to_hex(*configFile.dropdown_menu_color),
                                                     font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_menu.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_tlo_btn = ctk.CTkButton(self.ramka_menu, text='Zmień kolor',
                                                       text_font=('OpenSans.ttf', 14),
                                                       fg_color='#505050', hover_color='#404040',
                                                       command=lambda x = self.probka_koloru_tla_menu: self.change_obj_color(x))
        self.change_color_tlo_btn.grid(row=3, column=3, sticky='nsew', padx=10, pady=10)

        tk.Label(self.ramka_menu, text='Kolor tła\nopcji menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=4, column=1, sticky='nsew')
        self.probka_koloru_tla_opcji_menu = tk.Label(self.ramka_menu, text=' ',
                                                           bg=self.rgb_to_hex(
                                                               *configFile.dropdown_menu_option_color),
                                                           fg=self.rgb_to_hex(
                                                               *configFile.dropdown_menu_option_color),
                                                           font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_opcji_menu.grid(row=4, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_tlo_opcji_btn = ctk.CTkButton(self.ramka_menu, text='Zmień kolor',
                                                             text_font=('OpenSans.ttf', 14),
                                                             fg_color='#505050', hover_color='#404040',
                                                             command=lambda x = self.probka_koloru_tla_opcji_menu: self.change_obj_color(x))
        self.change_color_tlo_opcji_btn.grid(row=4, column=3, sticky='nsew', padx=10, pady=10)

        tk.Label(self.ramka_menu, text='Kolor czcionki\nopcji menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=5, column=1, sticky='nsew')
        self.probka_koloru_czcionki_menu = tk.Label(self.ramka_menu, text=' ',
                                                          bg=self.rgb_to_hex(
                                                              *configFile.dropdown_menu_font_color),
                                                          fg=self.rgb_to_hex(
                                                              *configFile.dropdown_menu_font_color),
                                                          font=('OpenSans.ttf', 14))
        self.probka_koloru_czcionki_menu.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_font_btn = ctk.CTkButton(self.ramka_menu, text='Zmień kolor',
                                                        text_font=('OpenSans.ttf', 14),
                                                        fg_color='#505050', hover_color='#404040',
                                                        command=lambda x = self.probka_koloru_czcionki_menu: self.change_obj_color(x))
        self.change_color_font_btn.grid(row=5, column=3, sticky='nsew', padx=10, pady=10)
        self.ramka_menu.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        ######### ZMIEN KOLORY ###################

        self.ramka_zmien_kolory = tk.LabelFrame(self.display_tab, text='Opcje funkcji zmień kolory', font=('OpenSans.ttf', 13),
                                        bg='#303030', fg='#c7c6c5')
        self.ramka_zmien_kolory.columnconfigure((1,2), weight=1)
        self.ramka_zmien_kolory.rowconfigure((1), weight=1)


        self.ramka_zk_domyslne = tk.LabelFrame(self.ramka_zmien_kolory, text='Opcje domyślne',
                                                font=('OpenSans.ttf', 13),
                                                bg='#303030', fg='#c7c6c5')
        self.ramka_zk_poklik = tk.LabelFrame(self.ramka_zmien_kolory, text='Opcje po kliknięciu',
                                             font=('OpenSans.ttf', 13),
                                             bg='#303030', fg='#c7c6c5')

        self.ramka_zk_domyslne.columnconfigure((1,2,3), weight =1)
        self.ramka_zk_domyslne.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.ramka_zk_poklik.columnconfigure((1,2,3), weight =1)
        self.ramka_zk_poklik.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)

        ### 1 rzad
        tk.Label(self.ramka_zk_domyslne, text='Kolor tła:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew')
        self.probka_koloru_tla_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                               bg=self.rgb_to_hex(*configFile.first_bg_layer_color),
                                               fg=self.rgb_to_hex(*configFile.first_bg_layer_color),
                                               font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_domyslne.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_tlo_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                  text_font=('OpenSans.ttf', 14),
                                                  fg_color='#505050', hover_color='#404040',
                                                  command=lambda x = self.probka_koloru_tla_domyslne: self.change_obj_color(x))
        self.change_color_tlo_domyslne_btn.grid(row=1, column=3, sticky='nsew', padx=10, pady=10)

        ### 2 rzad
        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\nkonturu:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew')
        self.probka_koloru_konturu_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                   bg=self.rgb_to_hex(*configFile.first_c_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.first_c_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_konturu_domyslne.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_konturu_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda x = self.probka_koloru_konturu_domyslne: self.change_obj_color(x))
        self.change_color_konturu_domyslne_btn.grid(row=2, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 3

        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\ndziur:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=3, column=1, sticky='nsew')
        self.probka_koloru_dziur_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                   bg=self.rgb_to_hex(*configFile.first_h_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.first_h_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_dziur_domyslne.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_dziur_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda
                                                               x=self.probka_koloru_dziur_domyslne: self.change_obj_color(
                                                               x))
        self.change_color_dziur_domyslne_btn.grid(row=3, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 4

        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\nniebieskiej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=4, column=1, sticky='nsew')
        self.probka_koloru_blue_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                  bg=self.rgb_to_hex(*configFile.first_b_layer_color),
                                                  fg=self.rgb_to_hex(*configFile.first_b_layer_color),
                                                  font=('OpenSans.ttf', 14))
        self.probka_koloru_blue_domyslne.grid(row=4, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_blue_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                          text_font=('OpenSans.ttf', 14),
                                                          fg_color='#505050', hover_color='#404040',
                                                          command=lambda
                                                              x=self.probka_koloru_blue_domyslne: self.change_obj_color(
                                                              x))
        self.change_color_blue_domyslne_btn.grid(row=4, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 5

        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\nzielonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=5, column=1, sticky='nsew')
        self.probka_koloru_green_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                   bg=self.rgb_to_hex(*configFile.first_g_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.first_g_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_green_domyslne.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_green_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda
                                                               x=self.probka_koloru_green_domyslne: self.change_obj_color(
                                                               x))
        self.change_color_green_domyslne_btn.grid(row=5, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 6

        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\nżółtej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=6, column=1, sticky='nsew')
        self.probka_koloru_yellow_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                    bg=self.rgb_to_hex(*configFile.first_y_layer_color),
                                                    fg=self.rgb_to_hex(*configFile.first_y_layer_color),
                                                    font=('OpenSans.ttf', 14))
        self.probka_koloru_yellow_domyslne.grid(row=6, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_yellow_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                            text_font=('OpenSans.ttf', 14),
                                                            fg_color='#505050', hover_color='#404040',
                                                            command=lambda
                                                                x=self.probka_koloru_yellow_domyslne: self.change_obj_color(
                                                                x))
        self.change_color_yellow_domyslne_btn.grid(row=6, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 7

        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\nczerwonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=7, column=1, sticky='nsew')
        self.probka_koloru_red_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                 bg=self.rgb_to_hex(*configFile.first_r_layer_color),
                                                 fg=self.rgb_to_hex(*configFile.first_r_layer_color),
                                                 font=('OpenSans.ttf', 14))
        self.probka_koloru_red_domyslne.grid(row=7, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_red_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                         text_font=('OpenSans.ttf', 14),
                                                         fg_color='#505050', hover_color='#404040',
                                                         command=lambda
                                                             x=self.probka_koloru_red_domyslne: self.change_obj_color(
                                                             x))
        self.change_color_red_domyslne_btn.grid(row=7, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 8
        linetype_values = ['Obszar', 'Linia']
        ### RZAD 8
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy niebieskiej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=8, column=1, sticky='nsew', padx=10, pady=10)
        self.blue_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                                 text_font=('OpenSans.ttf', 14))
        self.blue_first_layer_linetype_choose.grid(row=8, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_b_layer_linetype == 'polygon':
            self.blue_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_b_layer_linetype == 'lines':
            self.blue_first_layer_linetype_choose.set('Linia')

        ### RZAD 9
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy zielonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=9, column=1, sticky='nsew', padx=10, pady=10)
        self.green_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                                  text_font=('OpenSans.ttf', 14))
        self.green_first_layer_linetype_choose.grid(row=9, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_g_layer_linetype == 'polygon':
            self.green_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_g_layer_linetype == 'lines':
            self.green_first_layer_linetype_choose.set('Linia')

        ### RZAD 10
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy żółtej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=10, column=1, sticky='nsew', padx=10, pady=10)
        self.yellow_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                                   text_font=('OpenSans.ttf', 14))
        self.yellow_first_layer_linetype_choose.grid(row=10, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_y_layer_linetype == 'polygon':
            self.yellow_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_y_layer_linetype == 'lines':
            self.yellow_first_layer_linetype_choose.set('Linia')

        ### RZAD 11
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy czerwonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=11, column=1, sticky='nsew', padx=10, pady=10)
        self.red_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                                text_font=('OpenSans.ttf', 14))
        self.red_first_layer_linetype_choose.grid(row=11, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_r_layer_linetype == 'polygon':
            self.red_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_r_layer_linetype == 'lines':
            self.red_first_layer_linetype_choose.set('Linia')

        self.ramka_zk_domyslne.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        ######################################################### poklik
        ### RZAD 1
        tk.Label(self.ramka_zk_poklik, text='Kolor tła:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew')
        self.probka_koloru_tla_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                   bg=self.rgb_to_hex(*configFile.second_bg_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.second_bg_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_poklik.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_tlo_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda x = self.probka_koloru_tla_poklik: self.change_obj_color(x))
        self.change_color_tlo_poklik_btn.grid(row=1, column=3, sticky='nsew', padx=10, pady=10)
        ### RZAD 2
        tk.Label(self.ramka_zk_poklik, text='Kolor warstwy\nkonturu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew')
        self.probka_koloru_konturu_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                       bg=self.rgb_to_hex(*configFile.second_c_layer_color),
                                                       fg=self.rgb_to_hex(*configFile.second_c_layer_color),
                                                       font=('OpenSans.ttf', 14))
        self.probka_koloru_konturu_poklik.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_konturu_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                               text_font=('OpenSans.ttf', 14),
                                                               fg_color='#505050', hover_color='#404040',
                                                               command=lambda x = self.probka_koloru_konturu_poklik: self.change_obj_color(x))
        self.change_color_konturu_poklik_btn.grid(row=2, column=3, sticky='nsew', padx=10, pady=10)
        ### RZAD 3

        tk.Label(self.ramka_zk_poklik, text='Kolor warstwy\ndziur:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=3, column=1, sticky='nsew')
        self.probka_koloru_dziur_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                     bg=self.rgb_to_hex(*configFile.second_h_layer_color),
                                                     fg=self.rgb_to_hex(*configFile.second_h_layer_color),
                                                     font=('OpenSans.ttf', 14))
        self.probka_koloru_dziur_poklik.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_dziur_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                             text_font=('OpenSans.ttf', 14),
                                                             fg_color='#505050', hover_color='#404040',
                                                             command=lambda
                                                                 x=self.probka_koloru_dziur_poklik: self.change_obj_color(
                                                                 x))
        self.change_color_dziur_poklik_btn.grid(row=3, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 4

        tk.Label(self.ramka_zk_poklik, text='Kolor warstwy\nniebieskiej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=4, column=1, sticky='nsew')
        self.probka_koloru_blue_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                   bg=self.rgb_to_hex(*configFile.second_b_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.second_b_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_blue_poklik.grid(row=4, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_blue_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda
                                                               x=self.probka_koloru_blue_poklik: self.change_obj_color(
                                                               x))
        self.change_color_blue_poklik_btn.grid(row=4, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 5

        tk.Label(self.ramka_zk_poklik, text='Kolor warstwy\nzielonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=5, column=1, sticky='nsew')
        self.probka_koloru_green_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                   bg=self.rgb_to_hex(*configFile.second_g_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.second_g_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_green_poklik.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_green_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda
                                                               x=self.probka_koloru_green_poklik: self.change_obj_color(
                                                               x))
        self.change_color_green_poklik_btn.grid(row=5, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 6

        tk.Label(self.ramka_zk_poklik, text='Kolor warstwy\nżółtej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=6, column=1, sticky='nsew')
        self.probka_koloru_yellow_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                   bg=self.rgb_to_hex(*configFile.second_y_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.second_y_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_yellow_poklik.grid(row=6, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_yellow_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda
                                                               x=self.probka_koloru_yellow_poklik: self.change_obj_color(
                                                               x))
        self.change_color_yellow_poklik_btn.grid(row=6, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 7

        tk.Label(self.ramka_zk_poklik, text='Kolor warstwy\nczerwonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=7, column=1, sticky='nsew')
        self.probka_koloru_red_poklik = tk.Label(self.ramka_zk_poklik, text='',
                                                   bg=self.rgb_to_hex(*configFile.second_r_layer_color),
                                                   fg=self.rgb_to_hex(*configFile.second_r_layer_color),
                                                   font=('OpenSans.ttf', 14))
        self.probka_koloru_red_poklik.grid(row=7, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_red_poklik_btn = ctk.CTkButton(self.ramka_zk_poklik, text='Zmień kolor',
                                                           text_font=('OpenSans.ttf', 14),
                                                           fg_color='#505050', hover_color='#404040',
                                                           command=lambda
                                                               x=self.probka_koloru_red_poklik: self.change_obj_color(
                                                               x))
        self.change_color_red_poklik_btn.grid(row=7, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 8
        linetype_values = ['Obszar','Linia']
        ### RZAD 8
        tk.Label(self.ramka_zk_poklik, text='Typ skazy niebieskiej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=8, column=1, sticky='nsew', padx=10, pady=10)
        self.blue_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values, text_font=('OpenSans.ttf', 14))
        self.blue_second_layer_linetype_choose.grid(row=8, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_b_layer_linetype == 'polygon':
            self.blue_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_b_layer_linetype == 'lines':
            self.blue_second_layer_linetype_choose.set('Linia')

        ### RZAD 9
        tk.Label(self.ramka_zk_poklik, text='Typ skazy zielonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=9, column=1, sticky='nsew', padx=10, pady=10)
        self.green_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                          text_font=('OpenSans.ttf', 14))
        self.green_second_layer_linetype_choose.grid(row=9, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_g_layer_linetype == 'polygon':
            self.green_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_g_layer_linetype == 'lines':
            self.green_second_layer_linetype_choose.set('Linia')

        ### RZAD 10
        tk.Label(self.ramka_zk_poklik, text='Typ skazy żółtej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=10, column=1, sticky='nsew', padx=10, pady=10)
        self.yellow_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                           text_font=('OpenSans.ttf', 14))
        self.yellow_second_layer_linetype_choose.grid(row=10, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_y_layer_linetype == 'polygon':
            self.yellow_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_y_layer_linetype == 'lines':
            self.yellow_second_layer_linetype_choose.set('Linia')

        ### RZAD 11
        tk.Label(self.ramka_zk_poklik, text='Typ skazy czerwonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=11, column=1, sticky='nsew', padx=10, pady=10)
        self.red_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                            text_font=('OpenSans.ttf', 14))
        self.red_second_layer_linetype_choose.grid(row=11, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_r_layer_linetype == 'polygon':
            self.red_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_r_layer_linetype == 'lines':
            self.red_second_layer_linetype_choose.set('Linia')




        self.ramka_zk_poklik.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

        self.ramka_zmien_kolory.grid(row=1, column=2, columnspan=2, rowspan=2, sticky='nsew', padx=10, pady=10)




        self.ramka_pozostale = tk.LabelFrame(self.display_tab, text='Ogólne ustawienia', font=('OpenSans.ttf', 13),
                                          bg='#303030', fg='#c7c6c5')
        self.ramka_pozostale.columnconfigure((1,2,3,4,5,6), weight =1)
        self.ramka_pozostale.rowconfigure((1,2,3), weight=1)
        ###
        tk.Label(self.ramka_pozostale, text='Grubość linii\nwarstwy konturu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=5)
        self.c_layer_line_width_entry = ctk.CTkEntry(self.ramka_pozostale, width=50, justify=tk.CENTER,
                                                text_font=('OpenSans.ttf', 14))
        self.c_layer_line_width_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=5)
        self.c_layer_line_width_entry.insert(0, configFile.c_layer_line_width)
        tk.Label(self.ramka_pozostale, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                         column=3,
                                                                                                         sticky='w',
                                                                                                         padx=3,
                                                                                                         pady=10)
        ###
        tk.Label(self.ramka_pozostale, text='Grubość linii\nskazy:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew', padx=10, pady=5)
        self.flaw_line_width_entry = ctk.CTkEntry(self.ramka_pozostale, width=50, justify=tk.CENTER,
                                                      text_font=('OpenSans.ttf', 14))
        self.flaw_line_width_entry.grid(row=2, column=2, sticky='nsew', padx=10, pady=5)
        self.flaw_line_width_entry.insert(0, configFile.flaw_line_width)
        tk.Label(self.ramka_pozostale, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=2,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)
        ###
        tk.Label(self.ramka_pozostale, text='Grubość linii\nrysowanej skazy:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=3, column=1, sticky='nsew', padx=10, pady=5)
        self.new_flaw_line_width_entry = ctk.CTkEntry(self.ramka_pozostale, width=50, justify=tk.CENTER,
                                                     text_font=('OpenSans.ttf', 14))
        self.new_flaw_line_width_entry.grid(row=3, column=2, sticky='nsew', padx=10, pady=5)
        self.new_flaw_line_width_entry.insert(0, configFile.new_flaw_line_width)
        tk.Label(self.ramka_pozostale, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=3,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)
        #####
        tk.Label(self.ramka_pozostale, text='Szerokość otwartej\nskazy:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=4, sticky='nsew', padx=10, pady=5)
        self.open_flaw_line_width_entry = ctk.CTkEntry(self.ramka_pozostale, width=50, justify=tk.CENTER,
                                                      text_font=('OpenSans.ttf', 14))
        self.open_flaw_line_width_entry.grid(row=1, column=5, sticky='nsew', padx=10, pady=5)
        self.open_flaw_line_width_entry.insert(0, configFile.open_flaw_line_width)
        tk.Label(self.ramka_pozostale, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                              column=6,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)
        ###
        tk.Label(self.ramka_pozostale, text='Kolor rysowanej\nskazy:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=2, column=4, sticky='nsew')
        self.probka_koloru_new_flaw = tk.Label(self.ramka_pozostale, text='',
                                                    bg=self.rgb_to_hex(*configFile.new_flaw_color),
                                                    fg=self.rgb_to_hex(*configFile.new_flaw_color),
                                                    font=('OpenSans.ttf', 14))
        self.probka_koloru_new_flaw.grid(row=2, column=5, sticky='nsew', padx=10, pady=5)
        self.change_color_new_flaw_btn = ctk.CTkButton(self.ramka_pozostale, text='Zmień kolor',
                                                            text_font=('OpenSans.ttf', 14),
                                                            fg_color='#505050', hover_color='#404040',
                                                            command=lambda
                                                                x=self.probka_koloru_new_flaw: self.change_obj_color(
                                                                x))
        self.change_color_new_flaw_btn.grid(row=2, column=6, sticky='nsew', padx=10, pady=5)




        self.ramka_pozostale.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)
        #self.ramka_zmien_kolory.grid(row=1, column=2, columnspan=2, rowspan=2, sticky='nsew', padx=10, pady=10)



        ######### ZMIEN KOLORY ###################

    def anuluj_btn_func(self):
        self.destroy()

    def change_path(self, object):
        new_path = filedialog.askdirectory(parent=self)
        object.delete(0, 'end')
        object.insert(0, new_path)
    def change_obj_color(self, object):
        color = askcolor(parent=self, title='Wybierz kolor')
        object.configure(fg=color[1], bg=color[1])
    def rgb_to_hex (self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def hex_to_rgb (self, hex):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(hex[i:i + 2], 16)
            rgb.append(decimal)
        return tuple(rgb)





