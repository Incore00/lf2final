import tkinter as tk

class Message(tk.Toplevel):
	def __init__(self, parent, message_text:str, *args, **kwargs):
		tk.Toplevel.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.configure(height=int(parent.winfo_screenheight() * 0.15), width=int(parent.winfo_screenwidth() * 0.4), bg='#303030')
