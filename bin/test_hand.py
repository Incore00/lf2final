
import tkinter as tk

root = tk.Tk()

variable = tk.IntVar(root)

for onvalue in range(1, 5):
    print('onvalue', onvalue)
    checkbutton = tk.Checkbutton(root,onvalue=onvalue,variable=variable,
    )
    checkbutton.pack()

root.mainloop()