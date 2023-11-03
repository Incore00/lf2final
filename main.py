import tkinter as tk
from toolbar4 import Toolbar, Infobar, Leatherpreview, Layerinfo

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.pack_propagate(0)
        self.grid_propagate(0)

        self.toolbar = Toolbar(self)
        self.toolbar.grid(column=1, row=1, columnspan=2, sticky='nsew')

        self.infobar = Infobar(self)
        self.infobar.grid(column=1, row=2, columnspan=2, sticky='nsew')

        self.leather_preview = Leatherpreview(self)
        self.leather_preview.grid(column=1, row=3, sticky='nsew')

        self.layer_info = Layerinfo(self)
        self.layer_info.grid(column=2, row=3, sticky='nsew')

        self.configure(bg='#303030')
        self.pack_propagate(0)
        self.grid_propagate(0)

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap("images/icon.ico")
    root.title("LeatherFlaws")
    root.resizable(True, True)
    root.state("zoomed")
    MainApplication(root, width=1920, height=1080).pack(side="top", fill="both", expand=True)
    root.mainloop()



