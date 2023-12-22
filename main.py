import tkinter as tk
from tkinter import ttk
import subprocess
from multiprocessing import Process, Queue
from bin.toolbar import Toolbar
from bin.infobar import Infobar
from bin.preview_5_sprites import Leatherpreview
#from bin.preview_4_wo_history import Leatherpreview
from bin.layerInfo import Layerinfo
from bin.projector import Leathermain
from bin.leather_toolbar import leather_tools

class MainApplication(tk.Frame):
    def __init__(self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.leather_tools = leather_tools(self, queue)
        self.leather_tools.grid(column=1, row=4, sticky='nsew')

        self.toolbar = Toolbar(self, queue)
        self.toolbar.grid(column=1, row=1, columnspan=2, sticky='nsew')

        self.infobar = Infobar(self)
        self.infobar.grid(column=1, row=2, columnspan=2, sticky='nsew')

        self.leather_preview = Leatherpreview(self, queue)
        self.leather_preview.grid(column=1, row=3, sticky='nsew')

        self.layer_info = Layerinfo(self)
        self.layer_info.grid(column=2, row=3, rowspan=2, sticky='nsew')

        style = ttk.Style()
        # style.layout("TNotebook", [])
        # style.configure("TNotebook", highlightbackground="#505050", tabmargins=0)

        # '#c7c6c5'
        style.theme_create("RCS", parent="alt", settings={
            ".":
                {"configure": {
                    "focuscolor": 'background',
                    'relief': 'flat',
                    'borderwidth': 0,
                }
                },
            "TNotebook":
                {"configure":
                     {"background": '#404040', "tabmargins": [1, 1, 1, 0]}},
            "TNotebook.Tab":
                {"configure":
                     {"padding": [110, 0], "background": "#404040", "foreground": "#c7c6c5",
                      "font": ('OpenSans.ttf', '20')},
                 "map":
                     {"background": [("selected", "#505050")], "expand": [("selected", [1, 1, 1, 1])]}},
            "Treeview.Heading":
                {"configure":
                     {"background": '#404040',
                      "font": ('OpenSans.ttf', '14'),
                      "foreground": "#c7c6c5"}},
            "Treeview":
                {"configure":
                     {"background": '#505050',
                      'rowheight': 23,
                      "font": ('OpenSans.ttf', '13'),
                      "foreground": "#c7c6c5"}},
            "Vertical.TScrollbar":
                {"configure":
                     {'background': "#202020",
                      'troughcolor': "#606060",
                      'width': 40}},
            "TFrame":
                {"configure":
                     {'background': "#303030"
                      }}})

        style.theme_use("RCS")
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.map('Treeview', background=[('selected', '#808080')])

        style.element_create("Vertical.TScrollbar.trough", "from", "clam")
        # style.element_create("Vertical.TScrollbar.thumb", "from", "clam")
        style.element_create("Vertical.TScrollbar.grip", "from", "clam")

        style.layout("Vertical.TScrollbar",
                     [('Vertical.TScrollbar.trough',
                       {'children': [('Vertical.TScrollbar.thumb',
                                      {'unit': '1', 'expand': '1',
                                       'children':
                                           [('Vertical.TScrollbar.grip', {'sticky': 'nswe'})],
                                       'sticky': 'ns'})], 'sticky': 'ns'})])


if __name__ == '__main__':
    queue = Queue()
    leather_view = Process(target=Leathermain, args=(queue,))
    leather_view.start()
    main_root = tk.Tk()
    main_root.iconbitmap("images/icon.ico")
    main_root.title("LeatherFlaws")
    main_root.resizable(True, True)
    main_root.state("zoomed")
    MainApplication(main_root, queue, width=1920, height=1080).pack(side="top", fill="both", expand=True)
    main_root.mainloop()
    subprocess.call('taskkill /F /T /PID ' + str(leather_view.pid))





