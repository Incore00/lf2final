import tkinter as tk
import os
import pygame
import pyglet
from bin import configFile

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')


class Leatherpreview(tk.Frame):
	def __init__ (self, parent, queue, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.queue = queue
		self.pack_propagate(0)
		self.grid_propagate(0)
		self.sw, self.sh = int(parent.winfo_reqwidth() * 0.765), int(parent.winfo_reqheight() * 0.765)
		print(self.sw, self.sh)
		self.configure(height=self.sh, width=self.sw, bg='#0000FF')

		LeatherWindow_preview(self, self.queue, height=self.sh, width=self.sw).pack(side="top", fill="both",
																					expand=True)


class CursorSprite(pygame.sprite.Sprite):
	def __init__ (self, x, y, image):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect(center=(x, y))
		self.mask = pygame.mask.from_surface(self.image)

	def update (self):
		self.rect.center = pygame.mouse.get_pos()


class FlawSprite(pygame.sprite.Sprite):
	def __init__ (self, item, color, position):
		super().__init__()
		self.color = color
		self.new_item = []
		self.lowest_x = item[0][0]
		self.highest_x = item[0][0]
		self.lowest_y = item[0][1]
		self.highest_y = item[0][1]
		for point in item:
			if point[0] > self.highest_x:
				self.highest_x = point[0]
			if point[0] < self.lowest_x:
				self.lowest_x = point[0]
			if point[1] < self.lowest_y:
				self.lowest_y = point[1]
			if point[1] > self.highest_y:
				self.highest_y = point[1]
		for point in item:
			self.new_item.append([point[0] - self.lowest_x, point[1] - self.lowest_y])

		self.image = pygame.Surface((self.highest_x - self.lowest_x + 1, self.highest_y - self.lowest_y + 1))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect(center=position)

	def update_flaw(self, item, position):
		self.new_item = []
		self.lowest_x = item[0][0]
		self.highest_x = item[0][0]
		self.lowest_y = item[0][1]
		self.highest_y = item[0][1]
		for point in item:
			if point[0] > self.highest_x:
				self.highest_x = point[0]
			if point[0] < self.lowest_x:
				self.lowest_x = point[0]
			if point[1] < self.lowest_y:
				self.lowest_y = point[1]
			if point[1] > self.highest_y:
				self.highest_y = point[1]
		for point in item:
			self.new_item.append([point[0] - self.lowest_x, point[1] - self.lowest_y])

		self.image = pygame.Surface((self.highest_x - self.lowest_x + 1, self.highest_y - self.lowest_y + 1))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect(center=position)
		self.mask = pygame.mask.from_surface(self.image)

	def update_position(self, position):
		self.rect = self.image.get_rect(center=position)

	def update (self):
		self.image.fill(0)
		pygame.draw.lines(self.image, self.color, True, self.new_item)
		#pygame.draw.polygon(self.image, self.color, self.new_item)
		self.mask = pygame.mask.from_surface(self.image)

	def change_color (self, color):
		self.color = color


class LeatherWindow_preview(tk.Frame):
	def __init__ (self, parent, queue, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.queue = queue

		self.configure(bg='blue')

		os.environ['SDL_WINDOWID'] = str(self.winfo_id())
		os.environ['SDL_VIDEODRIVER'] = 'windows'
		pygame.display.init()

		window_size = (self.winfo_reqwidth(), self.winfo_reqheight())
		print('Window size', window_size)
		self.screen = pygame.display.set_mode(window_size)

		cursor_image = pygame.image.load('cursor.png').convert_alpha()
		self.cursor_sprite = CursorSprite(0, 0, cursor_image)

		self.all_sprites = pygame.sprite.Group([self.cursor_sprite])

		self.c_layer_items = None
		self.h_layer_items = None
		self.b_layer_items = None
		self.g_layer_items = None
		self.y_layer_items = None
		self.r_layer_items = None
		self.text_layer_items = None

		self.displayed_c_layer_items = None
		self.displayed_h_layer_items = None
		self.displayed_b_layer_items = None
		self.displayed_g_layer_items = None
		self.displayed_y_layer_items = None
		self.displayed_r_layer_items = None
		self.displayed_text_layer_items = None

		self.displayed_h_layer_flaws = None
		self.displayed_b_layer_flaws = None
		self.displayed_g_layer_flaws = None
		self.displayed_y_layer_flaws = None
		self.displayed_r_layer_flaws = None

		self.h_layer_flaw_center_list = []
		self.b_layer_flaw_center_list = []
		self.g_layer_flaw_center_list = []
		self.y_layer_flaw_center_list = []
		self.r_layer_flaw_center_list = []

		self.creating_shapes = False
		self.updating_shapes = False

		self.flaw_grouped_sprites = None
		self.flaw_sprites = None
		self.leather_center = None
		self.zoom_tick = 0.99

		self.pygame_loop()

	def pygame_loop (self):
		self.all_sprites.update()
		self.all_sprites.draw(self.screen)
		pygame.display.flip()
		try:
			item = self.queue.get(0)
			if item[0] == 'preview_load_data':
				self.load_data(item[1])
			else:
				self.queue.put(item)
		except:
			pass

		self.event_checker()

		if self.creating_shapes == True:
			self.create_shapes()
			self.creating_shapes = False

		if self.updating_shapes == True:
			self.update_shapes()
			self.updating_shapes = False

		self.after(1, self.pygame_loop)

	def event_checker (self):
		if self.flaw_grouped_sprites != None:
			if pygame.sprite.spritecollide(self.cursor_sprite, self.flaw_grouped_sprites, True):
				print('collision!!!')
			#if pygame.sprite.spritecollideany(self.cursor_sprite, self.flaw_grouped_sprites):
			#	print('collision!')

		for event in pygame.event.get():
			if event.type == pygame.MOUSEWHEEL:
				if event.y == 1:
					self.zoom_in(False)
				elif event.y != 1:
					self.zoom_out(False, True)


	def load_data (self, leather):
		self.c_layer_items = leather[0]
		self.h_layer_items = leather[1]
		self.b_layer_items = leather[2]
		self.g_layer_items = leather[3]
		self.y_layer_items = leather[4]
		self.r_layer_items = leather[5]
		self.text_layer_items = leather[6]

		self.calculate_rotation()
		self.calculate_center()
		self.calculate_position()
		self.calculate_zoom()
		self.creating_shapes = True
		print('preview data loaded')

	def calculate_rotation(self):
		new_c_layer_points = []
		new_h_layer_items = []
		new_b_layer_items = []
		new_g_layer_items = []
		new_y_layer_items = []
		new_r_layer_items = []
		new_text_layer_items = []
		for point in self.c_layer_items:
			new_c_layer_points.append([point[1], point[0]])
		self.displayed_c_layer_items = new_c_layer_points
		for item in self.h_layer_items:
			point_list = []
			for point in item:
				point_list.append([point[1], point[0]])
			new_h_layer_items.append(point_list)
		self.displayed_h_layer_items = new_h_layer_items
		for item in self.b_layer_items:
			point_list = []
			for point in item:
				point_list.append([point[1], point[0]])
			new_b_layer_items.append(point_list)
		self.displayed_b_layer_items = new_b_layer_items
		for item in self.g_layer_items:
			point_list = []
			for point in item:
				point_list.append([point[1], point[0]])
			new_g_layer_items.append(point_list)
		self.displayed_g_layer_items = new_g_layer_items
		for item in self.y_layer_items:
			point_list = []
			for point in item:
				point_list.append([point[1], point[0]])
			new_y_layer_items.append(point_list)
		self.displayed_y_layer_items = new_y_layer_items
		for item in self.r_layer_items:
			point_list = []
			for point in item:
				point_list.append([point[1], point[0]])
			new_r_layer_items.append(point_list)
		self.displayed_r_layer_items = new_r_layer_items
		for point in self.text_layer_items:
			new_text_layer_items.append([point[1], point[0]])
		self.displayed_text_layer_items = new_text_layer_items

	def calculate_center(self):
		if self.c_layer_items != None:
			self.highest_x = self.displayed_c_layer_items[0][0]
			self.highest_y = self.displayed_c_layer_items[0][1]
			self.lowest_x = self.displayed_c_layer_items[0][0]
			self.lowest_y = self.displayed_c_layer_items[0][1]

			for point in self.displayed_c_layer_items:
				if point[0] > self.highest_x:
					self.highest_x = point[0]
				if point[0] < self.lowest_x:
					self.lowest_x = point[0]
				if point[1] < self.lowest_y:
					self.lowest_y = point[1]
				if point[1] > self.highest_y:
					self.highest_y = point[1]

			self.leather_center = [self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
								   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)]

	def calculate_position (self):
		self.c_layer_items_pos_offset = []
		self.h_layer_items_pos_offset = []
		self.b_layer_items_pos_offset = []
		self.g_layer_items_pos_offset = []
		self.y_layer_items_pos_offset = []
		self.r_layer_items_pos_offset = []
		self.text_layer_items_pos_offset = []

		for point in self.displayed_c_layer_items:
			self.c_layer_items_pos_offset.append(
				[(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
		for item in self.displayed_h_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.h_layer_items_pos_offset.append(offset_list)
		for item in self.displayed_b_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.b_layer_items_pos_offset.append(offset_list)
		for item in self.displayed_g_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.g_layer_items_pos_offset.append(offset_list)
		for item in self.displayed_y_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.y_layer_items_pos_offset.append(offset_list)
		for item in self.displayed_r_layer_items:
			offset_list = []
			for point in item:
				offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
			self.r_layer_items_pos_offset.append(offset_list)
		for point in self.displayed_text_layer_items:
			self.text_layer_items_pos_offset.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])


		new_c_layer_items = []
		new_h_layer_items = []
		new_b_layer_items = []
		new_g_layer_items = []
		new_y_layer_items = []
		new_r_layer_items = []
		new_text_layer_items = []

		sw, sh = self.winfo_reqwidth(), self.winfo_reqheight()
		screen_center = [sw / 2, sh / 2]

		for offset in self.c_layer_items_pos_offset:
			new_c_layer_items.append(
				[round((offset[0] + screen_center[0]), 1), round((offset[1] + screen_center[1]), 1)])
		self.displayed_c_layer_items = new_c_layer_items
		for item, item_offset in zip(self.displayed_h_layer_items, self.h_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
			new_h_layer_items.append(item_list)
		self.displayed_h_layer_items = new_h_layer_items
		for item, item_offset in zip(self.displayed_b_layer_items, self.b_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
			new_b_layer_items.append(item_list)
		self.displayed_b_layer_items = new_b_layer_items
		for item, item_offset in zip(self.displayed_g_layer_items, self.g_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
			new_g_layer_items.append(item_list)
		self.displayed_g_layer_items = new_g_layer_items
		for item, item_offset in zip(self.displayed_y_layer_items, self.y_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
			new_y_layer_items.append(item_list)
		self.displayed_y_layer_items = new_y_layer_items
		for item, item_offset in zip(self.displayed_r_layer_items, self.r_layer_items_pos_offset):
			item_list = []
			for point, offset in zip(item, item_offset):
				item_list.append([round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
			new_r_layer_items.append(item_list)
		self.displayed_r_layer_items = new_r_layer_items
		for point, offset in zip(self.displayed_text_layer_items, self.text_layer_items_pos_offset):
			new_text_layer_items.append([round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
		self.displayed_text_layer_items = new_text_layer_items

	def calculate_zoom (self):
		if self.c_layer_items != None:
			self.highest_x = self.displayed_c_layer_items[0][0]
			self.highest_y = self.displayed_c_layer_items[0][1]
			self.lowest_x = self.displayed_c_layer_items[0][0]
			self.lowest_y = self.displayed_c_layer_items[0][1]

			for point in self.displayed_c_layer_items:
				if point[0] > self.highest_x:
					self.highest_x = point[0]
				if point[0] < self.lowest_x:
					self.lowest_x = point[0]
				if point[1] < self.lowest_y:
					self.lowest_y = point[1]
				if point[1] > self.highest_y:
					self.highest_y = point[1]

			if self.lowest_y >= 0 and self.highest_y <= self.winfo_reqheight() and self.lowest_x >= 0 and self.highest_x <= self.winfo_reqwidth():
				pass
			else:
				self.zoom_out(True, False)
				self.calculate_zoom()

	def zoom_out (self, queue_flag, update_flag):
		if queue_flag == False:
			self.queue.put(['main_zoom_out', True, True])
		center_point = [self.winfo_reqwidth() / 2, self.winfo_reqheight() / 2]
		new_layer = []
		for point in self.displayed_c_layer_items:
			if point[0] == center_point[0]:
				center_point[0] += 0.01
			wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
			wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
			nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
			nowe_y = wspol_a * nowe_x + wspol_b
			if center_point[0] - point[0] == 0.01:
				center_point[0] -= 0.01
			new_layer.append([nowe_x, nowe_y])
		self.displayed_c_layer_items = new_layer
		new_layer = []
		for item in self.displayed_h_layer_items:
			item_list = []
			for point in item:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			new_layer.append(item_list)
		self.displayed_h_layer_items = new_layer
		new_layer = []
		for item in self.displayed_b_layer_items:
			item_list = []
			for point in item:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			new_layer.append(item_list)
		self.displayed_b_layer_items = new_layer
		new_layer = []
		for item in self.displayed_g_layer_items:
			item_list = []
			for point in item:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			new_layer.append(item_list)
		self.displayed_g_layer_items = new_layer
		new_layer = []
		for item in self.displayed_y_layer_items:
			item_list = []
			for point in item:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			new_layer.append(item_list)
		self.displayed_y_layer_items = new_layer
		new_layer = []
		for item in self.displayed_r_layer_items:
			item_list = []
			for point in item:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				item_list.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			new_layer.append(item_list)
		self.displayed_r_layer_items = new_layer
		new_layer = []
		for point in self.displayed_text_layer_items:
			if point[0] == center_point[0]:
				center_point[0] += 0.01
			wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
			wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
			nowe_x = center_point[0] + (point[0] - center_point[0]) * self.zoom_tick
			nowe_y = wspol_a * nowe_x + wspol_b
			new_layer.append([nowe_x, nowe_y])
			if center_point[0] - point[0] == 0.01:
				center_point[0] -= 0.01
		self.displayed_text_layer_items = new_layer

		if update_flag == True:
			self.updating_shapes = True

	def zoom_in (self, flag):
		if flag == False:
			self.queue.put(['main_zoom_in', True])
		center_point = [self.winfo_reqwidth() / 2, self.winfo_reqheight() / 2]
		new_layer = []
		if self.displayed_c_layer_items != None:
			for point in self.displayed_c_layer_items:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				new_layer.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			self.displayed_c_layer_items = new_layer
		new_layer = []
		if self.displayed_h_layer_items != None:
			for item in self.displayed_h_layer_items:
				item_list = []
				for point in item:
					if point[0] == center_point[0]:
						center_point[0] += 0.01
					wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
					wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
					nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
					nowe_y = wspol_a * nowe_x + wspol_b
					item_list.append([nowe_x, nowe_y])
					if center_point[0] - point[0] == 0.01:
						center_point[0] -= 0.01
				new_layer.append(item_list)
			self.displayed_h_layer_items = new_layer
		new_layer = []
		if self.displayed_b_layer_items != None:
			for item in self.displayed_b_layer_items:
				item_list = []
				for point in item:
					if point[0] == center_point[0]:
						center_point[0] += 0.01
					wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
					wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
					nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
					nowe_y = wspol_a * nowe_x + wspol_b
					item_list.append([nowe_x, nowe_y])
					if center_point[0] - point[0] == 0.01:
						center_point[0] -= 0.01
				new_layer.append(item_list)
			self.displayed_b_layer_items = new_layer
		new_layer = []
		if self.displayed_g_layer_items != None:
			for item in self.displayed_g_layer_items:
				item_list = []
				for point in item:
					if point[0] == center_point[0]:
						center_point[0] += 0.01
					wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
					wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
					nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
					nowe_y = wspol_a * nowe_x + wspol_b
					item_list.append([nowe_x, nowe_y])
					if center_point[0] - point[0] == 0.01:
						center_point[0] -= 0.01
				new_layer.append(item_list)
			self.displayed_g_layer_items = new_layer
		new_layer = []
		if self.displayed_y_layer_items != None:
			for item in self.displayed_y_layer_items:
				item_list = []
				for point in item:
					if point[0] == center_point[0]:
						center_point[0] += 0.01
					wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
					wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
					nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
					nowe_y = wspol_a * nowe_x + wspol_b
					item_list.append([nowe_x, nowe_y])
					if center_point[0] - point[0] == 0.01:
						center_point[0] -= 0.01
				new_layer.append(item_list)
			self.displayed_y_layer_items = new_layer
		new_layer = []
		if self.displayed_r_layer_items != None:
			for item in self.displayed_r_layer_items:
				item_list = []
				for point in item:
					if point[0] == center_point[0]:
						center_point[0] += 0.01
					wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
					wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
					nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
					nowe_y = wspol_a * nowe_x + wspol_b
					item_list.append([nowe_x, nowe_y])
					if center_point[0] - point[0] == 0.01:
						center_point[0] -= 0.01
				new_layer.append(item_list)
			self.displayed_r_layer_items = new_layer
		new_layer = []
		if self.displayed_text_layer_items != None:
			for point in self.displayed_text_layer_items:
				if point[0] == center_point[0]:
					center_point[0] += 0.01
				wspol_a = (point[1] - center_point[1]) / (point[0] - center_point[0])
				wspol_b = point[1] - (((point[1] - center_point[1]) / (point[0] - center_point[0]) * point[0]))
				nowe_x = center_point[0] + (point[0] - center_point[0]) / self.zoom_tick
				nowe_y = wspol_a * nowe_x + wspol_b
				new_layer.append([nowe_x, nowe_y])
				if center_point[0] - point[0] == 0.01:
					center_point[0] -= 0.01
			self.displayed_text_layer_items = new_layer

		self.updating_shapes = True

	def calculate_flaws_center (self):
		self.h_layer_flaw_center_list = []
		self.b_layer_flaw_center_list = []
		self.g_layer_flaw_center_list = []
		self.y_layer_flaw_center_list = []
		self.r_layer_flaw_center_list = []

		if self.displayed_h_layer_items != None:
			for item in self.displayed_h_layer_items:
				self.lowest_x = item[0][0]
				self.highest_x = item[0][0]
				self.lowest_y = item[0][1]
				self.highest_y = item[0][1]
				for point in item:
					if point[0] > self.highest_x:
						self.highest_x = point[0]
					if point[0] < self.lowest_x:
						self.lowest_x = point[0]
					if point[1] < self.lowest_y:
						self.lowest_y = point[1]
					if point[1] > self.highest_y:
						self.highest_y = point[1]
				self.h_layer_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
												   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)])
		if self.displayed_b_layer_items != None:
			for item in self.displayed_b_layer_items:
				self.lowest_x = item[0][0]
				self.highest_x = item[0][0]
				self.lowest_y = item[0][1]
				self.highest_y = item[0][1]
				for point in item:
					if point[0] > self.highest_x:
						self.highest_x = point[0]
					if point[0] < self.lowest_x:
						self.lowest_x = point[0]
					if point[1] < self.lowest_y:
						self.lowest_y = point[1]
					if point[1] > self.highest_y:
						self.highest_y = point[1]
				self.b_layer_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
												   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)])

		if self.displayed_g_layer_items != None:
			for item in self.displayed_g_layer_items:
				self.lowest_x = item[0][0]
				self.highest_x = item[0][0]
				self.lowest_y = item[0][1]
				self.highest_y = item[0][1]
				for point in item:
					if point[0] > self.highest_x:
						self.highest_x = point[0]
					if point[0] < self.lowest_x:
						self.lowest_x = point[0]
					if point[1] < self.lowest_y:
						self.lowest_y = point[1]
					if point[1] > self.highest_y:
						self.highest_y = point[1]
				self.g_layer_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
													self.lowest_y + ((self.highest_y - self.lowest_y) / 2)])

		if self.displayed_y_layer_items != None:
			for item in self.displayed_y_layer_items:
				self.lowest_x = item[0][0]
				self.highest_x = item[0][0]
				self.lowest_y = item[0][1]
				self.highest_y = item[0][1]
				for point in item:
					if point[0] > self.highest_x:
						self.highest_x = point[0]
					if point[0] < self.lowest_x:
						self.lowest_x = point[0]
					if point[1] < self.lowest_y:
						self.lowest_y = point[1]
					if point[1] > self.highest_y:
						self.highest_y = point[1]
				self.y_layer_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
													 self.lowest_y + ((self.highest_y - self.lowest_y) / 2)])
		if self.displayed_r_layer_items != None:
			for item in self.displayed_r_layer_items:
				self.lowest_x = item[0][0]
				self.highest_x = item[0][0]
				self.lowest_y = item[0][1]
				self.highest_y = item[0][1]
				for point in item:
					if point[0] > self.highest_x:
						self.highest_x = point[0]
					if point[0] < self.lowest_x:
						self.lowest_x = point[0]
					if point[1] < self.lowest_y:
						self.lowest_y = point[1]
					if point[1] > self.highest_y:
						self.highest_y = point[1]
				self.r_layer_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
												  self.lowest_y + ((self.highest_y - self.lowest_y) / 2)])

	def create_shapes (self):
		self.calculate_flaws_center()
		self.displayed_h_layer_flaws = []
		self.displayed_b_layer_flaws = []
		self.displayed_g_layer_flaws = []
		self.displayed_y_layer_flaws = []
		self.displayed_r_layer_flaws = []
		self.flaw_sprites = []
		self.screen.fill((0, 0, 0))
		if self.c_layer_items != None:
			pygame.draw.lines(self.screen, configFile.c_layer_color, True, self.displayed_c_layer_items)
		if self.h_layer_items != None:
			for item, item_center in zip(self.displayed_h_layer_items, self.h_layer_flaw_center_list):
				self.displayed_h_layer_flaws.append(FlawSprite(item, configFile.h_layer_color, item_center))
			self.flaw_sprites.append(self.displayed_h_layer_flaws)
		if self.b_layer_items != None:
			for item, item_center in zip(self.displayed_b_layer_items, self.b_layer_flaw_center_list):
				self.displayed_b_layer_flaws.append(FlawSprite(item, configFile.b_layer_color, item_center))
			self.flaw_sprites.append(self.displayed_b_layer_flaws)
		if self.g_layer_items != None:
			for item, item_center in zip(self.displayed_g_layer_items, self.g_layer_flaw_center_list):
				self.displayed_g_layer_flaws.append(FlawSprite(item, configFile.g_layer_color, item_center))
			self.flaw_sprites.append(self.displayed_g_layer_flaws)
		if self.y_layer_items != None:
			for item, item_center in zip(self.displayed_y_layer_items, self.y_layer_flaw_center_list):
				self.displayed_y_layer_flaws.append(FlawSprite(item, configFile.y_layer_color, item_center))
			self.flaw_sprites.append(self.displayed_y_layer_flaws)
		if self.r_layer_items != None:
			for item, item_center in zip(self.displayed_r_layer_items, self.r_layer_flaw_center_list):
				self.displayed_r_layer_flaws.append(FlawSprite(item, configFile.r_layer_color, item_center))
			self.flaw_sprites.append(self.displayed_r_layer_flaws)

		if str(self.flaw_sprites) != '[]':
			self.all_sprites = pygame.sprite.Group([self.cursor_sprite, *self.flaw_sprites])
			self.flaw_grouped_sprites = pygame.sprite.Group([*self.flaw_sprites])

		if self.all_sprites != None:
			self.all_sprites.update()
			self.all_sprites.draw(self.screen)

		print('prev shapes created')

	def update_shapes(self):
		self.screen.fill((0, 0, 0))
		self.calculate_flaws_center()

		if self.c_layer_items != None:
			pygame.draw.lines(self.screen, configFile.c_layer_color, True, self.displayed_c_layer_items)
		if self.displayed_h_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_h_layer_flaws, self.displayed_h_layer_items, self.h_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_b_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_b_layer_flaws, self.displayed_b_layer_items, self.b_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_g_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_g_layer_flaws, self.displayed_g_layer_items, self.g_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_y_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_y_layer_flaws, self.displayed_y_layer_items, self.y_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_r_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_r_layer_flaws, self.displayed_r_layer_items, self.r_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)

		if self.all_sprites != None:
			self.all_sprites.update()
			self.all_sprites.draw(self.screen)

		pygame.display.flip()
