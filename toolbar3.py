import tkinter as tk
from datetime import datetime
import pyglet
import customtkinter as ctk
from tkfontawesome import icon_to_image
from PIL import ImageTk
from tkinter import filedialog
import ezdxf
from threading import Thread

from Leather import Leather
from LeatherWindow import LeatherWindow


base, texid = 0, 0
text = '''Hello World !'''

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')
fontfile = "VeraMono.ttf"


class Toolbar(tk.Frame):
	def __init__ (self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.configure(height=int(self.winfo_screenheight() * 0.1), width=self.winfo_screenwidth(), bg='#303030')
		self.pack_propagate(0)
		self.grid_propagate(0)

		toolbar_container = tk.Frame(self, height=self.winfo_screenheight() * 0.1, width=self.winfo_screenwidth(),
									 bg='#303030')
		toolbar_container.pack_propagate(0)
		toolbar_container.grid_propagate(0)
		toolbar_container.columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
		toolbar_container.rowconfigure(1, weight=1)

		anthr_window = tk.Toplevel(self)
		sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
		anthr_window.geometry('%dx%d%+d+%d'%(sw,sh,0,-sh))
		anthr_window.overrideredirect(True)

		self.content_container = LeatherWindow(anthr_window, self, height=int(self.winfo_screenheight() * 0.9),
											   width=int(self.winfo_screenwidth()))

		toolbar_container.pack(side='top', fill="both", expand=True)
		self.content_container.pack(side='top', fill="both", expand=True)

		self.load_file_icon = icon_to_image("folder-open", fill='#c7c6c5', scale_to_width=60)
		self.change_colors_icon_active = icon_to_image("sync-alt", fill='#c7c6c5', scale_to_width=60)
		self.blue_layer_icon_active = icon_to_image("layer-group", fill='#0000FF', scale_to_width=60)
		self.green_layer_icon_active = icon_to_image("layer-group", fill='#00FF00', scale_to_width=60)
		self.yellow_layer_icon_active = icon_to_image("layer-group", fill='#FFFF00', scale_to_width=60)
		self.red_layer_icon_active = icon_to_image("layer-group", fill='#FF0000', scale_to_width=60)
		self.blue_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=60)
		self.green_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=60)
		self.yellow_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=60)
		self.red_layer_icon_inactive = icon_to_image("layer-group", fill='#c7c6c5', scale_to_width=60)
		self.change_colors_icon_inactive = icon_to_image("sync-alt", fill='#FFFFFF', scale_to_width=60)

		self.blue_layer_flag = True
		self.green_layer_flag = True
		self.yellow_layer_flag = True
		self.red_layer_flag = True

		self.active_file = None
		self.change_colors_flag = None

		self.data = None

		self.clock = tk.StringVar()

		logo = ImageTk.PhotoImage(file='images/logo.png')

		logo_label = tk.Label(toolbar_container, image=logo, bg='#404040')
		logo_label.photo = logo
		logo_label.grid(column=1, row=1, sticky='nsew', ipadx=5)

		tk.Label(toolbar_container, text='Leather\nFlaws', bg='#404040', fg='#c7c6c5',
				 font=('OpenSans.ttf', 30)).grid(column=2, row=1, sticky='nsew', ipadx=5)

		self.load_file_btn = ctk.CTkButton(toolbar_container, image=self.load_file_icon, fg_color='#505050',
										   hover_color='#404040', command=lambda: self.load_leather()
										   , compound='top', corner_radius=10, text='Załaduj plik',
										   text_font=('OpenSans.ttf', 18))
		self.load_file_btn.grid(column=3, row=1, sticky='nsew')

		self.change_colors_btn = ctk.CTkButton(toolbar_container, image=self.change_colors_icon_active,
											   fg_color='#505050',
											   hover_color='#404040', command=self.change_colors
											   , compound='top', corner_radius=10, text='Zmień kolory',
											   text_font=('OpenSans.ttf', 18))
		self.change_colors_btn.grid(column=4, row=1, sticky='nsew')

		tk.Label(toolbar_container, textvariable=self.clock, bg='#404040', fg='#c7c6c5',
				 font=('OpenSans.ttf', 19)).grid(column=5, row=1, sticky='nsew', ipadx=5)

		self.blue_layer_btn = ctk.CTkButton(toolbar_container, image=self.blue_layer_icon_active, fg_color='#505050',
											hover_color='#404040', command=self.blue_layer_btnfunc
											, compound='top', corner_radius=10, text='Niebieska',
											text_font=('OpenSans.ttf', 18))
		self.blue_layer_btn.grid(column=6, row=1, sticky='nsew')

		self.green_layer_btn = ctk.CTkButton(toolbar_container, image=self.green_layer_icon_active, fg_color='#505050',
											 hover_color='#404040', command=self.green_layer_btnfunc
											 , compound='top', corner_radius=10, text='Zielona',
											 text_font=('OpenSans.ttf', 18))
		self.green_layer_btn.grid(column=7, row=1, sticky='nsew')

		self.yellow_layer_btn = ctk.CTkButton(toolbar_container, image=self.yellow_layer_icon_active,
											  fg_color='#505050',
											  hover_color='#404040', command=self.yellow_layer_btnfunc
											  , compound='top', corner_radius=10, text='Zółta',
											  text_font=('OpenSans.ttf', 18))
		self.yellow_layer_btn.grid(column=8, row=1, sticky='nsew')

		self.red_layer_btn = ctk.CTkButton(toolbar_container, image=self.red_layer_icon_active, fg_color='#505050',
										   hover_color='#404040', command=self.red_layer_btnfunc
										   , compound='top', corner_radius=10, text='Czerwona',
										   text_font=('OpenSans.ttf', 18))
		self.red_layer_btn.grid(column=9, row=1, sticky='nsew')

		Thread(target=self.clockLoop()).start()

		# with open('config.txt', 'r') as config:
		#	com_port = config.readlines()
		# print("com port:", *com_port)
		# try:
		#	self.barcode_scanner = serial.Serial(str(*com_port), 19200, timeout=1)
		#	Thread(target=self.read_barcode()).start()
		# except:
		#	pass

		for widget in toolbar_container.winfo_children():
			widget.grid(padx=2, pady=2)

		self.code = ''
		self.leather_name = ''
		self.code_flag = False

		self.parent.parent.bind('<Key>', self.get_key)

	def get_key (self, event):
		if self.code_flag == False:
			self.code += str(event.char)
		else:
			self.code_flag = False
			self.code = ''
		if len(self.code) >= 24 and event.keysym == 'Return':
			self.leather_name = self.code[-25:]
			self.load_scanned_leather(self.leather_name)
			self.code = ''
			self.code_flag = True

	def clockLoop (self):
		clock = datetime.now().strftime('%Y-%m-%d\n%H:%M:%S') + '\nTydzień ' + str(
			datetime.isocalendar(datetime.now())[1])
		self.clock.set(clock)
		self.after(1000, self.clockLoop)

	def load_scanned_leather (self, leather_name):
		data = leather_name[:-1]
		path_list = ["g:\hdsk" + "\\" + data + ".DXF",
					 "g:\hd" + "\\" + data + ".DXF",
					 "l:\hdsk" + "\\" + data + ".DXF",
					 "l:\hd" + "\\" + data + ".DXF"]
		for path in path_list:
			try:
				self.load_leather(path, self.change_colors_flag)
			except:
				print("Cant load file in: " + path)
				pass

	def change_colors (self):
		if self.change_colors_flag == None:
			self.change_colors_flag = "NotNone"
			if self.active_file == None:
				self.content_container.change_colors_func((255, 255, 255), (0, 0, 0), (127, 127, 127), (0, 0, 255),
														  "polygon", (0, 255, 0), "polygon", (255, 255, 0), "polygon",
														  (255, 0, 0), "polygon")
			else:
				self.content_container.change_colors_func((255, 255, 255), (0, 0, 0), (127, 127, 127), (0, 0, 255),
														  "polygon", (0, 255, 0), "polygon", (255, 255, 0), "polygon",
														  (255, 0, 0), "polygon")
			self.change_colors_btn.configure(image=self.change_colors_icon_inactive)
		else:
			self.change_colors_flag = None
			if self.active_file == None:
				self.content_container.change_colors_func((0, 0, 0), (255, 255, 255), (127, 127, 127), (0, 0, 255),
														  "lines", (0, 255, 0), "lines", (255, 255, 0), "lines",
														  (255, 0, 0), "lines")
			else:
				self.content_container.change_colors_func((0, 0, 0), (255, 255, 255), (127, 127, 127), (0, 0, 255),
														  "lines", (0, 255, 0), "lines", (255, 255, 0), "lines",
														  (255, 0, 0), "lines")
			self.change_colors_btn.configure(image=self.change_colors_icon_active)

	def blue_layer_btnfunc (self):
		if self.blue_layer_flag == True:
			self.blue_layer_flag = False
			#self.load_leather(self.active_file, self.change_colors_flag)
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag, self.yellow_layer_flag, self.red_layer_flag)
			self.blue_layer_btn.configure(image=self.blue_layer_icon_inactive)
		elif self.blue_layer_flag == False:
			self.blue_layer_flag = True
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.blue_layer_btn.configure(image=self.blue_layer_icon_active)

	def green_layer_btnfunc (self):
		if self.green_layer_flag == True:
			self.green_layer_flag = False
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.green_layer_btn.configure(image=self.green_layer_icon_inactive)
		elif self.green_layer_flag == False:
			self.green_layer_flag = True
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.green_layer_btn.configure(image=self.green_layer_icon_active)

	def yellow_layer_btnfunc (self):
		if self.yellow_layer_flag == True:
			self.yellow_layer_flag = False
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.yellow_layer_btn.configure(image=self.yellow_layer_icon_inactive)
		elif self.yellow_layer_flag == False:
			self.yellow_layer_flag = True
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.yellow_layer_btn.configure(image=self.yellow_layer_icon_active)

	def red_layer_btnfunc (self):
		if self.red_layer_flag == True:
			self.red_layer_flag = False
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.red_layer_btn.configure(image=self.red_layer_icon_inactive)
		elif self.red_layer_flag == False:
			self.red_layer_flag = True
			self.content_container.change_layers_visiblity(True, self.blue_layer_flag, self.green_layer_flag,
														   self.yellow_layer_flag, self.red_layer_flag)
			self.red_layer_btn.configure(image=self.red_layer_icon_active)

	def load_leather (self, file=None, color_mode=None):
		if file == None:
			file = filedialog.askopenfile()
			print(file)
			color_mode = self.change_colors_flag

		if color_mode != None:
			bg_layer_color = (255, 255, 255)
			c_layer_color = (0, 0, 0)
			h_layer_color = (127, 127, 127)
			b_layer_color = (0, 0, 255)
			b_layer_linetype = "polygon"
			g_layer_color = (0, 255, 0)
			g_layer_linetype = "polygon"
			y_layer_color = (255, 255, 0)
			y_layer_linetype = "polygon"
			r_layer_color = (255, 0, 0)
			r_layer_linetype = "polygon"
		else:
			bg_layer_color = (0, 0, 0)
			c_layer_color = (255, 255, 255)
			h_layer_color = (127, 127, 127)
			b_layer_color = (0, 0, 255)
			b_layer_linetype = "lines"
			g_layer_color = (0, 255, 0)
			g_layer_linetype = "lines"
			y_layer_color = (255, 255, 0)
			y_layer_linetype = "lines"
			r_layer_color = (255, 0, 0)
			r_layer_linetype = "lines"

		b_layer = []
		b_layer_points = []
		g_layer = []
		g_layer_points = []
		y_layer = []
		y_layer_points = []
		r_layer = []
		r_layer_points = []
		h_layer = []
		h_layer_points = []
		c_layer = []
		c_layer_points = []
		if file != 'NotNone':
			try:
				leather = ezdxf.readfile(file.name)
				self.active_file = file.name
			except:
				leather = ezdxf.readfile(file)
				self.active_file = file
			msp = leather.modelspace()
			for item in msp:
				if 'POLYLINE' in str(item):
					if str(item.dxf.get('layer')) == '51':
						b_layer.append(item)
					elif str(item.dxf.get('layer')) == '52':
						g_layer.append(item)
					elif str(item.dxf.get('layer')) == '53':
						y_layer.append(item)
					elif str(item.dxf.get('layer')) == '54':
						r_layer.append(item)
					elif str(item.dxf.get('layer')) == '11':
						h_layer.append(item)
					elif str(item.dxf.get('layer')) == '1':
						c_layer.append(item)

		# edited for PYGAME!!!!
		#try:
		for item in c_layer:
			for point in item.points():
				c_layer_points.append((point[0], point[1]))
		#except:
		#	raise Exception("Błąd podczas odczytu punktów warstwy konturu")

		try:
			for item in b_layer:
				item_list = []
				for point in item.points():
					item_list.append((point[0], point[1]))
				b_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy niebieskiej")
		try:
			for item in g_layer:
				item_list = []
				for point in item.points():
					item_list.append((point[0], point[1]))
				g_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy zielonej")
		try:
			for item in y_layer:
				item_list = []
				for point in item.points():
					item_list.append((point[0], point[1]))
				y_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy żółtej")
		try:
			for item in r_layer:
				item_list = []
				for point in item.points():
					item_list.append((point[0], point[1]))
				r_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy czerwonej")
		try:
			for item in h_layer:
				item_list = []
				for point in item.points():
					item_list.append((point[0], point[1]))
				h_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy dziur")

		self.content_container.load_leather_data(Leather(c_layer_points, h_layer_points, b_layer_points, g_layer_points,
														 y_layer_points, r_layer_points), bg_layer_color, c_layer_color,
												 h_layer_color, b_layer_color, b_layer_linetype, g_layer_color,
												 g_layer_linetype, y_layer_color, y_layer_linetype, r_layer_color,
												 r_layer_linetype)








