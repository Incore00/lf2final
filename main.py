import tkinter as tk
from toolbar3 import Toolbar

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.toolbar = Toolbar(self)
        self.toolbar.pack()

        self.configure(bg='#303030')
        self.pack_propagate(0)
        self.grid_propagate(0)

if __name__ == '__main__':
    root = tk.Tk()
    root.iconbitmap("images/icon.ico")
    root.title("LeatherFlaws")
    root.resizable(True, True)
    root.state("zoomed")
    MainApplication(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight()).pack(side="top", fill="both", expand=True)
    root.mainloop()



