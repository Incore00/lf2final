import tkinter as tk
import tkinter.ttk as ttk
import pyglet
import customtkinter as ctk
from tkfontawesome import icon_to_image
from bin import configFile

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')

class Layerinfo(tk.Frame):
    def __init__ (self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.queue = queue
        self.parent = parent
        self.pack_propagate(0)
        self.grid_propagate(0)
        self.columnconfigure((1, 2, 3, 4), weight=1)
        self.rowconfigure(6, weight=1)

        self.configure(background='#303030', width=int(parent.winfo_reqwidth()*0.235), height=int(parent.winfo_reqheight()*0.865))

        tk.Label(self, text='Wybrane skazy:', fg='#c7c6c5', font=('OpenSans.ttf', 15), text_color='#c7c6c5', bg='#303030').grid(column=1, columnspan=4, row=1)
        self.clicked_flaws_frame = tk.Frame(self, background='#303030', height = 215)
        self.clicked_flaws_frame.grid_propagate(0)
        self.clicked_flaws_frame.grid(column=1, columnspan=4, row=2, sticky='nsew')
        tk.Label(self, text='Widoczność warstw:', fg='#c7c6c5', font=('OpenSans.ttf', 15), text_color='#c7c6c5', bg='#303030').grid(column=1, columnspan=4, row=3)

        self.blue_layer_icon_active = icon_to_image("layer-group", fill='#0000FF', scale_to_width=40)
        self.blue_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=40)
        self.blue_layer_btn = ctk.CTkButton(self, image=self.blue_layer_icon_active, fg_color='#505050',
                                            hover_color='#404040', compound='top', corner_radius=10, text='Niebieska',
                                            text_font=('OpenSans.ttf', 15), text_color='#c7c6c5', command=lambda: self.change_layer_visibility('blue'))
        self.blue_layer_btn.grid(column=1, row=4, sticky='nsew')

        self.green_layer_icon_active = icon_to_image("layer-group", fill='#00FF00', scale_to_width=40)
        self.green_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=40)
        self.green_layer_btn = ctk.CTkButton(self, image=self.green_layer_icon_active, fg_color='#505050',
                                             hover_color='#404040', compound='top', corner_radius=10, text='Zielona',
                                             text_font=('OpenSans.ttf', 15), text_color='#c7c6c5', command=lambda: self.change_layer_visibility('green'))
        self.green_layer_btn.grid(column=2, row=4, sticky='nsew')

        self.yellow_layer_icon_active = icon_to_image("layer-group", fill='#FFFF00', scale_to_width=40)
        self.yellow_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=40)
        self.yellow_layer_btn = ctk.CTkButton(self, image=self.yellow_layer_icon_active,
                                              fg_color='#505050',
                                              hover_color='#404040', compound='top', corner_radius=10, text='Zółta',
                                              text_font=('OpenSans.ttf', 15), text_color='#c7c6c5', command=lambda: self.change_layer_visibility('yellow'))
        self.yellow_layer_btn.grid(column=3, row=4, sticky='nsew')

        self.red_layer_icon_active = icon_to_image("layer-group", fill='#FF0000', scale_to_width=40)
        self.red_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=40)
        self.red_layer_btn = ctk.CTkButton(self, image=self.red_layer_icon_active, fg_color='#505050',
                                           hover_color='#404040', compound='top', corner_radius=10, text='Czerwona',
                                           text_font=('OpenSans.ttf', 15), text_color='#c7c6c5', command=lambda: self.change_layer_visibility('red'))
        self.red_layer_btn.grid(column=4, row=4, sticky='nsew')

        ctk.CTkLabel(self, text="Warstwa:", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=1, columnspan=2, row=5, sticky='nsew')
        ctk.CTkLabel(self, text="Liczba skaz:", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=3, columnspan=2, row=5, sticky='w')

        self.layer_frame = VerticalScrolledFrame(self)
        self.layer_frame.columnconfigure((1, 2, 3, 4, 5), weight=1)
        self.layer_frame.rowconfigure(1, weight=1)
        self.layer_frame.grid(column=1, columnspan=4, row=6, sticky='nsew')

        self.rarrow = icon_to_image("caret-right", fill="#adaba5", scale_to_width=10)
        self.darrow = icon_to_image("caret-down", fill="#adaba5", scale_to_width=15)

        self.hole_flaws = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
                                        corner_radius=10, border_width=3, border_color='#000000')
        ctk.CTkLabel(self.hole_flaws, text="Dziury", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=2, row=1,sticky='nsew', padx=35, pady=10)
        self.hole_layer_items_amount = ctk.CTkLabel(self.hole_flaws, text="0", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5')
        self.hole_layer_items_amount.grid(column=3, row=1,sticky='nsew', padx=10, pady=10)
        self.hole_flaws.grid(column=1, row=1, sticky='nsew')

        ### TEST ###

        #self.hole_flaw = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
        #                               corner_radius=5, border_width=1, border_color='#000000')
        #self.hole_flaw.grid(column=1, row=2, sticky='nsew')

        ### TEST ###

        self.blue_flaws = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
                                        corner_radius=10, border_width=3, border_color='#000000')
        ctk.CTkLabel(self.blue_flaws, text="Niebieska", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=1, row=1,
                                                                                           sticky='nsew', padx=35,
                                                                                           pady=10)
        self.blue_layer_items_amount = ctk.CTkLabel(self.blue_flaws, text="0", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5')
        self.blue_layer_items_amount.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)
        self.blue_flaws.grid(column=1, row=3, sticky='nsew')

        self.green_flaws = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
                                       corner_radius=10, border_width=3, border_color='#000000')
        ctk.CTkLabel(self.green_flaws, text="Zielona", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=1, row=1,
                                                                                             sticky='nsew', padx=35,
                                                                                             pady=10)
        self.green_layer_items_amount = ctk.CTkLabel(self.green_flaws, text="0", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5')
        self.green_layer_items_amount.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)
        self.green_flaws.grid(column=1, row=5, sticky='nsew')

        self.yellow_flaws = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
                                        corner_radius=10, border_width=3, border_color='#000000')
        ctk.CTkLabel(self.yellow_flaws, text="Żółta", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=1, row=1, sticky='nsew', padx=35, pady=10)
        self.yellow_layer_items_amount = ctk.CTkLabel(self.yellow_flaws, text="0", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5')
        self.yellow_layer_items_amount.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)
        self.yellow_flaws.grid(column=1, row=7, sticky='nsew')

        self.red_flaws = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
                                         corner_radius=10, border_width=3, border_color='#000000')
        ctk.CTkLabel(self.red_flaws, text="Czerwona", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5').grid(column=1, row=1,
                                                                                               sticky='nsew', padx=35,
                                                                                               pady=10)
        self.red_layer_items_amount = ctk.CTkLabel(self.red_flaws, text="0", text_font=('OpenSans.ttf', 16), text_color='#c7c6c5')
        self.red_layer_items_amount.grid(column=2, row=1, sticky='nsew', padx=10, pady=10)
        self.red_flaws.grid(column=1, row=9, sticky='nsew')

        for widget in self.winfo_children():
            widget.grid(padx=2, pady=2)

        for widget in self.layer_frame.interior.winfo_children():
            widget.grid(padx=2, pady=2)

    def rgb_to_hex (self,r, g, b):
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)

    def clicked_flaws_update(self, flaw_id_list, flaw_list, flaw_type_list, flaw_position_list):
        if flaw_list == None or str(flaw_list) == '[]':
            for child in self.clicked_flaws_frame.winfo_children():
                child.destroy()
            self.flaw_frame_list = []
        else:
            for index, flaw_id, flaw, flaw_type, flaw_position in zip(range(0, len(flaw_list)), flaw_id_list, flaw_list, flaw_type_list, flaw_position_list):
                flaw_frame = ctk.CTkFrame(self.clicked_flaws_frame, bg_color='#303030', fg_color='#303030',
                             corner_radius=5, border_width=2, border_color='#000000')
                flaw_frame.grid(column=0, row=index, sticky='nse', pady=1, padx=1)
                ctk.CTkLabel(flaw_frame, text="Skaza #%d" %flaw_id, text_font=('OpenSans.ttf', 13), text_color='#c7c6c5').grid(column=0, row=0, sticky='nsew', padx=1, pady=3)
                if flaw_type == 'hole':
                    ctk.CTkLabel(flaw_frame, text="DZIURA", text_color=self.rgb_to_hex(*configFile.h_layer_color),
                                 text_font=('OpenSans.ttf', 13)).grid(column=1,row=0, pady=3, sticky='nsew')
                elif flaw_type == 'blue':
                    ctk.CTkLabel(flaw_frame, text="NIEBIESKA", text_color=self.rgb_to_hex(*configFile.b_layer_color),
                                 text_font=('OpenSans.ttf', 13)).grid(column=1, row=0, pady=3, sticky='nsew')
                elif flaw_type == 'green':
                    ctk.CTkLabel(flaw_frame, text="ZIELONA", text_color=self.rgb_to_hex(*configFile.g_layer_color),
                                 text_font=('OpenSans.ttf', 13)).grid(column=1, row=0, pady=3, sticky='nsew')
                elif flaw_type == 'yellow':
                    ctk.CTkLabel(flaw_frame, text="ŻÓŁTA", text_color=self.rgb_to_hex(*configFile.y_layer_color),
                                 text_font=('OpenSans.ttf', 13)).grid(column=1, row=0, pady=3, sticky='nsew')
                elif flaw_type == 'red':
                    ctk.CTkLabel(flaw_frame, text="CZERWONA", text_color=self.rgb_to_hex(*configFile.r_layer_color),
                                 text_font=('OpenSans.ttf', 13)).grid(column=1, row=0, pady=3, sticky='nsew')

                ctk.CTkLabel(flaw_frame, text="x:%d, y:%d" % (int(flaw_position[0]), int(flaw_position[1])),
                             text_font=('OpenSans.ttf', 13), text_color='#c7c6c5').grid(column=2, row=0, pady=3, sticky='nsew')

                exit_icon = icon_to_image("times", fill='#c7c6c5', scale_to_width=20)
                exit_btn = ctk.CTkButton(flaw_frame, image=exit_icon, width=1, height=1, bg_color='#303030',
                                         fg_color='#303030', hover_color='#303030',
                                         command=lambda x=flaw_frame, y=flaw, z=flaw_list:self.exit_btn_handler(x, y, z), text='')
                exit_btn.grid(column=3, row=0, pady=3, sticky='nsew')

    def exit_btn_handler(self, flaw_frame, flaw, flaw_list):
        flaw_frame.destroy()
        flaw_list.remove(flaw)
        new_list = []
        for item in flaw_list:
            try:
                new_list.append(*item)
            except TypeError:
                new_list.append(item[0])
                new_list.append(item[1])
        print(new_list)
        flaw_dict = self.convert_list_to_dict(new_list)
        self.parent.leather_preview.lw_prev.clicked_flaw_editor(flaw_dict)

    def convert_list_to_dict(self, list):
        it = iter(list)
        res_dct = dict(zip(it, it))
        return res_dct

    def change_layer_visibility(self, layer):
        if layer == 'blue':
            if configFile.b_layer_flag == True:
                configFile.b_layer_flag = False
                self.blue_layer_btn.configure(image=self.blue_layer_icon_inactive)
            else:
                configFile.b_layer_flag = True
                self.blue_layer_btn.configure(image=self.blue_layer_icon_active)
        elif layer == 'green':
            if configFile.g_layer_flag == True:
                configFile.g_layer_flag = False
                self.green_layer_btn.configure(image=self.green_layer_icon_inactive)
            else:
                configFile.g_layer_flag = True
                self.green_layer_btn.configure(image=self.green_layer_icon_active)
        elif layer == 'yellow':
            if configFile.y_layer_flag == True:
                configFile.y_layer_flag = False
                self.yellow_layer_btn.configure(image=self.yellow_layer_icon_inactive)
            else:
                configFile.y_layer_flag = True
                self.yellow_layer_btn.configure(image=self.yellow_layer_icon_active)
        elif layer == 'red':
            if configFile.r_layer_flag == True:
                configFile.r_layer_flag = False
                self.red_layer_btn.configure(image=self.red_layer_icon_inactive)
            else:
                configFile.r_layer_flag = True
                self.red_layer_btn.configure(image=self.red_layer_icon_active)
        layers_status = [configFile.b_layer_flag,
                        configFile.g_layer_flag,
                        configFile.y_layer_flag,
                        configFile.r_layer_flag]
        self.queue.put(['main_change_layer_visibility', layers_status])
    def load_data(self, hole_amount, blue_amount, green_amount, yellow_amount, red_amount):
        self.hole_layer_items_amount.configure(text=hole_amount)
        self.blue_layer_items_amount.configure(text=blue_amount)
        self.green_layer_items_amount.configure(text=green_amount)
        self.yellow_layer_items_amount.configure(text=yellow_amount)
        self.red_layer_items_amount.configure(text=red_amount)

        blue_flaws_list = []
        for i in range(blue_amount):
            current_frame = ctk.CTkFrame(self.layer_frame.interior, bg_color='#303030', fg_color='#303030',
                                       corner_radius=5, border_width=1, border_color='#000000')




class VerticalScrolledFrame(ttk.Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set, background='#303030')
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)
