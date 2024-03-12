import tkinter as tk

class messBox(tk.Toplevel):
	def __init__ (self, parent, queue, leather_name, *args, **kwargs):
		tk.Toplevel.__init__(self, parent, *args, **kwargs)

		self.parent = parent
		self.queue = queue

		self.geometry('%dx%d%+d+%d' % (800, 450, 560, 315))
		self.attributes('-topmost', 'true')
		self.resizable(False, False)
		self.overrideredirect(True)
		self.configure(bg='#505050')
		self.columnconfigure((1,2,3,4), weight=1)
		self.rowconfigure(2, weight=1)

		tk.Label(self, text='Zapis pliku',bg='#303030', fg='#c7c6c5',font=('OpenSans.ttf', 14)).grid(row=1, column=1, columnspan=4, sticky='nsew')
		if leather_name != None:
			tk.Label(self, text='Czy na pewno chcesz zapisać skórę\n%s'%leather_name, bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 17)).grid(row=2, column=1,
																									   columnspan=4,
																									   sticky='nsew')
		elif leather_name == None:
			tk.Label(self, text='Brak wczytanego pliku skóry!\n\n\n Wczytaj plik skóry za pomocą opcji "Wybierz plik" znajdującej się\n na górnym pasku i dokonaj w nim zmian aby móc skorzystać\nz funkcji "Zapisz plik".',
					 bg='#505050', fg='#c7c6c5', font=('OpenSans.ttf', 17)).grid(row=2, column=1,
													 columnspan=4,
													 sticky='nsew')

		#ctk.CTkButton(