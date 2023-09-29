import tkinter as tk
from datetime import datetime
import pyglet
import customtkinter as ctk
from tkfontawesome import icon_to_image
from PIL import ImageTk
from pyopengltk import OpenGLFrame
from OpenGL.GL import *
import pyautogui
from tkinter import filedialog
import ezdxf
from threading import Thread

base, texid = 0, 0
text  = '''Hello World !'''

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')
fontfile = "VeraMono.ttf"


class Toolbar(tk.Frame):
	def __init__ (self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		self.configure(height=self.winfo_screenheight(), width=self.winfo_screenwidth(), bg='#303030')
		self.pack_propagate(0)
		self.grid_propagate(0)


		toolbar_container = tk.Frame(self, height=self.winfo_screenheight() * 0.1, width=self.winfo_screenwidth(),
									 bg='#303030')
		toolbar_container.pack_propagate(0)
		toolbar_container.grid_propagate(0)
		toolbar_container.columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)
		toolbar_container.rowconfigure(1, weight=1)

		self.content_container = LeatherWindow(self, self, height=int(self.winfo_screenheight() * 0.9), width=int(self.winfo_screenwidth()))

		toolbar_container.pack(side='top', fill="both", expand=True)
		self.content_container.pack(side='bottom', fill="both", expand=True)

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
				 font=('OpenSans.ttf', 30)).grid(column=2,row=1,sticky='nsew',ipadx=5)

		self.load_file_btn = ctk.CTkButton(toolbar_container, image=self.load_file_icon, fg_color='#505050',
										   hover_color='#404040', command=lambda: self.load_leather()
										   , compound='top', corner_radius=10, text='Załaduj plik',
										   text_font=('OpenSans.ttf', 18))
		self.load_file_btn.grid(column=3, row=1, sticky='nsew')

		self.change_colors_btn = ctk.CTkButton(toolbar_container, image=self.change_colors_icon_active, fg_color='#505050',
											   hover_color='#404040', command = self.change_colors
											   , compound='top', corner_radius=10, text='Zmień kolory',
											   text_font=('OpenSans.ttf', 18))
		self.change_colors_btn.grid(column=4, row=1, sticky='nsew')

		tk.Label(toolbar_container, textvariable=self.clock, bg='#404040', fg='#c7c6c5',
				 font=('OpenSans.ttf', 19)).grid(column=5, row=1, sticky='nsew', ipadx=5)

		self.blue_layer_btn = ctk.CTkButton(toolbar_container, image=self.blue_layer_icon_active, fg_color='#505050',
											hover_color='#404040', command = self.blue_layer_btnfunc
											, compound='top', corner_radius=10, text='Niebieska',
											text_font=('OpenSans.ttf', 18))
		self.blue_layer_btn.grid(column=6, row=1, sticky='nsew')

		self.green_layer_btn = ctk.CTkButton(toolbar_container, image=self.green_layer_icon_active, fg_color='#505050',
											 hover_color='#404040', command = self.green_layer_btnfunc
											 , compound='top', corner_radius=10, text='Zielona',
											 text_font=('OpenSans.ttf', 18))
		self.green_layer_btn.grid(column=7, row=1, sticky='nsew')

		self.yellow_layer_btn = ctk.CTkButton(toolbar_container, image=self.yellow_layer_icon_active, fg_color='#505050',
											  hover_color='#404040', command = self.yellow_layer_btnfunc
											  , compound='top', corner_radius=10, text='Zółta',
											  text_font=('OpenSans.ttf', 18))
		self.yellow_layer_btn.grid(column=8, row=1, sticky='nsew')

		self.red_layer_btn = ctk.CTkButton(toolbar_container, image=self.red_layer_icon_active, fg_color='#505050',
										   hover_color='#404040', command = self.red_layer_btnfunc
										   , compound='top', corner_radius=10, text='Czerwona',
										   text_font=('OpenSans.ttf', 18))
		self.red_layer_btn.grid(column=9, row=1, sticky='nsew')

		Thread(target=self.clockLoop()).start()

		#with open('config.txt', 'r') as config:
		#	com_port = config.readlines()
		#print("com port:", *com_port)
		#try:
		#	self.barcode_scanner = serial.Serial(str(*com_port), 19200, timeout=1)
		#	Thread(target=self.read_barcode()).start()
		#except:
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

	def load_scanned_leather(self, leather_name):
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

	def change_colors(self):
		if self.change_colors_flag == None:
			self.change_colors_flag = "NotNone"
			if self.active_file == None:
				self.load_leather("NotNone", self.change_colors_flag)
			else:
				self.load_leather(self.active_file, self.change_colors_flag)
			self.change_colors_btn.configure(image=self.change_colors_icon_inactive)
		else:
			self.change_colors_flag = None
			if self.active_file == None:
				self.load_leather("NotNone", self.change_colors_flag)
			else:
				self.load_leather(self.active_file, self.change_colors_flag)
			self.change_colors_btn.configure(image=self.change_colors_icon_active)

	def blue_layer_btnfunc(self):
		if self.blue_layer_flag == True:
			self.blue_layer_flag = False
			self.load_leather(self.active_file, self.change_colors_flag)
			self.blue_layer_btn.configure(image=self.blue_layer_icon_inactive)
		elif self.blue_layer_flag == False:
			self.blue_layer_flag = True
			self.load_leather(self.active_file, self.change_colors_flag)
			self.blue_layer_btn.configure(image=self.blue_layer_icon_active)

	def green_layer_btnfunc(self):
		if self.green_layer_flag == True:
			self.green_layer_flag = False
			self.load_leather(self.active_file, self.change_colors_flag)
			self.green_layer_btn.configure(image=self.green_layer_icon_inactive)
		elif self.green_layer_flag == False:
			self.green_layer_flag = True
			self.load_leather(self.active_file, self.change_colors_flag)
			self.green_layer_btn.configure(image=self.green_layer_icon_active)

	def yellow_layer_btnfunc(self):
		if self.yellow_layer_flag == True:
			self.yellow_layer_flag = False
			self.load_leather(self.active_file, self.change_colors_flag)
			self.yellow_layer_btn.configure(image=self.yellow_layer_icon_inactive)
		elif self.yellow_layer_flag == False:
			self.yellow_layer_flag = True
			self.load_leather(self.active_file, self.change_colors_flag)
			self.yellow_layer_btn.configure(image=self.yellow_layer_icon_active)

	def red_layer_btnfunc(self):
		if self.red_layer_flag == True:
			self.red_layer_flag = False
			self.load_leather(self.active_file, self.change_colors_flag)
			self.red_layer_btn.configure(image=self.red_layer_icon_inactive)
		elif self.red_layer_flag == False:
			self.red_layer_flag = True
			self.load_leather(self.active_file, self.change_colors_flag)
			self.red_layer_btn.configure(image=self.red_layer_icon_active)

	def load_leather(self, file = None, color_mode = None):
		if file == None:
			file = filedialog.askopenfile()
			print(file)
			color_mode = self.change_colors_flag

		if color_mode != None:
			bg_layer_color = 1.0, 1.0, 1.0, 1.0
			c_layer_color = 0,0,0
			h_layer_color = 0.5,0.5,0.5
			b_layer_color = 0,0,1
			b_layer_linetype = GL_POLYGON
			g_layer_color = 0,1,0
			g_layer_linetype = GL_POLYGON
			y_layer_color = 1,1,0
			y_layer_linetype = GL_POLYGON
			r_layer_color = 1,0,0
			r_layer_linetype = GL_POLYGON
		else:
			bg_layer_color = 0.0, 0.0, 0.0, 0.0
			c_layer_color = 1,1,1
			h_layer_color = 0.5,0.5,0.5
			b_layer_color = 0,0,1
			b_layer_linetype = GL_LINE_LOOP
			g_layer_color = 0,1,0
			g_layer_linetype = GL_LINE_LOOP
			y_layer_color = 1,1,0
			y_layer_linetype = GL_LINE_LOOP
			r_layer_color = 1,0,0
			r_layer_linetype = GL_LINE_LOOP


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
		try:
			for item in c_layer:
				item_list = []
				for point in item.points():
					item_list.append([point[0], point[1]])
				c_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy konturu")
		try:
			for item in b_layer:
				item_list = []
				for point in item.points():
					item_list.append([point[0], point[1]])
				b_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy niebieskiej")
		try:
			for item in g_layer:
				item_list = []
				for point in item.points():
					item_list.append([point[0], point[1]])
				g_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy zielonej")
		try:
			for item in y_layer:
				item_list = []
				for point in item.points():
					item_list.append([point[0], point[1]])
				y_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy żółtej")
		try:
			for item in r_layer:
				item_list = []
				for point in item.points():
					item_list.append([point[0], point[1]])
				r_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy czerwonej")
		try:
			for item in h_layer:
				item_list = []
				for point in item.points():
					item_list.append([point[0], point[1]])
				h_layer_points.append(item_list)
		except:
			raise Exception("Błąd podczas odczytu punktów warstwy dziur")
		if self.red_layer_flag == False:
			r_layer_points = []
		if self.green_layer_flag == False:
			g_layer_points = []
		if self.yellow_layer_flag == False:
			y_layer_points = []
		if self.blue_layer_flag == False:
			b_layer_points = []
		self.content_container.load_data(b_layer_points, g_layer_points, y_layer_points, r_layer_points, h_layer_points, c_layer_points,
				  bg_layer_color, c_layer_color, h_layer_color, b_layer_color, b_layer_linetype, g_layer_color,
				  g_layer_linetype,y_layer_color, y_layer_linetype, r_layer_color, r_layer_linetype)


