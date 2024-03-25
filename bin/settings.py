import json
import os
import sys
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import pyglet
from tkfontawesome import icon_to_image
from PIL import ImageTk, ImageColor, Image
from datetime import datetime
from threading import Thread
import ezdxf
from ezdxf.enums import TextEntityAlignment
from bin import configFile
from tkinter import ttk
from tkinter.colorchooser import askcolor
from bin.messHandler import Error

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
        self.ogolne_tab = ctk.CTkFrame(self.settings_notebook, bg_color='#303030', fg_color='#303030')
        self.display_tab = ctk.CTkFrame(self.settings_notebook, bg_color='#303030', fg_color='#303030')
        #self.calibration_tab = ctk.CTkFrame(self.settings_notebook)

        self.display_tab.columnconfigure((1,2,3), weight =1)
        self.display_tab.rowconfigure((1, 2, 3), weight=1)
        self.ogolne_tab.columnconfigure((1,2,3), weight =1)
        self.ogolne_tab.rowconfigure((2,3,4,5,6), weight=1)

        self.settings_notebook.add(self.ogolne_tab, text='       Ogólne       ')
        self.settings_notebook.add(self.display_tab, text='      Wyświetlanie      ')
        #self.settings_notebook.add(self.calibration_tab, text='      Kalibracja      ')
        self.settings_notebook.grid(row=1, column=1, columnspan=3, sticky='nsew')

        self.save_btn = ctk.CTkButton(self, text = 'Zapisz', fg_color='#505050', hover_color='#606060',
                                      text_font=('OpenSans.ttf', 20), command=lambda:self.save_btn_func(), text_color="#c7c6c5")
        self.save_btn.grid(row=2, column=1, sticky='e', padx=10, pady=10)
        self.ok_btn = ctk.CTkButton(self, text='   OK   ', fg_color='#505050', hover_color='#606060',
                                      text_font=('OpenSans.ttf', 20), command = lambda:self.ok_btn_func(), text_color="#c7c6c5")
        self.ok_btn.grid(row=2, column=2, sticky='e', padx=10, pady=10)
        self.anuluj_btn = ctk.CTkButton(self, text='Anuluj', fg_color='#505050', hover_color='#606060',
                                    text_font=('OpenSans.ttf', 20), command = lambda:self.anuluj_btn_func(), text_color="#c7c6c5")
        self.anuluj_btn.grid(row=2, column=3, sticky='e', padx=10, pady=10)
        ######## OGOLNE TAB
        self.temp_path_list = configFile.leather_path_list.copy()
        self.create_ogolne_frame()
        ######## DISPLAY TAB
        self.create_display_frame()

    def save_btn_func(self):
        configFile.cursor_radius = int(self.cursor_radius_entry.get())
        configFile.cursor_color = self.hex_to_rgb(self.probka_koloru_cursora.cget("bg"))
        configFile.flaw_dropdown_menu_x_size = int(self.szerokosc_menu_skazy_entry.get())
        configFile.flaw_dropdown_menu_y_size = int(self.wysokosc_menu_skazy_entry.get())
        configFile.flaw_dropdown_menu_color = self.hex_to_rgb(self.probka_koloru_tla_menu_skazy.cget("bg"))
        configFile.flaw_dropdown_menu_option_color = self.hex_to_rgb(self.probka_koloru_tla_opcji_menu_skazy.cget("bg"))
        configFile.flaw_dropdown_menu_font_color = self.hex_to_rgb(self.probka_koloru_czcionki_menu_skazy.cget('bg'))
        configFile.dropdown_menu_x_size = int(self.szerokosc_menu_entry.get())
        configFile.dropdown_menu_y_size = int(self.wysokosc_menu_entry.get())
        configFile.dropdown_menu_color = self.hex_to_rgb(self.probka_koloru_tla_menu.cget('bg'))
        configFile.dropdown_menu_option_color = self.hex_to_rgb(self.probka_koloru_tla_opcji_menu.cget("bg"))
        configFile.dropdown_menu_font_color = self.hex_to_rgb(self.probka_koloru_czcionki_menu.cget("bg"))
        configFile.first_bg_layer_color = self.hex_to_rgb(self.probka_koloru_tla_domyslne.cget("bg"))
        configFile.first_c_layer_color = self.hex_to_rgb(self.probka_koloru_konturu_domyslne.cget("bg"))
        configFile.first_h_layer_color = self.hex_to_rgb(self.probka_koloru_dziur_domyslne.cget('bg'))
        configFile.first_b_layer_color = self.hex_to_rgb(self.probka_koloru_blue_domyslne.cget('bg'))
        configFile.first_g_layer_color = self.hex_to_rgb(self.probka_koloru_green_domyslne.cget('bg'))
        configFile.first_y_layer_color = self.hex_to_rgb(self.probka_koloru_yellow_domyslne.cget('bg'))
        configFile.first_r_layer_color = self.hex_to_rgb(self.probka_koloru_red_domyslne.cget('bg'))
        if self.blue_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_b_layer_linetype = 'polygon'
        elif self.blue_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_b_layer_linetype = 'lines'
        if self.green_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_g_layer_linetype = 'polygon'
        elif self.green_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_g_layer_linetype = 'lines'
        if self.yellow_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_y_layer_linetype = 'polygon'
        elif self.yellow_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_y_layer_linetype = 'lines'
        if self.red_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_r_layer_linetype = 'polygon'
        elif self.red_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_r_layer_linetype = 'lines'
        configFile.second_bg_layer_color = self.hex_to_rgb(self.probka_koloru_tla_poklik.cget('bg'))
        configFile.second_c_layer_color = self.hex_to_rgb(self.probka_koloru_konturu_poklik.cget('bg'))
        configFile.second_h_layer_color = self.hex_to_rgb(self.probka_koloru_dziur_poklik.cget('bg'))
        configFile.second_b_layer_color = self.hex_to_rgb(self.probka_koloru_blue_poklik.cget('bg'))
        configFile.second_g_layer_color = self.hex_to_rgb(self.probka_koloru_green_poklik.cget('bg'))
        configFile.second_y_layer_color = self.hex_to_rgb(self.probka_koloru_yellow_poklik.cget('bg'))
        configFile.second_r_layer_color = self.hex_to_rgb(self.probka_koloru_red_poklik.cget('bg'))
        if self.blue_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_b_layer_linetype = 'polygon'
        elif self.blue_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_b_layer_linetype = 'lines'
        if self.green_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_g_layer_linetype = 'polygon'
        elif self.green_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_g_layer_linetype = 'lines'
        if self.yellow_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_y_layer_linetype = 'polygon'
        elif self.yellow_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_y_layer_linetype = 'lines'
        if self.red_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_r_layer_linetype = 'polygon'
        elif self.red_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_r_layer_linetype = 'lines'
        configFile.c_layer_line_width = int(self.c_layer_line_width_entry.get())
        configFile.flaw_line_width = int(self.flaw_line_width_entry.get())
        configFile.new_flaw_line_width = int(self.new_flaw_line_width_entry.get())
        configFile.new_flaw_color = self.hex_to_rgb(self.probka_koloru_new_flaw.cget('bg'))
        configFile.open_flaw_line_width = int(self.open_flaw_line_width_entry.get())
        configFile.leather_backup_path = str(self.bckp_path_entry.get())
        dirs = []
        for sciezka in self.sciezki_entry_list:
            dirs.append(str(sciezka.get()))
        configFile.leather_path_list = dirs
        configFile.domyslne_leather_path = int(self.check_var.get())
        configFile.barcode_com_port = str(self.barcode_port_choose.get())

        sett = [
            configFile.cursor_radius,
            configFile.cursor_color,
            configFile.flaw_dropdown_menu_x_size,
            configFile.flaw_dropdown_menu_y_size,
            configFile.flaw_dropdown_menu_color,
            configFile.flaw_dropdown_menu_option_color,
            configFile.flaw_dropdown_menu_font_color,
            configFile.dropdown_menu_x_size,
            configFile.dropdown_menu_y_size,
            configFile.dropdown_menu_color,
            configFile.dropdown_menu_option_color,
            configFile.dropdown_menu_font_color,
            configFile.first_bg_layer_color,
            configFile.first_c_layer_color,
            configFile.first_h_layer_color,
            configFile.first_b_layer_color,
            configFile.first_g_layer_color,
            configFile.first_y_layer_color,
            configFile.first_r_layer_color,
            configFile.first_b_layer_linetype,
            configFile.first_g_layer_linetype,
            configFile.first_y_layer_linetype,
            configFile.first_r_layer_linetype,
            configFile.second_bg_layer_color,
            configFile.second_c_layer_color,
            configFile.second_h_layer_color,
            configFile.second_b_layer_color,
            configFile.second_g_layer_color,
            configFile.second_y_layer_color,
            configFile.second_r_layer_color,
            configFile.second_b_layer_linetype,
            configFile.second_g_layer_linetype,
            configFile.second_y_layer_linetype,
            configFile.second_r_layer_linetype,
            configFile.c_layer_line_width,
            configFile.flaw_line_width,
            configFile.new_flaw_line_width,
            configFile.new_flaw_color,
            configFile.open_flaw_line_width,
            configFile.leather_backup_path,
            configFile.leather_path_list,
            configFile.domyslne_leather_path,
            configFile.barcode_com_port
        ]
        self.queue.put(['preview_settings', sett])
        self.queue.put(['main_settings', sett])
        sett_keys = [
            "cursor_radius",
            "cursor_color",
            "flaw_dropdown_menu_x_size",
            "flaw_dropdown_menu_y_size",
            "flaw_dropdown_menu_color",
            "flaw_dropdown_menu_option_color",
            "flaw_dropdown_menu_font_color",
            "dropdown_menu_x_size",
            "dropdown_menu_y_size",
            "dropdown_menu_color",
            "dropdown_menu_option_color",
            "dropdown_menu_font_color",
            "first_bg_layer_color",
            "first_c_layer_color",
            "first_h_layer_color",
            "first_b_layer_color",
            "first_g_layer_color",
            "first_y_layer_color",
            "first_r_layer_color",
            "first_b_layer_linetype",
            "first_g_layer_linetype",
            "first_y_layer_linetype",
            "first_r_layer_linetype",
            "second_bg_layer_color",
            "second_c_layer_color",
            "second_h_layer_color",
            "second_b_layer_color",
            "second_g_layer_color",
            "second_y_layer_color",
            "second_r_layer_color",
            "second_b_layer_linetype",
            "second_g_layer_linetype",
            "second_y_layer_linetype",
            "second_r_layer_linetype",
            "c_layer_line_width",
            "flaw_line_width",
            "new_flaw_line_width",
            "new_flaw_color",
            "open_flaw_line_width",
            "leather_backup_path",
            "leather_path_list",
            "domyslne_leather_path",
            "barcode_com_port"
        ]
        sett_values = [
            configFile.cursor_radius,
            configFile.cursor_color,
            configFile.flaw_dropdown_menu_x_size,
            configFile.flaw_dropdown_menu_y_size,
            configFile.flaw_dropdown_menu_color,
            configFile.flaw_dropdown_menu_option_color,
            configFile.flaw_dropdown_menu_font_color,
            configFile.dropdown_menu_x_size,
            configFile.dropdown_menu_y_size,
            configFile.dropdown_menu_color,
            configFile.dropdown_menu_option_color,
            configFile.dropdown_menu_font_color,
            configFile.first_bg_layer_color,
            configFile.first_c_layer_color,
            configFile.first_h_layer_color,
            configFile.first_b_layer_color,
            configFile.first_g_layer_color,
            configFile.first_y_layer_color,
            configFile.first_r_layer_color,
            configFile.first_b_layer_linetype,
            configFile.first_g_layer_linetype,
            configFile.first_y_layer_linetype,
            configFile.first_r_layer_linetype,
            configFile.second_bg_layer_color,
            configFile.second_c_layer_color,
            configFile.second_h_layer_color,
            configFile.second_b_layer_color,
            configFile.second_g_layer_color,
            configFile.second_y_layer_color,
            configFile.second_r_layer_color,
            configFile.second_b_layer_linetype,
            configFile.second_g_layer_linetype,
            configFile.second_y_layer_linetype,
            configFile.second_r_layer_linetype,
            configFile.c_layer_line_width,
            configFile.flaw_line_width,
            configFile.new_flaw_line_width,
            configFile.new_flaw_color,
            configFile.open_flaw_line_width,
            configFile.leather_backup_path,
            configFile.leather_path_list,
            configFile.domyslne_leather_path,
            configFile.barcode_com_port,
        ]
        sett_dict = dict(zip(sett_keys, sett_values))
        print(sett_dict)
        with open('config.json', 'w') as file:
            json.dump(sett_dict, file)
        header = "Informacja"
        mess1 = "Ustawienia zostały zapisane."
        Error(self.parent, self.queue, mess1, None, header)



    def ok_btn_func(self):
        configFile.cursor_radius = int(self.cursor_radius_entry.get())
        configFile.cursor_color = self.hex_to_rgb(self.probka_koloru_cursora.cget("bg"))
        configFile.flaw_dropdown_menu_x_size = int(self.szerokosc_menu_skazy_entry.get())
        configFile.flaw_dropdown_menu_y_size = int(self.wysokosc_menu_skazy_entry.get())
        configFile.flaw_dropdown_menu_color = self.hex_to_rgb(self.probka_koloru_tla_menu_skazy.cget("bg"))
        configFile.flaw_dropdown_menu_option_color = self.hex_to_rgb(self.probka_koloru_tla_opcji_menu_skazy.cget("bg"))
        configFile.flaw_dropdown_menu_font_color = self.hex_to_rgb(self.probka_koloru_czcionki_menu_skazy.cget('bg'))
        configFile.dropdown_menu_x_size = int(self.szerokosc_menu_entry.get())
        configFile.dropdown_menu_y_size = int(self.wysokosc_menu_entry.get())
        configFile.dropdown_menu_color = self.hex_to_rgb(self.probka_koloru_tla_menu.cget('bg'))
        configFile.dropdown_menu_option_color = self.hex_to_rgb(self.probka_koloru_tla_opcji_menu.cget("bg"))
        configFile.dropdown_menu_font_color = self.hex_to_rgb(self.probka_koloru_czcionki_menu.cget("bg"))
        configFile.first_bg_layer_color = self.hex_to_rgb(self.probka_koloru_tla_domyslne.cget("bg"))
        configFile.first_c_layer_color = self.hex_to_rgb(self.probka_koloru_konturu_domyslne.cget("bg"))
        configFile.first_h_layer_color = self.hex_to_rgb(self.probka_koloru_dziur_domyslne.cget('bg'))
        configFile.first_b_layer_color = self.hex_to_rgb(self.probka_koloru_blue_domyslne.cget('bg'))
        configFile.first_g_layer_color = self.hex_to_rgb(self.probka_koloru_green_domyslne.cget('bg'))
        configFile.first_y_layer_color = self.hex_to_rgb(self.probka_koloru_yellow_domyslne.cget('bg'))
        configFile.first_r_layer_color = self.hex_to_rgb(self.probka_koloru_red_domyslne.cget('bg'))
        if self.blue_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_b_layer_linetype = 'polygon'
        elif self.blue_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_b_layer_linetype = 'lines'
        if self.green_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_g_layer_linetype = 'polygon'
        elif self.green_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_g_layer_linetype = 'lines'
        if self.yellow_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_y_layer_linetype = 'polygon'
        elif self.yellow_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_y_layer_linetype = 'lines'
        if self.red_first_layer_linetype_choose.get() == 'Obszar':
            configFile.first_r_layer_linetype = 'polygon'
        elif self.red_first_layer_linetype_choose.get() == 'Linia':
            configFile.first_r_layer_linetype = 'lines'
        configFile.second_bg_layer_color = self.hex_to_rgb(self.probka_koloru_tla_poklik.cget('bg'))
        configFile.second_c_layer_color = self.hex_to_rgb(self.probka_koloru_konturu_poklik.cget('bg'))
        configFile.second_h_layer_color = self.hex_to_rgb(self.probka_koloru_dziur_poklik.cget('bg'))
        configFile.second_b_layer_color = self.hex_to_rgb(self.probka_koloru_blue_poklik.cget('bg'))
        configFile.second_g_layer_color = self.hex_to_rgb(self.probka_koloru_green_poklik.cget('bg'))
        configFile.second_y_layer_color = self.hex_to_rgb(self.probka_koloru_yellow_poklik.cget('bg'))
        configFile.second_r_layer_color = self.hex_to_rgb(self.probka_koloru_red_poklik.cget('bg'))
        if self.blue_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_b_layer_linetype = 'polygon'
        elif self.blue_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_b_layer_linetype = 'lines'
        if self.green_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_g_layer_linetype = 'polygon'
        elif self.green_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_g_layer_linetype = 'lines'
        if self.yellow_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_y_layer_linetype = 'polygon'
        elif self.yellow_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_y_layer_linetype = 'lines'
        if self.red_second_layer_linetype_choose.get() == 'Obszar':
            configFile.second_r_layer_linetype = 'polygon'
        elif self.red_second_layer_linetype_choose.get() == 'Linia':
            configFile.second_r_layer_linetype = 'lines'
        configFile.c_layer_line_width = int(self.c_layer_line_width_entry.get())
        configFile.flaw_line_width = int(self.flaw_line_width_entry.get())
        configFile.new_flaw_line_width = int(self.new_flaw_line_width_entry.get())
        configFile.new_flaw_color = self.hex_to_rgb(self.probka_koloru_new_flaw.cget('bg'))
        configFile.open_flaw_line_width = int(self.open_flaw_line_width_entry.get())
        configFile.leather_backup_path = str(self.bckp_path_entry.get())
        dirs = []
        for sciezka in self.sciezki_entry_list:
            dirs.append(str(sciezka.get()))
        configFile.leather_path_list = dirs
        configFile.domyslne_leather_path = int(self.check_var.get())
        configFile.barcode_com_port = str(self.barcode_port_choose.get())

        sett = [
        configFile.cursor_radius,
        configFile.cursor_color,
        configFile.flaw_dropdown_menu_x_size,
        configFile.flaw_dropdown_menu_y_size,
        configFile.flaw_dropdown_menu_color,
        configFile.flaw_dropdown_menu_option_color,
        configFile.flaw_dropdown_menu_font_color,
        configFile.dropdown_menu_x_size,
        configFile.dropdown_menu_y_size,
        configFile.dropdown_menu_color,
        configFile.dropdown_menu_option_color,
        configFile.dropdown_menu_font_color,
        configFile.first_bg_layer_color,
        configFile.first_c_layer_color,
        configFile.first_h_layer_color,
        configFile.first_b_layer_color,
        configFile.first_g_layer_color,
        configFile.first_y_layer_color,
        configFile.first_r_layer_color,
        configFile.first_b_layer_linetype,
        configFile.first_g_layer_linetype,
        configFile.first_y_layer_linetype,
        configFile.first_r_layer_linetype,
        configFile.second_bg_layer_color,
        configFile.second_c_layer_color,
        configFile.second_h_layer_color,
        configFile.second_b_layer_color,
        configFile.second_g_layer_color,
        configFile.second_y_layer_color,
        configFile.second_r_layer_color,
        configFile.second_b_layer_linetype,
        configFile.second_g_layer_linetype,
        configFile.second_y_layer_linetype,
        configFile.second_r_layer_linetype,
        configFile.c_layer_line_width,
        configFile.flaw_line_width,
        configFile.new_flaw_line_width,
        configFile.new_flaw_color,
        configFile.open_flaw_line_width,
        configFile.leather_backup_path,
        configFile.leather_path_list,
        configFile.domyslne_leather_path,
        configFile.barcode_com_port
        ]
        self.queue.put(['preview_settings', sett])
        self.queue.put(['main_settings', sett])
        self.anuluj_btn_func()
    def anuluj_btn_func(self):
        self.destroy()

    def create_display_frame(self):
        self.ramka_cursor = tk.LabelFrame(self.display_tab, text='Opcje kursora', font=('OpenSans.ttf', 13),
                                          bg='#303030', fg='#c7c6c5')
        self.ramka_cursor.columnconfigure((1, 2, 3), weight=1)
        self.ramka_cursor.rowconfigure((1, 2), weight=1)
        tk.Label(self.ramka_cursor, text='Średnica kursora:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.cursor_radius_entry = ctk.CTkEntry(self.ramka_cursor, width=50, justify=tk.CENTER,
                                                text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
        self.cursor_radius_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.cursor_radius_entry.insert(0, configFile.cursor_radius)
        tk.Label(self.ramka_cursor, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                           column=3,
                                                                                                           sticky='w',
                                                                                                           padx=3,
                                                                                                           pady=10)

        tk.Label(self.ramka_cursor, text='Kolor kursora:', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew', padx=10, pady=10)
        self.probka_koloru_cursora = tk.Label(self.ramka_cursor, text=' ', bg=self.rgb_to_hex(*configFile.cursor_color),
                                              fg=self.rgb_to_hex(*configFile.cursor_color), font=('OpenSans.ttf', 14))
        self.probka_koloru_cursora.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_cursor_btn = ctk.CTkButton(self.ramka_cursor, text='Zmień kolor',
                                                     text_font=('OpenSans.ttf', 14),
                                                     fg_color='#505050', hover_color='#404040',
                                                     command=lambda x=self.probka_koloru_cursora: self.change_obj_color(
                                                         x), text_color="#c7c6c5")
        self.change_color_cursor_btn.grid(row=2, column=3, sticky='nsew', padx=10, pady=10)
        self.ramka_cursor.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)

        self.ramka_flaw_menu = tk.LabelFrame(self.display_tab, text='Opcje menu na skazie', font=('OpenSans.ttf', 13),
                                             bg='#303030', fg='#c7c6c5')
        self.ramka_flaw_menu.columnconfigure((1, 2, 3), weight=1)
        self.ramka_flaw_menu.rowconfigure((1, 2, 3, 4, 5), weight=1)

        tk.Label(self.ramka_flaw_menu, text='Szerokość menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=10)
        self.szerokosc_menu_skazy_entry = ctk.CTkEntry(self.ramka_flaw_menu, width=70, justify=tk.CENTER,
                                                       text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
        self.szerokosc_menu_skazy_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.szerokosc_menu_skazy_entry.insert(0, configFile.flaw_dropdown_menu_x_size)
        tk.Label(self.ramka_flaw_menu, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)

        tk.Label(self.ramka_flaw_menu, text='Wysokość menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew')
        self.wysokosc_menu_skazy_entry = ctk.CTkEntry(self.ramka_flaw_menu, width=70, justify=tk.CENTER,
                                                      text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
        self.wysokosc_menu_skazy_entry.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.wysokosc_menu_skazy_entry.insert(0, configFile.flaw_dropdown_menu_y_size)
        tk.Label(self.ramka_flaw_menu, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=2,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)

        tk.Label(self.ramka_flaw_menu, text='Kolor tła menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=3, column=1, sticky='nsew')
        self.probka_koloru_tla_menu_skazy = tk.Label(self.ramka_flaw_menu, text=' ',
                                                     bg=self.rgb_to_hex(*configFile.flaw_dropdown_menu_color),
                                                     fg=self.rgb_to_hex(*configFile.flaw_dropdown_menu_color),
                                                     font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_menu_skazy.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_flaw_tlo_btn = ctk.CTkButton(self.ramka_flaw_menu, text='Zmień kolor',
                                                       text_font=('OpenSans.ttf', 14),
                                                       fg_color='#505050', hover_color='#404040',
                                                       command=lambda
                                                           x=self.probka_koloru_tla_menu_skazy: self.change_obj_color(
                                                           x), text_color="#c7c6c5")
        self.change_color_flaw_tlo_btn.grid(row=3, column=3, sticky='nsew', padx=10, pady=10)

        tk.Label(self.ramka_flaw_menu, text='Kolor tła\nopcji menu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=4, column=1, sticky='nsew')
        self.probka_koloru_tla_opcji_menu_skazy = tk.Label(self.ramka_flaw_menu, text=' ',
                                                           bg=self.rgb_to_hex(
                                                               *configFile.flaw_dropdown_menu_option_color),
                                                           fg=self.rgb_to_hex(
                                                               *configFile.flaw_dropdown_menu_option_color),
                                                           font=('OpenSans.ttf', 14))
        self.probka_koloru_tla_opcji_menu_skazy.grid(row=4, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_flaw_tlo_opcji_btn = ctk.CTkButton(self.ramka_flaw_menu, text='Zmień kolor',
                                                             text_font=('OpenSans.ttf', 14),
                                                             fg_color='#505050', hover_color='#404040',
                                                             command=lambda
                                                                 x=self.probka_koloru_tla_opcji_menu_skazy: self.change_obj_color(
                                                                 x), text_color="#c7c6c5")
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
                                                        command=lambda
                                                            x=self.probka_koloru_czcionki_menu_skazy: self.change_obj_color(
                                                            x), text_color="#c7c6c5")
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
                                                 text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
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
                                                text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
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
                                                  command=lambda x=self.probka_koloru_tla_menu: self.change_obj_color(
                                                      x), text_color="#c7c6c5")
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
                                                        command=lambda
                                                            x=self.probka_koloru_tla_opcji_menu: self.change_obj_color(
                                                            x), text_color="#c7c6c5")
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
                                                   command=lambda
                                                       x=self.probka_koloru_czcionki_menu: self.change_obj_color(x), text_color="#c7c6c5")
        self.change_color_font_btn.grid(row=5, column=3, sticky='nsew', padx=10, pady=10)
        self.ramka_menu.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        ######### ZMIEN KOLORY ###################

        self.ramka_zmien_kolory = tk.LabelFrame(self.display_tab, text='Opcje funkcji zmień kolory',
                                                font=('OpenSans.ttf', 13),
                                                bg='#303030', fg='#c7c6c5')
        self.ramka_zmien_kolory.columnconfigure((1, 2), weight=1)
        self.ramka_zmien_kolory.rowconfigure((1), weight=1)

        self.ramka_zk_domyslne = tk.LabelFrame(self.ramka_zmien_kolory, text='Opcje domyślne',
                                               font=('OpenSans.ttf', 13),
                                               bg='#303030', fg='#c7c6c5')
        self.ramka_zk_poklik = tk.LabelFrame(self.ramka_zmien_kolory, text='Opcje po kliknięciu',
                                             font=('OpenSans.ttf', 13),
                                             bg='#303030', fg='#c7c6c5')

        self.ramka_zk_domyslne.columnconfigure((1, 2, 3), weight=1)
        self.ramka_zk_domyslne.rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.ramka_zk_poklik.columnconfigure((1, 2, 3), weight=1)
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
                                                           command=lambda
                                                               x=self.probka_koloru_tla_domyslne: self.change_obj_color(
                                                               x), text_color="#c7c6c5")
        self.change_color_tlo_domyslne_btn.grid(row=1, column=3, sticky='nsew', padx=10, pady=10)

        ### 2 rzad
        tk.Label(self.ramka_zk_domyslne, text='Kolor warstwy\nkonturu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=2, column=1, sticky='nsew')
        self.probka_koloru_konturu_domyslne = tk.Label(self.ramka_zk_domyslne, text='',
                                                       bg=self.rgb_to_hex(*configFile.first_c_layer_color),
                                                       fg=self.rgb_to_hex(*configFile.first_c_layer_color),
                                                       font=('OpenSans.ttf', 14))
        self.probka_koloru_konturu_domyslne.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)
        self.change_color_konturu_domyslne_btn = ctk.CTkButton(self.ramka_zk_domyslne, text='Zmień kolor',
                                                               text_font=('OpenSans.ttf', 14),
                                                               fg_color='#505050', hover_color='#404040',
                                                               command=lambda
                                                                   x=self.probka_koloru_konturu_domyslne: self.change_obj_color(
                                                                   x), text_color="#c7c6c5")
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
                                                                 x), text_color="#c7c6c5")
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
                                                                x), text_color="#c7c6c5")
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
                                                                 x), text_color="#c7c6c5")
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
                                                                  x), text_color="#c7c6c5")
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
                                                               x), text_color="#c7c6c5")
        self.change_color_red_domyslne_btn.grid(row=7, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 8
        linetype_values = ['Obszar', 'Linia']
        ### RZAD 8
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy niebieskiej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=8, column=1, sticky='nsew', padx=10, pady=10)
        self.blue_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values, text_font=('OpenSans.ttf', 14)
                                                                ,dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.blue_first_layer_linetype_choose.grid(row=8, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_b_layer_linetype == 'polygon':
            self.blue_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_b_layer_linetype == 'lines':
            self.blue_first_layer_linetype_choose.set('Linia')

        ### RZAD 9
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy zielonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=9, column=1, sticky='nsew', padx=10, pady=10)
        self.green_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                                 text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.green_first_layer_linetype_choose.grid(row=9, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_g_layer_linetype == 'polygon':
            self.green_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_g_layer_linetype == 'lines':
            self.green_first_layer_linetype_choose.set('Linia')

        ### RZAD 10
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy żółtej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=10, column=1, sticky='nsew', padx=10, pady=10)
        self.yellow_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                                  text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.yellow_first_layer_linetype_choose.grid(row=10, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.first_y_layer_linetype == 'polygon':
            self.yellow_first_layer_linetype_choose.set('Obszar')
        elif configFile.first_y_layer_linetype == 'lines':
            self.yellow_first_layer_linetype_choose.set('Linia')

        ### RZAD 11
        tk.Label(self.ramka_zk_domyslne, text='Typ skazy czerwonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=11, column=1, sticky='nsew', padx=10, pady=10)
        self.red_first_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_domyslne, values=linetype_values,
                                                               text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
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
                                                         command=lambda
                                                             x=self.probka_koloru_tla_poklik: self.change_obj_color(x), text_color="#c7c6c5")
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
                                                             command=lambda
                                                                 x=self.probka_koloru_konturu_poklik: self.change_obj_color(
                                                                 x), text_color="#c7c6c5")
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
                                                               x), text_color="#c7c6c5")
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
                                                              x), text_color="#c7c6c5")
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
                                                               x), text_color="#c7c6c5")
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
                                                                x), text_color="#c7c6c5")
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
                                                             x), text_color="#c7c6c5")
        self.change_color_red_poklik_btn.grid(row=7, column=3, sticky='nsew', padx=10, pady=10)

        ### RZAD 8
        linetype_values = ['Obszar', 'Linia']
        ### RZAD 8
        tk.Label(self.ramka_zk_poklik, text='Typ skazy niebieskiej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=8, column=1, sticky='nsew', padx=10, pady=10)
        self.blue_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                                 text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.blue_second_layer_linetype_choose.grid(row=8, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_b_layer_linetype == 'polygon':
            self.blue_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_b_layer_linetype == 'lines':
            self.blue_second_layer_linetype_choose.set('Linia')

        ### RZAD 9
        tk.Label(self.ramka_zk_poklik, text='Typ skazy zielonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=9, column=1, sticky='nsew', padx=10, pady=10)
        self.green_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                                  text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.green_second_layer_linetype_choose.grid(row=9, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_g_layer_linetype == 'polygon':
            self.green_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_g_layer_linetype == 'lines':
            self.green_second_layer_linetype_choose.set('Linia')

        ### RZAD 10
        tk.Label(self.ramka_zk_poklik, text='Typ skazy żółtej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=10, column=1, sticky='nsew', padx=10, pady=10)
        self.yellow_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                                   text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.yellow_second_layer_linetype_choose.grid(row=10, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_y_layer_linetype == 'polygon':
            self.yellow_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_y_layer_linetype == 'lines':
            self.yellow_second_layer_linetype_choose.set('Linia')

        ### RZAD 11
        tk.Label(self.ramka_zk_poklik, text='Typ skazy czerwonej:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=11, column=1, sticky='nsew', padx=10, pady=10)
        self.red_second_layer_linetype_choose = ctk.CTkComboBox(self.ramka_zk_poklik, values=linetype_values,
                                                                text_font=('OpenSans.ttf', 14),dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.red_second_layer_linetype_choose.grid(row=11, column=2, sticky='nsew', padx=10, pady=5)
        if configFile.second_r_layer_linetype == 'polygon':
            self.red_second_layer_linetype_choose.set('Obszar')
        elif configFile.second_r_layer_linetype == 'lines':
            self.red_second_layer_linetype_choose.set('Linia')

        self.ramka_zk_poklik.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)

        self.ramka_zmien_kolory.grid(row=1, column=2, columnspan=2, rowspan=2, sticky='nsew', padx=10, pady=10)

        self.ramka_pozostale = tk.LabelFrame(self.display_tab, text='Ogólne ustawienia', font=('OpenSans.ttf', 13),
                                             bg='#303030', fg='#c7c6c5')
        self.ramka_pozostale.columnconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.ramka_pozostale.rowconfigure((1, 2), weight=1)
        ###
        tk.Label(self.ramka_pozostale, text='Grubość linii\nwarstwy konturu:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=5)
        self.c_layer_line_width_entry = ctk.CTkEntry(self.ramka_pozostale, width=50, justify=tk.CENTER,
                                                     text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
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
                                                  text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
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
            row=1, column=4, sticky='nsew', padx=10, pady=5)
        self.new_flaw_line_width_entry = ctk.CTkEntry(self.ramka_pozostale, width=50, justify=tk.CENTER,
                                                      text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
        self.new_flaw_line_width_entry.grid(row=1, column=5, sticky='nsew', padx=10, pady=5)
        self.new_flaw_line_width_entry.insert(0, configFile.new_flaw_line_width)
        tk.Label(self.ramka_pozostale, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                              column=6,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)
        #####
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
                                                           x), text_color="#c7c6c5")
        self.change_color_new_flaw_btn.grid(row=2, column=6, sticky='nsew', padx=10, pady=5)

        self.ramka_pozostale.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)

    def create_ogolne_frame(self):
        self.create_sciezki_frame()
        #ramka otwarta skaza
        self.ramka_otw_skaza = tk.LabelFrame(self.ogolne_tab, text='Opcje otwieranej skazy', font=('OpenSans.ttf', 13),
                                           bg='#303030', fg='#c7c6c5')
        tk.Label(self.ramka_otw_skaza, text='Szerokość otwartej skazy:', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(
            row=1, column=1, sticky='nsew', padx=10, pady=5)
        self.open_flaw_line_width_entry = ctk.CTkEntry(self.ramka_otw_skaza, width=50, justify=tk.CENTER,
                                                       text_font=('OpenSans.ttf', 14), fg_color='#303030', text_color="#c7c6c5")
        self.open_flaw_line_width_entry.grid(row=1, column=2, sticky='nsew', padx=10, pady=5)
        self.open_flaw_line_width_entry.insert(0, configFile.open_flaw_line_width)
        tk.Label(self.ramka_otw_skaza, text='Px', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1,
                                                                                                              column=3,
                                                                                                              sticky='w',
                                                                                                              padx=3,
                                                                                                              pady=10)
        self.ramka_otw_skaza.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        #ramka barcode
        self.ramka_barcode = tk.LabelFrame(self.ogolne_tab, text='Opcje czytnika', font=('OpenSans.ttf', 13),
                                           bg='#303030', fg='#c7c6c5')

        tk.Label(self.ramka_barcode, text='Port czytnika:',
                 bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=1, sticky='nsew', padx=5, pady=3)

        com_values = ["COM%s" % str(i) for i in range(1,14)]
        self.barcode_port_choose = ctk.CTkComboBox(self.ramka_barcode, values=com_values, text_font=('OpenSans.ttf', 14)
                                                                ,dropdown_text_font=('OpenSans.ttf', 14), text_color='#c7c6c5',fg_color='#303030',dropdown_color='#303030', dropdown_hover_color="#606060", dropdown_text_color='#c7c6c5')
        self.barcode_port_choose.grid(row=1, column=2, sticky='nsew', padx=10, pady=10)
        self.barcode_port_choose.set(configFile.barcode_com_port)
        self.ramka_barcode.grid(row=1, column=3, sticky='nsew', padx=10, pady=10)

        #ramka displays

        self.ramka_displays = tk.LabelFrame(self.ogolne_tab, text='Opcje ekranu', font=('OpenSans.ttf', 13),
                                           bg='#303030', fg='#c7c6c5')

        self.ramka_displays.rowconfigure((2,5), weight=1)
        self.ramka_displays.columnconfigure((1,2), weight=1)
        self.ramka_displays.grid_propagate(0)
        tk.Label(self.ramka_displays, text='Wybierz pozycję drugiego ekranu\npierwszy musi być ustawiony jako główny.',
                 bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=1, columnspan=4, sticky='nsew', padx=10, pady=10)

        size = 100,100



        screen_up_img = ImageTk.PhotoImage(file='images/main_up.png')
        screen_up_label = tk.Label(self.ramka_displays, image=screen_up_img, bg="#303030")
        screen_up_label.photo = screen_up_img
        screen_up_label.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

        screen_right_img = ImageTk.PhotoImage(file='images/main_right.png')
        screen_right_label = tk.Label(self.ramka_displays, image=screen_right_img, bg="#303030")
        screen_right_label.photo = screen_right_img
        screen_right_label.grid(row=5, column=1, sticky='nsew', padx=10, pady=10)

        screen_left_img = ImageTk.PhotoImage(file='images/main_left.png')
        screen_left_label = tk.Label(self.ramka_displays, image=screen_left_img, bg="#303030")
        screen_left_label.photo = screen_left_img
        screen_left_label.grid(row=5, column=2, sticky='nsew', padx=10, pady=10)

        screen_down_img = ImageTk.PhotoImage(file='images/main_down.png')
        screen_down_label = tk.Label(self.ramka_displays, image=screen_down_img, bg="#303030")
        screen_down_label.photo = screen_down_img
        screen_down_label.grid(row=2, column=2, sticky='nsew', padx=10, pady=10)

        self.ramka_displays.grid(row=2, column=2, columnspan=2, rowspan=4, sticky='nsew', padx=10, pady=10)

        #ramka backup
        self.ramka_backup = tk.LabelFrame(self.ogolne_tab, text='Lokalizacja backupu plików', font=('OpenSans.ttf', 13),
                                          bg='#303030', fg='#c7c6c5')
        self.ramka_backup.rowconfigure((1,2), weight=1)
        self.ramka_backup.columnconfigure((1,2), weight=1)
        tk.Label(self.ramka_backup, text='Ścieżka do folderu w którym mają się zapisywać kopie zapasowe plików skór',
                 bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=1, columnspan=2, sticky='nsew', padx=5, pady=3)
        self.bckp_path_entry = ctk.CTkEntry(self.ramka_backup, width=400, justify=tk.LEFT, text_font=('OpenSans.ttf', 13), fg_color='#303030', text_color="#c7c6c5")
        self.bckp_path_entry.grid(row=2, column=1, sticky='nsew', padx=5, pady=3)
        self.bckp_path_entry.insert(0, configFile.leather_backup_path)
        change_bckp_path_btn = ctk.CTkButton(self.ramka_backup, text='Zmień ścieżkę', text_font=('OpenSans.ttf', 14),
                                             fg_color='#505050', hover_color='#404040', text_color="#c7c6c5",
                                             command=lambda x=self.bckp_path_entry: self.change_path(x))
        change_bckp_path_btn.grid(row=2, column=2, sticky='nsew', padx=5, pady=3)

        self.ramka_backup.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)
        ###
    def create_sciezki_frame(self):

        self.ramka_sciezki = tk.LabelFrame(self.ogolne_tab, text='Lokalizacje plików skór',
                                               font=('OpenSans.ttf', 13),
                                               bg='#303030', fg='#c7c6c5')

        row_list = [i+2 for i, j in enumerate(self.temp_path_list)]
        self.ramka_sciezki.rowconfigure(row_list, weight=1)
        self.sciezki_entry_list = []
        self.sciezki_button_list = []
        self.sciezki_radio_list = []
        self.radio_var = tk.IntVar()

        tk.Label(self.ramka_sciezki,
                 text='Ścieżki do folderów zawierających skany skór:\n(Używane do wyszukiwania skór przy skanowaniu kodów kreskowych)',
                 bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=1, columnspan=3, sticky='nsew', padx=5, pady=3)
        tk.Label(self.ramka_sciezki, text='Domyślne dla opcji\n"wybierz plik', bg='#303030', fg='#c7c6c5',
                 font=('OpenSans.ttf', 14)).grid(row=1, column=4, sticky='nsew', padx=5, pady=3)
        self.check_var = tk.IntVar(self)

        for index, path in enumerate(self.temp_path_list):
            row_index = index + 2
            tk.Label(self.ramka_sciezki, text='Ścieżka %s:' % str(index + 1), bg='#303030', fg='#c7c6c5',
                     font=('OpenSans.ttf', 14)).grid(row=row_index, column=1, sticky='nsew', padx=5, pady=3)
            self.sciezki_entry_list.append(
                ctk.CTkEntry(self.ramka_sciezki, width=400, justify=tk.LEFT, text_font=('OpenSans.ttf', 13), fg_color='#303030', text_color="#c7c6c5"))
            self.sciezki_entry_list[index].grid(row=row_index, column=2, sticky='nsew', padx=5, pady=3)
            self.sciezki_entry_list[index].insert(0, path)
            self.sciezki_button_list.append(
                ctk.CTkButton(self.ramka_sciezki, text='Zmień ścieżkę', text_font=('OpenSans.ttf', 14),
                              fg_color='#505050', hover_color='#404040',
                              command=lambda x=self.sciezki_entry_list[index]: self.change_path(x), text_color="#c7c6c5"))
            self.sciezki_button_list[index].grid(row=row_index, column=3, sticky='nsew', padx=5, pady=3)
            self.sciezki_radio_list.append(ctk.CTkRadioButton(self.ramka_sciezki, value=index, variable=self.check_var,
                                                              text='', fg_color='#707070', border_width_checked=15,
                                                              width=30, height=30))
            self.sciezki_radio_list[index].grid(row=row_index, column=4, sticky='n', padx=5, pady=3)
        self.check_var.set(configFile.domyslne_leather_path)
        self.add_path_btn = ctk.CTkButton(self.ramka_sciezki, text='Dodaj ścieżkę', text_font=('OpenSans.ttf', 14),
                                          fg_color='#505050', hover_color='#404040',
                                          command=lambda: self.add_path(), text_color="#c7c6c5")
        self.add_path_btn.grid(row=row_index + 1, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)
        self.remove_path_btn = ctk.CTkButton(self.ramka_sciezki, text='Usuń ścieżkę', text_font=('OpenSans.ttf', 14),
                                             fg_color='#505050', hover_color='#404040',
                                             command=lambda: self.remove_path(), text_color="#c7c6c5")
        self.remove_path_btn.grid(row=row_index + 1, column=3, columnspan=2, sticky='nsew', padx=10, pady=10)

        self.ramka_sciezki.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

    def remove_path(self):
        self.temp_path_list = self.temp_path_list[:-1]
        self.ramka_sciezki.destroy()
        self.create_sciezki_frame()
    def add_path(self):
        self.temp_path_list.append('')
        self.ramka_sciezki.destroy()
        self.create_sciezki_frame()
    def change_path(self, object):
        new_path = filedialog.askdirectory(parent=self)
        if new_path != "":
            object.delete(0, 'end')
            object.insert(0, new_path)


    def change_obj_color(self, object):
        color = askcolor(parent=self, title='Wybierz kolor')
        object.configure(fg=color[1], bg=color[1])
    def rgb_to_hex (self, r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def hex_to_rgb (self, hex):
        rgb = ImageColor.getcolor(hex, "RGB")
        return rgb





