import tkinter as tk
import customtkinter as ctk

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
			leather_name_to_disp = leather_name.split("/")
			leather_name_to_disp = leather_name_to_disp[-1]
			tk.Label(self, text='Czy na pewno chcesz zapisać plik\n%s ?'%leather_name_to_disp, bg='#505050', fg='#c7c6c5', font=('OpenSans.ttf', 17)).grid(row=2, column=1,
																									   columnspan=4,
																									   sticky='nsew')
			self.save_btn = ctk.CTkButton(self, text='Zapisz', fg_color='#303030', hover_color='#404040',
										  text_font=('OpenSans.ttf', 20), command=lambda:self.parent.toolbar.save_leather_data())
			self.save_btn.grid(row=3, column=2, sticky='nsew', padx=10, pady=10)
			self.anuluj_btn = ctk.CTkButton(self, text='Anuluj', fg_color='#303030', hover_color='#404040',
											text_font=('OpenSans.ttf', 20), command=lambda: self.anuluj_btn_func())
			self.anuluj_btn.grid(row=3, column=3, sticky='nsew', padx=10, pady=10)
		elif leather_name == None:
			tk.Label(self, text='Brak wczytanego pliku skóry!\n\n\n Wczytaj plik skóry za pomocą opcji "Wybierz plik" znajdującej się\n na górnym pasku i dokonaj w nim zmian aby móc skorzystać\nz funkcji "Zapisz plik".',
					 bg='#505050', fg='#c7c6c5', font=('OpenSans.ttf', 17)).grid(row=2, column=1,
													 columnspan=4,
													 sticky='nsew')
			self.ok_btn = ctk.CTkButton(self, text='OK', fg_color='#303030', hover_color='#404040',
											text_font=('OpenSans.ttf', 20), command=lambda: self.anuluj_btn_func())
			self.ok_btn.grid(row=3, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)

	def anuluj_btn_func (self):
		self.destroy()

class infoBox(tk.Toplevel):
	def __init__ (self, parent, queue, leather_name, *args, **kwargs):
		tk.Toplevel.__init__(self, parent, *args, **kwargs)

		self.parent = parent
		self.queue = queue

		self.geometry('%dx%d%+d+%d' % (800, 450, 560, 315))
		self.attributes('-topmost', 'true')
		self.resizable(False, False)
		self.overrideredirect(True)
		self.configure(bg='#505050')
		self.columnconfigure((1, 2, 3, 4), weight=1)
		self.rowconfigure((2,3), weight=1)

		tk.Label(self, text='Zapis pliku', bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1, column=1,
																									   columnspan=4,
																									   sticky='nsew')

		leather_name_to_disp = leather_name.split("/")
		leather_name_to_disp = leather_name_to_disp[-1]
		tk.Label(self, text='Plik %s został zapisany w lokalizacji' % leather_name_to_disp, bg='#505050',
				 fg='#c7c6c5', font=('OpenSans.ttf', 17)).grid(row=2, column=1,
															   columnspan=4,
															   sticky='s')
		tk.Label(self, text='%s' % leather_name, bg='#505050',
				 fg='#c7c6c5', font=('OpenSans.ttf', 13)).grid(row=3, column=1,
															   columnspan=4,
															   sticky='n')
		self.ok_btn = ctk.CTkButton(self, text='OK', fg_color='#303030', hover_color='#404040',
										text_font=('OpenSans.ttf', 20), command=lambda: self.anuluj_btn_func())
		self.ok_btn.grid(row=4, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)



	def anuluj_btn_func (self):
		self.destroy()

class Error(tk.Toplevel):
	def __init__ (self, parent, queue, message1, message2=None, header = 'Błąd!', *args, **kwargs):
		tk.Toplevel.__init__(self, parent, *args, **kwargs)

		self.parent = parent
		self.queue = queue

		self.geometry('%dx%d%+d+%d' % (600, 300, 660, 390))
		self.attributes('-topmost', 'true')
		self.resizable(False, False)
		self.overrideredirect(True)
		self.configure(bg='#505050')
		self.columnconfigure((1, 2, 3, 4), weight=1)
		self.rowconfigure((2,3), weight=1)

		tk.Label(self, text=header, bg='#303030', fg='#c7c6c5', font=('OpenSans.ttf', 14)).grid(row=1, column=1,
																									   columnspan=4,
																									   sticky='nsew')

		tk.Label(self, text=message1, bg='#505050',
				 fg='#c7c6c5', font=('OpenSans.ttf', 15)).grid(row=2, column=1,
															   columnspan=4,
															   sticky='s')
		if message2 != None:
			tk.Label(self, text=message2, bg='#505050',
				 	fg='#c7c6c5', font=('OpenSans.ttf', 15)).grid(row=3, column=1, columnspan=4, sticky='n')
		self.ok_btn = ctk.CTkButton(self, text='OK', fg_color='#303030', hover_color='#404040',
										text_font=('OpenSans.ttf', 20), command=lambda: self.anuluj_btn_func())
		self.ok_btn.grid(row=4, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)



	def anuluj_btn_func (self):
		self.destroy()