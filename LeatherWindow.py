import tkinter as tk
import os
import pygame
import math



class LeatherWindow(tk.Frame):
	def __init__ (self, parent, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent

		os.environ['SDL_WINDOWID'] = str(self.winfo_id())
		os.environ['SDL_VIDEODRIVER'] = 'windib'
		pygame.display.init()
		window_size = (self.winfo_screenwidth(), self.winfo_screenheight())
		self.screen = pygame.display.set_mode(window_size)

		self.main_surface = pygame.Surface(window_size)

		self.leather = None
		self.offset_x = None
		self.offset_y = None

		self.bg_layer_color = (0, 0, 0)
		self.c_layer_color = (255, 255, 255)
		self.h_layer_color = (127, 127, 127)
		self.b_layer_color = (0, 0, 255)
		self.b_layer_linetype = "lines"
		self.g_layer_color = (0, 255, 0)
		self.g_layer_linetype = "lines"
		self.y_layer_color = (255, 255, 0)
		self.y_layer_linetype = "lines"
		self.r_layer_color = (255, 0, 0)
		self.r_layer_linetype = "lines"

		self.highest_x = None
		self.highest_y = None
		self.lowest_x = None
		self.lowest_y = None

		self.c_layer_items = None
		self.h_layer_items = None
		self.b_layer_items = None
		self.g_layer_items = None
		self.y_layer_items = None
		self.r_layer_items = None

		self.c_layer_items_offset = []
		self.h_layer_items_offset = []
		self.b_layer_items_offset = []
		self.g_layer_items_offset = []
		self.y_layer_items_offset = []
		self.r_layer_items_offset = []

		self.h_layer_flag = True
		self.b_layer_flag = True
		self.g_layer_flag = True
		self.y_layer_flag = True
		self.r_layer_flag = True

		self.leather_center = None

		self.leather_c_layer_line = []
		self.leather_c_layer_line_len = []
		self.zoom_tick = 0.99

		self.leather_draging = False

		self.drawing_shapes = False

		self.pygame_loop()

	def change_layers_visiblity(self, h_layer_flag, b_layer_flag, g_layer_flag, y_layer_flag, r_layer_flag):
		self.h_layer_flag = h_layer_flag
		self.b_layer_flag = b_layer_flag
		self.g_layer_flag = g_layer_flag
		self.y_layer_flag = y_layer_flag
		self.r_layer_flag = r_layer_flag
		self.drawing_shapes = False

	def change_colors_func (self, bg_layer_color, c_layer_color, h_layer_color, b_layer_color, b_layer_linetype,
				  g_layer_color, g_layer_linetype, y_layer_color, y_layer_linetype, r_layer_color,
				  r_layer_linetype):
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
		self.drawing_shapes = False

	def load_leather_data(self, leather, bg_layer_color, c_layer_color, h_layer_color, b_layer_color, b_layer_linetype,
				  g_layer_color, g_layer_linetype, y_layer_color, y_layer_linetype, r_layer_color,
				  r_layer_linetype): #c h b g y r

		self.leather = leather

		self.c_layer_items = self.leather.c_layer_point_list_to_display
		self.h_layer_items = self.leather.h_layer_point_list_to_display
		self.b_layer_items = self.leather.b_layer_point_list_to_display
		self.g_layer_items = self.leather.g_layer_point_list_to_display
		self.y_layer_items = self.leather.y_layer_point_list_to_display
		self.r_layer_items = self.leather.r_layer_point_list_to_display

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

		if self.c_layer_items != None:
			self.highest_x = self.c_layer_items[0][0]
			self.highest_y = self.c_layer_items[0][1]
			self.lowest_x = self.c_layer_items[0][0]
			self.lowest_y = self.c_layer_items[0][1]

			for point in self.c_layer_items:
				if point[0] > self.highest_x:
					self.highest_x = point[0]
				if point[0] < self.lowest_x:
					self.lowest_x = point[0]
				if point[1] < self.lowest_y:
					self.lowest_y = point[1]
				if point[1] > self.highest_y:
					self.highest_y = point[1]

			self.leather_center = [self.lowest_x + ((self.highest_x - self.lowest_x)/2), self.lowest_y + ((self.highest_y - self.lowest_y)/2)]

		self.calculate_position()
		self.drawing_shapes = False

	def pygame_loop (self):
		#rotated_surface = pygame.transform.rotate(self.main_surface, 180)
		self.screen.blit(self.main_surface,(0,0))
		pygame.display.flip()
		if self.drawing_shapes == False and self.leather != None:
			self.draw_shapes()
			self.drawing_shapes = True

		self.event_checker()

		self.update()
		self.after(1, self.pygame_loop)

	def zoom_in(self):
		center_point = [self.winfo_screenwidth()/2 , self.winfo_screenheight()/2]
		new_layer = []
		for point in self.c_layer_items:
			wspol_a = (point[1]-center_point[1])/(point[0]-center_point[0])
			wspol_b = point[1]-(((point[1]-center_point[1])/(point[0]-center_point[0])*point[0]))
			nowe_x = center_point[0]+(point[0]-center_point[0]) / self.zoom_tick
			nowe_y = wspol_a * nowe_x + wspol_b
			new_layer.append([nowe_x, nowe_y])
		self.c_layer_items = new_layer
		new_layer = []
		for item in self.h_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.h_layer_items = new_layer
		new_layer = []
		for item in self.b_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.b_layer_items = new_layer
		new_layer = []
		for item in self.g_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.g_layer_items = new_layer
		new_layer = []
		for item in self.y_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.y_layer_items = new_layer
		new_layer = []
		for item in self.r_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.r_layer_items = new_layer

		self.drawing_shapes = False

	def zoom_out(self):
		center_point = [self.winfo_screenwidth() / 2, self.winfo_screenheight() / 2]
		new_layer = []
		for point in self.c_layer_items:
			wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
			wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
			nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
			nowe_y = wspol_a * nowe_x + wspol_b
			new_layer.append([nowe_x, nowe_y])
		self.c_layer_items = new_layer
		new_layer = []
		for item in self.h_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.h_layer_items = new_layer
		new_layer = []
		for item in self.b_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.b_layer_items = new_layer
		new_layer = []
		for item in self.g_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.g_layer_items = new_layer
		new_layer = []
		for item in self.y_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.y_layer_items = new_layer
		new_layer = []
		for item in self.r_layer_items:
			item_list = []
			for point in item:
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
			new_layer.append(item_list)
		self.r_layer_items = new_layer

		self.drawing_shapes = False

	def event_checker (self):
		for event in pygame.event.get():
			if event.type == pygame.MOUSEWHEEL:
				if event.y == 1:
					self.zoom_in()
				elif event.y != 1:
					self.zoom_out()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and self.leather != None:
					self.leather_draging = True
					mouse_x, mouse_y = event.pos
					for point in self.c_layer_items:
						self.c_layer_items_offset.append([(point[0] - mouse_x) , point[1] - mouse_y])
					for item in self.h_layer_items:
						offset_list = []
						for point in item:
							offset_list.append([(point[0] - mouse_x) , point[1] - mouse_y])
						self.h_layer_items_offset.append(offset_list)
					for item in self.b_layer_items:
						offset_list = []
						for point in item:
							offset_list.append([(point[0] - mouse_x) , point[1] - mouse_y])
						self.b_layer_items_offset.append(offset_list)
					for item in self.g_layer_items:
						offset_list = []
						for point in item:
							offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
						self.g_layer_items_offset.append(offset_list)
					for item in self.y_layer_items:
						offset_list = []
						for point in item:
							offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
						self.y_layer_items_offset.append(offset_list)
					for item in self.r_layer_items:
						offset_list = []
						for point in item:
							offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
						self.r_layer_items_offset.append(offset_list)

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1 and self.leather != None:
					self.leather_draging = False
					self.c_layer_items_offset = []
					self.h_layer_items_offset = []
					self.b_layer_items_offset = []
					self.g_layer_items_offset = []
					self.y_layer_items_offset = []
					self.r_layer_items_offset = []
			elif event.type == pygame.MOUSEMOTION:
				if self.leather_draging and self.leather != None:
					mouse_x, mouse_y = event.pos
					new_c_layer_items = []
					new_h_layer_items = []
					new_b_layer_items = []
					new_g_layer_items = []
					new_y_layer_items = []
					new_r_layer_items = []
					for point, offset in zip(self.c_layer_items, self.c_layer_items_offset):
						new_c_layer_items.append([(offset[0] + mouse_x) , (offset[1] + mouse_y)])
					self.c_layer_items = new_c_layer_items
					for item, item_offset in zip(self.h_layer_items, self.h_layer_items_offset):
						item_list = []
						for point, offset in zip(item, item_offset):
							item_list.append([(offset[0] + mouse_x) , offset[1] + mouse_y])
						new_h_layer_items.append(item_list)
					self.h_layer_items = new_h_layer_items
					for item, item_offset in zip(self.b_layer_items, self.b_layer_items_offset):
						item_list = []
						for point, offset in zip(item, item_offset):
							item_list.append([(offset[0] + mouse_x) , offset[1] + mouse_y])
						new_b_layer_items.append(item_list)
					self.b_layer_items = new_b_layer_items
					for item, item_offset in zip(self.g_layer_items, self.g_layer_items_offset):
						item_list = []
						for point, offset in zip(item, item_offset):
							item_list.append([(offset[0] + mouse_x) , offset[1] + mouse_y])
						new_g_layer_items.append(item_list)
					self.g_layer_items = new_g_layer_items
					for item, item_offset in zip(self.y_layer_items, self.y_layer_items_offset):
						item_list = []
						for point, offset in zip(item, item_offset):
							item_list.append([(offset[0] + mouse_x) , offset[1] + mouse_y])
						new_y_layer_items.append(item_list)
					self.y_layer_items = new_y_layer_items
					for item, item_offset in zip(self.r_layer_items, self.r_layer_items_offset):
						item_list = []
						for point, offset in zip(item, item_offset):
							item_list.append([(offset[0] + mouse_x) , offset[1] + mouse_y])
						new_r_layer_items.append(item_list)
					self.r_layer_items = new_r_layer_items
					self.drawing_shapes = False

	def calculate_position(self):
		self.c_layer_items_pos_offset = []
		self.h_layer_items_pos_offset = []
		self.b_layer_items_pos_offset = []
		self.g_layer_items_pos_offset = []
		self.y_layer_items_pos_offset = []
		self.r_layer_items_pos_offset = []
		for point in self.c_layer_items:
			self.c_layer_items_pos_offset.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
		for item in self.h_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.h_layer_items_pos_offset.append(offset_list)
		for item in self.b_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.b_layer_items_pos_offset.append(offset_list)
		for item in self.g_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.g_layer_items_pos_offset.append(offset_list)
		for item in self.y_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.y_layer_items_pos_offset.append(offset_list)
		for item in self.r_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.r_layer_items_pos_offset.append(offset_list)

		new_c_layer_items = []
		new_h_layer_items = []
		new_b_layer_items = []
		new_g_layer_items = []
		new_y_layer_items = []
		new_r_layer_items = []

		sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
		screen_center = [sw/2, sh/2]

		for point, offset in zip(self.c_layer_items, self.c_layer_items_pos_offset):
			new_c_layer_items.append([(offset[0] + screen_center[0]), (offset[1] + screen_center[1])])
		self.c_layer_items = new_c_layer_items
		for item, item_offset in zip(self.h_layer_items, self.h_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([(offset[0] + screen_center[0]), offset[1] + screen_center[1]])
			new_h_layer_items.append(item_list)
		self.h_layer_items = new_h_layer_items
		for item, item_offset in zip(self.b_layer_items, self.b_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([(offset[0] + screen_center[0]), offset[1] + screen_center[1]])
			new_b_layer_items.append(item_list)
		self.b_layer_items = new_b_layer_items
		for item, item_offset in zip(self.g_layer_items, self.g_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([(offset[0] + screen_center[0]), offset[1] + screen_center[1]])
			new_g_layer_items.append(item_list)
		self.g_layer_items = new_g_layer_items
		for item, item_offset in zip(self.y_layer_items, self.y_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([(offset[0] + screen_center[0]), offset[1] + screen_center[1]])
			new_y_layer_items.append(item_list)
		self.y_layer_items = new_y_layer_items
		for item, item_offset in zip(self.r_layer_items, self.r_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([(offset[0] + screen_center[0]), offset[1] + screen_center[1]])
			new_r_layer_items.append(item_list)
		self.r_layer_items = new_r_layer_items
		self.drawing_shapes = False



	def draw_shapes (self):
		self.main_surface.fill(self.bg_layer_color)
		# Draw shapes

		if self.c_layer_items != None:
			pygame.draw.lines(self.main_surface, self.c_layer_color, True, self.c_layer_items)
		if self.h_layer_items != None and self.h_layer_flag == True:
			for item in self.h_layer_items:
				pygame.draw.lines(self.main_surface, self.h_layer_color, True, item)
		if self.g_layer_items != None and self.g_layer_flag == True:
			for item in self.g_layer_items:
				if self.g_layer_linetype == "lines":
					pygame.draw.lines(self.main_surface, self.g_layer_color, True, item)
				elif self.g_layer_linetype == "polygon":
					pygame.draw.polygon(self.main_surface, self.g_layer_color, item)
		if self.b_layer_items != None and self.b_layer_flag == True:
			for item in self.b_layer_items:
				if self.b_layer_linetype == "lines":
					pygame.draw.lines(self.main_surface, self.b_layer_color, True, item)
				elif self.b_layer_linetype == "polygon":
					pygame.draw.polygon(self.main_surface, self.b_layer_color, item)
		if self.y_layer_items != None and self.y_layer_flag == True:
			for item in self.y_layer_items:
				if self.y_layer_linetype == "lines":
					pygame.draw.lines(self.main_surface, self.y_layer_color, True, item)
				elif self.y_layer_linetype == "polygon":
					pygame.draw.polygon(self.main_surface, self.y_layer_color, item)
		if self.r_layer_items != None and self.r_layer_flag == True:
			for item in self.r_layer_items:
				if self.r_layer_linetype == "lines":
					pygame.draw.lines(self.main_surface, self.r_layer_color, True, item)
				elif self.r_layer_linetype == "polygon":
					pygame.draw.polygon(self.main_surface, self.r_layer_color, item)


