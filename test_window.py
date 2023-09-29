from tkinter import *

def create_win():
    def close(): win1.destroy();win2.destroy()
    win1 = Toplevel()
    print("win1")
    print('%dx%d%+d+%d'%(sw,sh,0,-sh))
    win1.geometry('%dx%d%+d+%d'%(sw,sh,0,-sh))
    win1.overrideredirect(True)
    Button(win1,text="Exit1",command=close).pack()

root=Tk()
sw,sh = root.winfo_screenwidth(),root.winfo_screenheight()
print("screen1:",sw,sh)
w,h = 800,600
a,b = (sw-w)/2,(sh-h)/2

Button(root,text="Exit",command=lambda r=root:r.destroy()).pack()
Button(root,text="Create win",command=create_win).pack()

root.geometry('%sx%s+%s+%s'%(w,h,int(a),int(b)))
root.mainloop()