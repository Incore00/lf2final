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

		self.image = pygame.Surface((self.highest_x - self.lowest_x, self.highest_y - self.lowest_y))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect(center=position)

	def update (self):
		self.image.fill(0)
		pygame.draw.polygon(self.image, self.color, self.new_item)
		self.mask = pygame.mask.from_surface(self.image)

	def change_color (self, color):
		self.color = color


class LeatherWindow_preview(tk.Frame):
	def __init__ (self, parent, queue, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.queue = queue

		os.environ['SDL_WINDOWID'] = str(self.winfo_id())
		os.environ['SDL_VIDEODRIVER'] = 'windows'
		pygame.display.init()

		window_size = (self.winfo_reqwidth(), self.winfo_reqheight())
		print('Window size', window_size)
		self.window = pygame.display.set_mode(window_size)

		cursor_image = pygame.image.load('cursor.png').convert_alpha()
		self.cursor_sprite = CursorSprite(0, 0, cursor_image)

		self.c_layer_items = None
		self.h_layer_items = None
		self.b_layer_items = None
		self.g_layer_items = None
		self.y_layer_items = None
		self.r_layer_items = None

		self.all_sprites = None

		self.pygame_loop()

	def pygame_loop (self):
		self.draw_sprites()

		self.hoover_checker()

		self.after(1, self.pygame_loop)

	def load_data (self, leather):
		self.c_layer_items = leather[0]
		self.h_layer_items = leather[1]
		self.b_layer_items = leather[2]
		self.g_layer_items = leather[3]
		self.y_layer_items = leather[4]
		self.r_layer_items = leather[5]



	def hoover_checker (self):
		pass

	def draw_sprites (self):
		self.all_sprites.update()
		self.screen.fill((0, 0, 0))
		self.all_sprites.draw(self.screen)
		pygame.display.flip()