class LeatherWindow(OpenGLFrame):
	wheel_pos = 0
	last_mouse_x_pos = 0
	last_mouse_y_pos = 0
	b_layer_items = []
	g_layer_items = []
	y_layer_items = []
	r_layer_items = []
	h_layer_items = []
	c_layer_items = []
	prev_vertex_main = None
	init_flag = False

	bg_layer_color = (0.0, 0.0, 0.0, 0.0)
	c_layer_color = (1, 1, 1)
	h_layer_color = (0.5, 0.5, 0.5)
	b_layer_color = (0, 0, 1)
	b_layer_linetype = GL_LINE_LOOP
	g_layer_color = (0, 1, 0)
	g_layer_linetype = GL_LINE_LOOP
	y_layer_color = (1, 1, 0)
	y_layer_linetype = GL_LINE_LOOP
	r_layer_color = (1, 0, 0)
	r_layer_linetype = GL_LINE_LOOP

	def load_data(self, b_layer_points, g_layer_points, y_layer_points, r_layer_points, h_layer_points, c_layer_points,
				  bg_layer_color, c_layer_color, h_layer_color, b_layer_color, b_layer_linetype, g_layer_color,
				  g_layer_linetype,y_layer_color, y_layer_linetype, r_layer_color, r_layer_linetype):
		self.b_layer_items = b_layer_points
		self.g_layer_items = g_layer_points
		self.y_layer_items = y_layer_points
		self.r_layer_items = r_layer_points
		self.h_layer_items = h_layer_points
		self.c_layer_items = c_layer_points

		self.bg_layer_color = bg_layer_color
		self.c_layer_color = c_layer_color
		self.h_layer_color = h_layer_color
		self.b_layer_color = b_layer_color
		self.b_layer_linetype = b_layer_linetype
		self.g_layer_color = g_layer_color
		self.g_layer_linetype = g_layer_linetype
		self.y_layer_color = y_layer_color
		self.y_layer_linetype = y_layer_linetype
		self.r_layer_color = r_layer_color
		self.r_layer_linetype = r_layer_linetype

	def initgl(self):
		if self.init_flag == True:
			pass
		else:
			self.init_flag = True
			self.bind("<MouseWheel>", self.on_mouse_scroll)
			self.bind("<B1-Motion>", self.on_mouse_drag)
			self.bind("<Button-1>", self.on_mouse_click)
			self.bind("<Control-1>", self.on_ctrl_hold)
			glViewport(0, 0, self.width, self.height)
			glTranslatef(500, 1000, 0)
			glScaled(0.25, 0.25, 0.25)
			glRotatef(-90, 0, 0, 1)
			glClearColor(0.0, 0.0, 0.0, 0.0)
			self.animate = 1
			glMatrixMode(GL_PROJECTION)
			glLoadIdentity()
			glOrtho(0, self.width, self.height, 0, -1, 1)
			glMatrixMode(GL_MODELVIEW)
	def redraw(self):
		glClearColor(*self.bg_layer_color)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glLineWidth(2.0)
		glBegin(GL_LINE_LOOP)
		glColor3f(*self.c_layer_color)
		for item in self.c_layer_items:
			for point in item:
				glVertex2f(int(abs(point[0])), int(abs(point[1])))
		glEnd()
		glBegin(self.r_layer_linetype)
		glColor3f(*self.r_layer_color)
		for item in self.r_layer_items:
			for point, index in zip(item, range(0, len(item))):
				glVertex2f(int(abs(point[0])), int(abs(point[1])))
				if index == len(item)-1:
					glEnd()
					glBegin(self.r_layer_linetype)
					glColor3f(*self.r_layer_color)
		glEnd()

		glBegin(self.g_layer_linetype)
		glColor3f(*self.g_layer_color)
		for item in self.g_layer_items:
			for point, index in zip(item, range(0, len(item))):
				glVertex2f(int(abs(point[0])), int(abs(point[1])))
				if index == len(item) - 1:
					glEnd()
					glBegin(self.g_layer_linetype)
					glColor3f(*self.g_layer_color)
		glEnd()

		glBegin(self.b_layer_linetype)
		glColor3f(*self.b_layer_color)
		for item in self.b_layer_items:
			for point, index in zip(item, range(0, len(item))):
				glVertex2f(int(abs(point[0])), int(abs(point[1])))
				if index == len(item) - 1:
					glEnd()
					glBegin(self.b_layer_linetype)
					glColor3f(*self.b_layer_color)
		glEnd()

		glBegin(GL_LINE_LOOP)
		glColor3f(*self.h_layer_color)
		for item in self.h_layer_items:
			for point, index in zip(item, range(0, len(item))):
				glVertex2f(int(abs(point[0])), int(abs(point[1])))
				if index == len(item) - 1:
					glEnd()
					glBegin(GL_LINE_LOOP)
					glColor3f(*self.h_layer_color)
		glEnd()

		glBegin(self.y_layer_linetype)
		glColor3f(*self.y_layer_color)
		for item in self.y_layer_items:
			for point, index in zip(item, range(0, len(item))):
				glVertex2f(int(abs(point[0])), int(abs(point[1])))
				if index == len(item) - 1:
					glEnd()
					glBegin(self.y_layer_linetype)
					glColor3f(*self.y_layer_color)
		glEnd()
		glFlush()

	def on_mouse_scroll (self, event):
		try:
			glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
			if event.num == 5 or event.delta == -120:
				glScaled(0.95, 0.95, 0.95)
			if event.num == 4 or event.delta == 120:
				glScaled(1.05, 1.05, 1.05)
		except:
			raise Exception("Scroll error")

	def on_mouse_click (self, event):
		try:
			self.last_mouse_x_pos, self.last_mouse_y_pos = pyautogui.position()
		except:
			raise Exception("Click error")

	def on_mouse_drag (self, event):
		try:
			x, y = pyautogui.position()
			dx = x - self.last_mouse_x_pos
			dy = y - self.last_mouse_y_pos
			self.last_mouse_x_pos = x
			self.last_mouse_y_pos = y
			glTranslatef(-dy, dx, 0)
		except:
			raise Exception("Drag Error")

	def on_ctrl_hold (self, event):
		try:
			pass
		except:
			raise Exception("Ctrl error")





