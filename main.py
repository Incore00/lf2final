import tkinter as tk
import subprocess
from multiprocessing import Process, Queue
from bin.toolbar import Toolbar
from bin.infobar import Infobar
from bin.preview import Leatherpreview
from bin.layerInfo import Layerinfo
from bin.projector import Leathermain

class MainApplication(tk.Frame):
    def __init__(self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.toolbar = Toolbar(self, queue)
        self.toolbar.grid(column=1, row=1, columnspan=2, sticky='nsew')

        self.infobar = Infobar(self)
        self.infobar.grid(column=1, row=2, columnspan=2, sticky='nsew')

        self.leather_preview = Leatherpreview(self, queue)
        self.leather_preview.grid(column=1, row=3, sticky='nsew')

        self.layer_info = Layerinfo(self)
        self.layer_info.grid(column=2, row=3, sticky='nsew')


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





