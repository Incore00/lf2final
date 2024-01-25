import tkinter as tk
import os
import pygame
import pyglet
from bin import configFile
from tkfontawesome import icon_to_image
from playsound import playsound
from multiprocessing import Process

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
#Na skórze (pozaz skazą):
#-cofnij
#-dodaj skaze
#
#Na skazie:
#-cofnij
#-warstwa(z kolejnym menu)
#-usuń
#-zmień rozmiar
#-przesuń
class DropdownMenuOption(pygame.sprite.Sprite):
	def __init__(self, x_size, y_size, position, text, font_color, bg_color, font = None, flaw_type = None):
		super().__init__()
		self.position = position
		self.x_size = x_size
		self.y_size = y_size
		self.text = text
		self.font_color = font_color
		self.flaw_type = flaw_type
		self.bg_color = bg_color
		self.image = pygame.Surface((x_size, y_size))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect(center=self.position)
		self.image.fill(bg_color)
		if font == None:
			self.font = pygame.font.Font('fonts/OpenSans/OpenSans.ttf', y_size)
		else:
			self.font = font
		self.rendered_text = self.font.render(text, True, font_color, bg_color)
		if self.text == 'Warstwa':
			self.image.blit(self.rendered_text, self.rendered_text.get_rect(center=((x_size - x_size * 0.1) / 2, y_size / 2)))
			pygame.draw.polygon(self.image, font_color, ((x_size, y_size/2), (x_size-x_size*0.1, 0+y_size*0.1), (x_size-x_size*0.1, y_size-y_size*0.1)))
		elif self.text == 'Niebieska' and self.flaw_type == 'blue':
			self.image.blit(self.rendered_text, self.rendered_text.get_rect(center=((x_size - x_size * 0.1) / 2, y_size / 2)))
			pygame.draw.lines(self.image, configFile.flaw_dropdown_menu_font_color, False, (
			(x_size - x_size*0.1, y_size / 2), (x_size - x_size * 0.05, y_size - y_size * 0.1),
			(x_size - x_size * 0.01,  y_size * 0.01)), int(y_size * 0.15))
		elif self.text == 'Zielona' and self.flaw_type == 'green':
			self.image.blit(self.rendered_text,
							self.rendered_text.get_rect(center=((x_size - x_size * 0.1) / 2, y_size / 2)))
			pygame.draw.lines(self.image, configFile.flaw_dropdown_menu_font_color, False, (
				(x_size - x_size * 0.1, y_size / 2), (x_size - x_size * 0.05, y_size - y_size * 0.1),
				(x_size - x_size * 0.01, y_size * 0.01)), int(y_size * 0.15))
		elif self.text == 'Czerwona' and self.flaw_type == 'red':
			self.image.blit(self.rendered_text,
							self.rendered_text.get_rect(center=((x_size - x_size * 0.1) / 2, y_size / 2)))
			pygame.draw.lines(self.image, configFile.flaw_dropdown_menu_font_color, False, (
				(x_size - x_size * 0.1, y_size / 2), (x_size - x_size * 0.05, y_size - y_size * 0.1),
				(x_size - x_size * 0.01, y_size * 0.01)), int(y_size * 0.15))
		elif self.text == 'Żółta' and self.flaw_type == 'yellow':
			self.image.blit(self.rendered_text,
							self.rendered_text.get_rect(center=((x_size - x_size * 0.1) / 2, y_size / 2)))
			pygame.draw.lines(self.image, configFile.flaw_dropdown_menu_font_color, False, (
				(x_size - x_size * 0.1, y_size / 2), (x_size - x_size * 0.05, y_size - y_size * 0.1),
				(x_size - x_size * 0.01, y_size * 0.01)), int(y_size * 0.15))
		else:
			self.image.blit(self.rendered_text, self.rendered_text.get_rect(center=(x_size / 2, y_size / 2)))
		self.mask = pygame.mask.from_surface(self.image)

	def on_hoover(self):
		self.font.bold = True
		self.__init__(self.x_size, self.y_size, self.position, self.text, self.font_color, self.bg_color, self.font, self.flaw_type)
		if self.text == 'Warstwa':
			return 'Warstwa'

	def on_leave(self):
		self.font.bold = False
		self.__init__(self.x_size, self.y_size, self.position, self.text, self.font_color, self.bg_color, self.font, self.flaw_type)
		if self.text == 'Warstwa':
			return 'Warstwa'

	def on_click(self, flaw_list = None):
		if flaw_list != None:
			for flaw in flaw_list.keys():
				if self.text == 'Cofnij':
					print('Cofnij')
				elif self.text == 'Warstwa':
					print('Warstwa')
				elif self.text == 'Usuń':
					print('Usuń')
					flaw.kill()
				elif self.text == 'Przesuń':
					print('Przesuń')
				elif self.text == 'Niebieska':
					flaw.change_flaw_type('blue')
					playsound('sounds\Q1.wav', False)
				elif self.text == 'Zielona':
					flaw.change_flaw_type('green')
					playsound('sounds\Q2.wav', False)
				elif self.text == 'Żółta':
					flaw.change_flaw_type('yellow')
					playsound('sounds\Q3.wav', False)
				elif self.text == 'Czerwona':
					flaw.change_flaw_type('red')
					playsound('sounds\Q4.wav', False)
		else:
			if self.text == 'Rysuj skaze':
				print('Rysuj skaze')
	#def update(self):
	#	#pygame.draw.rect(self.image, configFile.flaw_dropdown_menu_option_color, self.rect, border_radius=0)
	#	self.rect = self.image.get_rect(center=self.position)
	#	self.mask = pygame.mask.from_surface(self.image)

#-cofnij
#-warstwa(z kolejnym menu)
#-usuń
#-zmień rozmiar
#-przesuń





class CursorSprite(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.Surface((configFile.cursor_radius*2,configFile.cursor_radius*2))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect(center=(configFile.cursor_radius, configFile.cursor_radius))
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		mouse_pos = pygame.mouse.get_pos()
		pygame.draw.circle(self.image, configFile.cursor_color, (configFile.cursor_radius, configFile.cursor_radius), configFile.cursor_radius)
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.center = mouse_pos


class FlawSprite(pygame.sprite.Sprite):
	def __init__ (self, item, color, position, flaw_type):
		super().__init__()
		self.item = item
		self.color = color
		self.flaw_type = flaw_type
		self.linetype = None
		self.visable = True
		self.position = position
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
		self.rect = self.image.get_rect(center=self.position)
	def update_flaw(self, item, position):
		self.position = position
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
		temp_item = []
		for point in self.item:
			temp_item.append([point[0] + (position[0] - self.position[0]), point[1] + (position[1] - self.position[1])])
		self.__init__(temp_item, self.color, position, self.flaw_type)

	def update (self):
		self.image.fill(0)
		if self.flaw_type == 'blue':
			self.linetype = configFile.b_layer_linetype
			self.visable = configFile.b_layer_flag
		elif self.flaw_type == 'red':
			self.linetype = configFile.r_layer_linetype
			self.visable = configFile.r_layer_flag
		elif self.flaw_type == 'green':
			self.linetype = configFile.g_layer_linetype
			self.visable = configFile.g_layer_flag
		elif self.flaw_type == 'yellow':
			self.linetype = configFile.y_layer_linetype
			self.visable = configFile.y_layer_flag
		if self.linetype == 'polygon' and self.visable == True:
			pygame.draw.polygon(self.image, self.color, self.new_item)
		elif self.linetype == 'lines' and self.visable == True:
			pygame.draw.lines(self.image, self.color, True, self.new_item)
		self.mask = pygame.mask.from_surface(self.image)

	def change_color (self, color):
		self.color = color

	def change_flaw_type(self, type):
		self.flaw_type = type
		if type == 'blue':
			self.color = configFile.b_layer_color
		elif type == 'green':
			self.color = configFile.g_layer_color
		elif type == 'yellow':
			self.color = configFile.y_layer_color
		elif type == 'red':
			self.color = configFile.r_layer_color


class LeatherWindow_preview(tk.Frame):
	def __init__ (self, parent, queue, *args, **kwargs):
		tk.Frame.__init__(self, parent, *args, **kwargs)
		self.parent = parent
		self.queue = queue

		self.configure(bg='blue')

		os.environ['SDL_WINDOWID'] = str(self.winfo_id())
		os.environ['SDL_VIDEODRIVER'] = 'windows'
		pygame.display.init()
		pygame.font.init()

		window_size = (self.winfo_reqwidth(), self.winfo_reqheight())
		print('Window size', window_size)
		self.screen = pygame.display.set_mode(window_size)
		#pygame.mouse.set_visible(False)

		self.cursor_sprite = CursorSprite()
		self.cursor_sprite = pygame.sprite.GroupSingle(self.cursor_sprite)

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

		self.c_layer_items_offset = []
		self.h_layer_items_offset = []
		self.b_layer_items_offset = []
		self.g_layer_items_offset = []
		self.y_layer_items_offset = []
		self.r_layer_items_offset = []

		self.h_layer_flaw_center_list = []
		self.b_layer_flaw_center_list = []
		self.g_layer_flaw_center_list = []
		self.y_layer_flaw_center_list = []
		self.r_layer_flaw_center_list = []

		self.creating_shapes = False
		self.updating_shapes = False
		self.leather_draging = False

		self.color = 0
		self.max_color_flag = False

		self.dropdown_menu_bg = None
		self.dropdown_options_sprites = None
		self.dropdown_options_grouped_sprites = None
		self.options_grouped_sprites = None

		self.dropdown_layer_options_grouped_sprites = None
		self.dropdown_layer_options_sprites = None
		self.dropdown_layer_menu_bg = None

		self.dropdown_option_on_hoover = None
		self.dropdown_layer_option_on_hoover = None
		self.choosed_menu_option = None
		self.choosed_layer_menu_option = None
		self.dropdown_menu_flag = False

		self.edit_mode = False
		self.editted_flaw = None
		self.editted_flaw_offset = None
		self.flaw_center_list_index = None
		self.editted_flaw_start_position = None
		self.editted_flaw_index = None

		self.drawing_mode = False
		self.drawing_flaw_started = False
		self.drawing_flaw_points = []


		self.clicked_flaws = None
		self.flaw_grouped_sprites = None
		self.flaw_sprites = None
		self.leather_center = None
		self.zoom_tick = 0.99

		self.pygame_loop()

	def pygame_loop (self):
		self.all_sprites.update()
		self.all_sprites.draw(self.screen)

		if self.options_grouped_sprites != None and len(self.dropdown_options_sprites) != 2:
			pygame.draw.rect(self.screen, configFile.flaw_dropdown_menu_color, pygame.Rect(self.dropdown_menu_bg))
			self.options_grouped_sprites.update()
			self.options_grouped_sprites.draw(self.screen)
		elif self.options_grouped_sprites != None and len(self.dropdown_options_sprites) == 2:
			pygame.draw.rect(self.screen, configFile.dropdown_menu_color, pygame.Rect(self.dropdown_menu_bg))
			self.options_grouped_sprites.update()
			self.options_grouped_sprites.draw(self.screen)
		if self.dropdown_layer_options_grouped_sprites != None:
			pygame.draw.rect(self.screen, configFile.dropdown_menu_color, pygame.Rect(self.dropdown_layer_menu_bg))
			self.dropdown_layer_options_grouped_sprites.update()
			self.dropdown_layer_options_grouped_sprites.draw(self.screen)

		self.cursor_sprite.update()
		self.cursor_sprite.draw(self.screen)

		pygame.display.flip()

		if self.clicked_flaws != None:
			self.change_flaw_color(self.clicked_flaws)

		try:
			item = self.queue.get(0)
			if item[0] == 'preview_reload':
				self.updating_shapes = True
			else:
				self.queue.put(item)
		except:
			pass
		try:
			item = self.queue.get(0)
			if item[0] == 'preview_load_data':
				self.load_data(item[1])
			else:
				self.queue.put(item)
		except:
			pass
		try:
			item = self.queue.get(0)
			if item[0] == 'preview_zoom_in':
				self.zoom_in(item[1])
			else:
				self.queue.put(item)
		except:
			pass

		try:
			item = self.queue.get(0)
			if item[0] == 'preview_zoom_out':
				self.zoom_out(item[1], True)
			else:
				self.queue.put(item)
		except:
			pass

		try:
			item = self.queue.get(0)
			if item[0] == 'preview_dragging':
				self.dragging_income(item[1])
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
		self.screen.fill(configFile.bg_layer_color)
		if self.c_layer_items != None:
			pygame.draw.lines(self.screen, configFile.c_layer_color, True, self.displayed_c_layer_items)
		if str(self.drawing_flaw_points) != '[]' and self.drawing_flaw_points != None and len(self.drawing_flaw_points) >= 2:
			print('drawing poionts', self.drawing_flaw_points)
			pygame.draw.lines(self.screen, configFile.c_layer_color, False, self.drawing_flaw_points)
		if self.drawing_flaw_started == True:
			self.drawing_flaw_points.append(pygame.mouse.get_pos())

		self.after(1, self.pygame_loop)

	def change_flaw_color(self, collide_list):
		for flaw in collide_list.keys():
			if flaw.flaw_type == 'hole':
				pass
			else:
				if self.max_color_flag != True:
					self.color = min(255, self.color + (3/len(collide_list.keys())))
				else:
					self.color = max(0, self.color - (3/len(collide_list.keys())))
				if self.color >= 255:
					self.max_color_flag = True
				elif self.color <= 0:
					self.max_color_flag = False
				self.reset_flaws_colors(collide_list.keys())
				if flaw.flaw_type == 'blue':
					flaw.change_color((self.color, self.color, 255))
				elif flaw.flaw_type == 'green':
					flaw.change_color((self.color, 255, self.color))
				elif flaw.flaw_type == 'yellow':
					flaw.change_color((255, 255, self.color))
				elif flaw.flaw_type == 'red':
					flaw.change_color((255, self.color, self.color))

		if str(collide_list) == '{}' and self.clicked_flaws == None or str(self.clicked_flaws) == '{}' and str(collide_list) != '{}':
			self.reset_flaws_colors()
			self.color = 0

	def layer_choose_menu(self, flaw_list, position):
		if len(flaw_list) == 1 and self.dropdown_layer_options_grouped_sprites == None:
			self.dropdown_layer_options_sprites = []
			self.dropdown_layer_menu_bg = [position[0], position[1], configFile.flaw_dropdown_menu_x_size,
									 configFile.flaw_dropdown_menu_y_size]
			self.option_border = int((configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * 0.1)
			self.option_x_size = int(configFile.flaw_dropdown_menu_x_size - 2 * self.option_border)
			self.option_y_size = int((configFile.flaw_dropdown_menu_y_size - (self.option_border * (configFile.flaw_dropdown_menu_options_amount + 1))) / configFile.flaw_dropdown_menu_options_amount)
			self.layer_options_positions = []
			for option in range(0, 4):
				self.layer_options_positions.append((position[0] + configFile.flaw_dropdown_menu_x_size / 2, position[1] + (int((configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * option) + configFile.flaw_dropdown_menu_y_size / (2 * configFile.flaw_dropdown_menu_options_amount))))
			for flaw in flaw_list.keys():
				self.flaw_layer = flaw.flaw_type
			for option_name, option_position in zip(configFile.flaw_dropdown_layer_menu_options, self.layer_options_positions):
				if option_name == 'Niebieska':
					self.dropdown_layer_options_sprites.append(DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
																				  configFile.b_layer_color, configFile.flaw_dropdown_menu_option_color, None, self.flaw_layer))
				elif option_name == 'Zielona':
					self.dropdown_layer_options_sprites.append(DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
																				  configFile.g_layer_color, configFile.flaw_dropdown_menu_option_color, None, self.flaw_layer))
				elif option_name == 'Żółta':
					self.dropdown_layer_options_sprites.append(DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
																				  configFile.y_layer_color, configFile.flaw_dropdown_menu_option_color, None, self.flaw_layer))
				elif option_name == 'Czerwona':
					self.dropdown_layer_options_sprites.append(DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
																				  configFile.r_layer_color, configFile.flaw_dropdown_menu_option_color, None, self.flaw_layer))
			self.dropdown_layer_options_grouped_sprites = pygame.sprite.Group([*self.dropdown_layer_options_sprites])



	def event_checker (self):
		if self.dropdown_layer_options_grouped_sprites != None:
			dropdown_layer_options_collide_list = pygame.sprite.groupcollide(self.dropdown_layer_options_grouped_sprites, self.cursor_sprite, False, False, collided=pygame.sprite.collide_mask)
			if self.dropdown_layer_option_on_hoover != None:
				for option in self.dropdown_layer_option_on_hoover:
					if option in dropdown_layer_options_collide_list:
						continue
					else:
						option.on_leave()
			self.dropdown_layer_option_on_hoover = dropdown_layer_options_collide_list
			for option in dropdown_layer_options_collide_list.keys():
				if pygame.mouse.get_pos()[0] >= option.position[0]-option.x_size/2 and pygame.mouse.get_pos()[0] <= option.position[0]+option.x_size/2 and pygame.mouse.get_pos()[1] <= option.position[1]+option.y_size/2 and pygame.mouse.get_pos()[1] >= option.position[1]-option.y_size/2:
					option.on_hoover()
					self.choosed_layer_menu_option = option
				else:
					option.on_leave()
		if self.options_grouped_sprites != None:
			dropdown_collide_list = pygame.sprite.groupcollide(self.options_grouped_sprites, self.cursor_sprite, False, False, collided=pygame.sprite.collide_mask)
			if self.dropdown_option_on_hoover != None:
				for option in self.dropdown_option_on_hoover:
					if option in dropdown_collide_list:
						continue
					else:
						if option.on_leave() == 'Warstwa' and self.dropdown_layer_menu_bg != None:
							if pygame.mouse.get_pos()[0] >= self.dropdown_layer_menu_bg[0] and pygame.mouse.get_pos()[1] >= self.dropdown_layer_menu_bg[1] and pygame.mouse.get_pos()[0] <= self.dropdown_layer_menu_bg[0] + self.dropdown_layer_menu_bg[2] and pygame.mouse.get_pos()[1] <= self.dropdown_layer_menu_bg[1] + self.dropdown_layer_menu_bg[3]:
								pass
							else:
								self.dropdown_layer_options_grouped_sprites = None
						else:
							option.on_leave()
			self.dropdown_option_on_hoover = dropdown_collide_list
			for option in dropdown_collide_list.keys():
				if pygame.mouse.get_pos()[0] >= option.position[0]-option.x_size/2 and pygame.mouse.get_pos()[0] <= option.position[0]+option.x_size/2 and pygame.mouse.get_pos()[1] <= option.position[1]+option.y_size/2 and pygame.mouse.get_pos()[1] >= option.position[1]-option.y_size/2:
					if option.on_hoover() == 'Warstwa':
						self.layer_choose_menu(self.clicked_flaws, (option.position[0]+option.x_size/2, option.position[1]-option.y_size/2))
					self.choosed_menu_option = option
				else:
					if option.on_leave() == 'Warstwa' and self.dropdown_layer_menu_bg != None:

						if pygame.mouse.get_pos()[0] >= self.dropdown_layer_menu_bg[0] and pygame.mouse.get_pos()[1] >= self.dropdown_layer_menu_bg[1] and pygame.mouse.get_pos()[0] <= self.dropdown_layer_menu_bg[0] + self.dropdown_layer_menu_bg[2] and pygame.mouse.get_pos()[1] <= self.dropdown_layer_menu_bg[1] + self.dropdown_layer_menu_bg[3]:
							pass
						else:
							self.dropdown_layer_options_grouped_sprites = None
					else:
						option.on_leave()
		if self.flaw_grouped_sprites != None and self.dropdown_menu_flag == False:
			collide_list = pygame.sprite.groupcollide(self.flaw_grouped_sprites,self.cursor_sprite, False, False, collided = pygame.sprite.collide_mask)
			if self.clicked_flaws != None:
				# tu dodawac co ma sie dziac po kliknieciu
				some_flaws = collide_list
				some_flaws.update(self.clicked_flaws)
				self.change_flaw_color(some_flaws)
			else:
				self.change_flaw_color(collide_list)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEWHEEL:
				if event.y == 1 and self.edit_mode == False and self.drawing_mode == False:
					self.zoom_in(False)
				elif event.y != 1 and self.edit_mode == False and self.drawing_mode == False:
					self.zoom_out(False, True)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and self.displayed_c_layer_items != None and self.edit_mode == False and self.drawing_mode == False:
					if self.dropdown_menu_flag == True:
						self.dropdown_menu_flag = False
					if self.choosed_menu_option != None and self.dropdown_option_on_hoover != None and self.choosed_menu_option in self.dropdown_option_on_hoover.keys() and self.clicked_flaws != None:
						self.choosed_menu_option.on_click(self.clicked_flaws)
						print('clicked flaws 1', self.clicked_flaws)
						if self.choosed_menu_option.text == 'Przesuń' and len(self.clicked_flaws) == 1:
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
							self.edit_mode = True
						self.choosed_menu_option = None
					if self.choosed_menu_option != None and self.dropdown_option_on_hoover != None and self.choosed_menu_option in self.dropdown_option_on_hoover.keys() and self.clicked_flaws == None:
						if self.choosed_menu_option.text == 'Rysuj skaze':
							print('Rysuj skaze prev')
							self.choosed_menu_option.on_click()
							self.drawing_mode = True
					if self.choosed_layer_menu_option != None and self.dropdown_layer_option_on_hoover != None and self.choosed_layer_menu_option in self.dropdown_layer_option_on_hoover.keys():
						self.choosed_layer_menu_option.on_click(self.clicked_flaws)
						print('clicked flaws 2', self.clicked_flaws)
						if self.choosed_menu_option.text == 'Przesuń' and len(self.clicked_flaws) == 1:
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
							self.edit_mode = True
						if self.choosed_layer_menu_option.text == 'Niebieska':
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
								if self.editted_flaw.position in self.b_layer_flaw_center_list:
									pass
								elif self.editted_flaw.position in self.g_layer_flaw_center_list:
									flaw_index = self.g_layer_flaw_center_list.index(self.editted_flaw.position)
									self.b_layer_flaw_center_list.append(self.g_layer_flaw_center_list.pop(flaw_index))
									self.displayed_b_layer_items.append(self.displayed_g_layer_items.pop(flaw_index))
									self.displayed_b_layer_flaws.append(self.displayed_g_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.y_layer_flaw_center_list:
									flaw_index = self.y_layer_flaw_center_list.index(self.editted_flaw.position)
									self.b_layer_flaw_center_list.append(self.y_layer_flaw_center_list.pop(flaw_index))
									self.displayed_b_layer_items.append(self.displayed_y_layer_items.pop(flaw_index))
									self.displayed_b_layer_flaws.append(self.displayed_y_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.r_layer_flaw_center_list:
									flaw_index = self.r_layer_flaw_center_list.index(self.editted_flaw.position)
									self.b_layer_flaw_center_list.append(self.r_layer_flaw_center_list.pop(flaw_index))
									self.displayed_b_layer_items.append(self.displayed_r_layer_items.pop(flaw_index))
									self.displayed_b_layer_flaws.append(self.displayed_r_layer_flaws.pop(flaw_index))
						elif self.choosed_layer_menu_option.text == 'Zielona':
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
								if self.editted_flaw.position in self.b_layer_flaw_center_list:
									flaw_index = self.b_layer_flaw_center_list.index(self.editted_flaw.position)
									self.g_layer_flaw_center_list.append(self.b_layer_flaw_center_list.pop(flaw_index))
									self.displayed_g_layer_items.append(self.displayed_b_layer_items.pop(flaw_index))
									self.displayed_g_layer_flaws.append(self.displayed_b_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.g_layer_flaw_center_list:
									pass
								elif self.editted_flaw.position in self.y_layer_flaw_center_list:
									flaw_index = self.y_layer_flaw_center_list.index(self.editted_flaw.position)
									self.g_layer_flaw_center_list.append(self.y_layer_flaw_center_list.pop(flaw_index))
									self.displayed_g_layer_items.append(self.displayed_y_layer_items.pop(flaw_index))
									self.displayed_g_layer_flaws.append(self.displayed_y_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.r_layer_flaw_center_list:
									flaw_index = self.r_layer_flaw_center_list.index(self.editted_flaw.position)
									self.g_layer_flaw_center_list.append(self.r_layer_flaw_center_list.pop(flaw_index))
									self.displayed_g_layer_items.append(self.displayed_r_layer_items.pop(flaw_index))
									self.displayed_g_layer_flaws.append(self.displayed_r_layer_flaws.pop(flaw_index))
						elif self.choosed_layer_menu_option.text == 'Żółta':
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
								if self.editted_flaw.position in self.b_layer_flaw_center_list:
									flaw_index = self.b_layer_flaw_center_list.index(self.editted_flaw.position)
									self.y_layer_flaw_center_list.append(self.b_layer_flaw_center_list.pop(flaw_index))
									self.displayed_y_layer_items.append(self.displayed_b_layer_items.pop(flaw_index))
									self.displayed_y_layer_flaws.append(self.displayed_b_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.g_layer_flaw_center_list:
									flaw_index = self.g_layer_flaw_center_list.index(self.editted_flaw.position)
									self.y_layer_flaw_center_list.append(self.g_layer_flaw_center_list.pop(flaw_index))
									self.displayed_y_layer_items.append(self.displayed_g_layer_items.pop(flaw_index))
									self.displayed_y_layer_flaws.append(self.displayed_g_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.y_layer_flaw_center_list:
									pass
								elif self.editted_flaw.position in self.r_layer_flaw_center_list:
									flaw_index = self.r_layer_flaw_center_list.index(self.editted_flaw.position)
									self.y_layer_flaw_center_list.append(self.r_layer_flaw_center_list.pop(flaw_index))
									self.displayed_y_layer_items.append(self.displayed_r_layer_items.pop(flaw_index))
									self.displayed_y_layer_flaws.append(self.displayed_r_layer_flaws.pop(flaw_index))
						elif self.choosed_layer_menu_option.text == 'Czerwona':
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
								if self.editted_flaw.position in self.b_layer_flaw_center_list:
									flaw_index = self.b_layer_flaw_center_list.index(self.editted_flaw.position)
									self.r_layer_flaw_center_list.append(self.b_layer_flaw_center_list.pop(flaw_index))
									self.displayed_r_layer_items.append(self.displayed_b_layer_items.pop(flaw_index))
									self.displayed_r_layer_flaws.append(self.displayed_b_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.g_layer_flaw_center_list:
									flaw_index = self.g_layer_flaw_center_list.index(self.editted_flaw.position)
									self.r_layer_flaw_center_list.append(self.g_layer_flaw_center_list.pop(flaw_index))
									self.displayed_r_layer_items.append(self.displayed_g_layer_items.pop(flaw_index))
									self.displayed_r_layer_flaws.append(self.displayed_g_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.y_layer_flaw_center_list:
									flaw_index = self.y_layer_flaw_center_list.index(self.editted_flaw.position)
									self.r_layer_flaw_center_list.append(self.y_layer_flaw_center_list.pop(flaw_index))
									self.displayed_r_layer_items.append(self.displayed_y_layer_items.pop(flaw_index))
									self.displayed_r_layer_flaws.append(self.displayed_y_layer_flaws.pop(flaw_index))
								elif self.editted_flaw.position in self.r_layer_flaw_center_list:
									pass
						self.choosed_layer_menu_option = None
					collide_list = pygame.sprite.groupcollide(self.flaw_grouped_sprites,self.cursor_sprite, False, False, collided = pygame.sprite.collide_mask)
					if str(collide_list) != '{}':
						self.clicked_flaws = collide_list
					else:
						self.clicked_flaws = None
					self.leather_draging = True
					mouse_x, mouse_y = event.pos
					if self.options_grouped_sprites != None:
						self.options_grouped_sprites = None
					if self.dropdown_layer_options_grouped_sprites != None:
						self.dropdown_layer_options_grouped_sprites = None
					if self.displayed_c_layer_items != None:
						for point in self.displayed_c_layer_items:
							self.c_layer_items_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
					if self.displayed_h_layer_items != None:
						for item in self.displayed_h_layer_items:
							offset_list = []
							for point in item:
								offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
							self.h_layer_items_offset.append(offset_list)
					if self.displayed_b_layer_items != None:
						for item in self.displayed_b_layer_items:
							offset_list = []
							for point in item:
								offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
							self.b_layer_items_offset.append(offset_list)
					if self.displayed_g_layer_items != None:
						for item in self.displayed_g_layer_items:
							offset_list = []
							for point in item:
								offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
							self.g_layer_items_offset.append(offset_list)
					if self.displayed_y_layer_items != None:
						for item in self.displayed_y_layer_items:
							offset_list = []
							for point in item:
								offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
							self.y_layer_items_offset.append(offset_list)
					if self.displayed_r_layer_items != None:
						for item in self.displayed_r_layer_items:
							offset_list = []
							for point in item:
								offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
							self.r_layer_items_offset.append(offset_list)
				elif event.button == 1 and self.edit_mode == True and self.editted_flaw != None:
					self.editted_flaw_offset = []
					mouse_x, mouse_y = pygame.mouse.get_pos()
					if self.editted_flaw.flaw_type == 'hole':
						self.editted_flaw_index = self.h_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_h_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x) , point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'blue':
						self.editted_flaw_index = self.b_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_b_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x) , point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'green':
						self.editted_flaw_index = self.g_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_g_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x) , point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'yellow':
						self.editted_flaw_index = self.y_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_y_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x) , point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'red':
						self.editted_flaw_index = self.r_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_r_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x) , point[1] - mouse_y])
				elif event.button == 1 and self.drawing_mode == True:
					#rysowanie nowej skazy
					self.drawing_flaw_started = True
				elif event.button == 3 and self.displayed_c_layer_items != None:
					self.leather_draging = False
					collide_list = pygame.sprite.groupcollide(self.flaw_grouped_sprites, self.cursor_sprite, False,
															  False, collided=pygame.sprite.collide_mask)
					if len(collide_list) >= 1:
						self.clicked_flaws = collide_list
						self.flaw_dropdown_menu()
						self.updating_shapes = True
						break
					if self.clicked_flaws != None and len(self.clicked_flaws) >= 1:
						self.flaw_dropdown_menu()
						self.updating_shapes = True
						break
					if str(collide_list) == '{}' and self.clicked_flaws == None or self.clicked_flaws == 0 and str(collide_list) == '{}':
						self.dropdown_menu()
						self.clicked_flaws = None
						self.updating_shapes = True

			elif event.type == pygame.MOUSEMOTION:
				if self.leather_draging and self.edit_mode == False and self.drawing_mode == False:
					mouse_x, mouse_y = event.pos
					sh, sw = self.winfo_reqheight(), self.winfo_reqwidth()
					new_c_layer_items = []
					new_h_layer_items = []
					new_b_layer_items = []
					new_g_layer_items = []
					new_y_layer_items = []
					new_r_layer_items = []
					self.temp_drag_diff_c_layer_items = []
					self.temp_drag_diff_h_layer_items = []
					self.temp_drag_diff_b_layer_items = []
					self.temp_drag_diff_g_layer_items = []
					self.temp_drag_diff_y_layer_items = []
					self.temp_drag_diff_r_layer_items = []
					if self.displayed_c_layer_items != None:
						for point, offset in zip(self.displayed_c_layer_items, self.c_layer_items_offset):
							new_c_layer_items.append([(offset[0] + mouse_x), (offset[1] + mouse_y)])
							self.temp_drag_diff_c_layer_items.append(
								[(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
						self.displayed_c_layer_items = new_c_layer_items
					if self.displayed_h_layer_items != None:
						for item, item_offset in zip(self.displayed_h_layer_items, self.h_layer_items_offset):
							item_list = []
							diff_list = []
							for point, offset in zip(item, item_offset):
								item_list.append([(offset[0] + mouse_x), offset[1] + mouse_y])
								diff_list.append(
									[(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
							self.temp_drag_diff_h_layer_items.append(diff_list)
							new_h_layer_items.append(item_list)
						self.displayed_h_layer_items = new_h_layer_items
					if self.displayed_b_layer_items != None:
						for item, item_offset in zip(self.displayed_b_layer_items, self.b_layer_items_offset):
							item_list = []
							diff_list = []
							for point, offset in zip(item, item_offset):
								item_list.append([(offset[0] + mouse_x), offset[1] + mouse_y])
								diff_list.append(
									[(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
							self.temp_drag_diff_b_layer_items.append(diff_list)
							new_b_layer_items.append(item_list)
						self.displayed_b_layer_items = new_b_layer_items
					if self.displayed_g_layer_items != None:
						for item, item_offset in zip(self.displayed_g_layer_items, self.g_layer_items_offset):
							item_list = []
							diff_list = []
							for point, offset in zip(item, item_offset):
								item_list.append([(offset[0] + mouse_x), offset[1] + mouse_y])
								diff_list.append(
									[(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
							self.temp_drag_diff_g_layer_items.append(diff_list)
							new_g_layer_items.append(item_list)
						self.displayed_g_layer_items = new_g_layer_items
					if self.displayed_y_layer_items != None:
						for item, item_offset in zip(self.displayed_y_layer_items, self.y_layer_items_offset):
							item_list = []
							diff_list = []
							for point, offset in zip(item, item_offset):
								item_list.append([(offset[0] + mouse_x), offset[1] + mouse_y])
								diff_list.append(
									[(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
							self.temp_drag_diff_y_layer_items.append(diff_list)
							new_y_layer_items.append(item_list)
						self.displayed_y_layer_items = new_y_layer_items
					if self.displayed_r_layer_items != None:
						for item, item_offset in zip(self.displayed_r_layer_items, self.r_layer_items_offset):
							item_list = []
							diff_list = []
							for point, offset in zip(item, item_offset):
								item_list.append([(offset[0] + mouse_x), offset[1] + mouse_y])
								diff_list.append(
									[(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
							self.temp_drag_diff_r_layer_items.append(diff_list)
							new_r_layer_items.append(item_list)
						self.displayed_r_layer_items = new_r_layer_items
					if self.displayed_c_layer_items != None:
						dragging_changes = [self.temp_drag_diff_c_layer_items, self.temp_drag_diff_h_layer_items,
											self.temp_drag_diff_b_layer_items, self.temp_drag_diff_g_layer_items,
											self.temp_drag_diff_y_layer_items, self.temp_drag_diff_r_layer_items]
						self.queue.put(['main_dragging', dragging_changes])
						self.updating_shapes = True
				elif self.edit_mode == True and self.editted_flaw != None and self.editted_flaw_offset != None and str(self.editted_flaw_offset) != '[]':
					sh, sw = self.winfo_reqheight(), self.winfo_reqwidth()
					mouse_pos = pygame.mouse.get_pos()
					if self.editted_flaw_start_position == None:
						self.editted_flaw_start_position = self.editted_flaw.position
					if self.editted_flaw.flaw_type == 'hole':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_h_layer_items[self.editted_flaw_index], self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw, (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_h_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'blue':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_b_layer_items[self.editted_flaw_index], self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw, (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_b_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'green':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_g_layer_items[self.editted_flaw_index], self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw, (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_g_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'yellow':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_y_layer_items[self.editted_flaw_index], self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw, (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_y_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'red':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_r_layer_items[self.editted_flaw_index], self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw, (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_r_layer_items[self.editted_flaw_index] = item_list
					self.updating_shapes = True
						# jeszcze diff
					#self.editted_flaw.update_position([self.editted_flaw_offset[0] + mouse_pos[0], self.editted_flaw_offset[1] + mouse_pos[1]])

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if self.edit_mode == True and self.editted_flaw_start_position != None:
						self.editted_flaw_start_position = None
						self.edit_mode = False
						self.editted_flaw_offset = None
						#self.editted_flaw = None
					if self.drawing_flaw_started == True and len(self.drawing_flaw_points) >= 2:
						self.drawing_mode = False
						self.drawing_flaw_started = False
						self.drawing_flaw_points = []
					self.leather_draging = False
					self.c_layer_items_offset = []
					self.h_layer_items_offset = []
					self.b_layer_items_offset = []
					self.g_layer_items_offset = []
					self.y_layer_items_offset = []
					self.r_layer_items_offset = []

	def flaw_dropdown_menu(self):
		if self.dropdown_menu_flag == False:
			self.mouse_pos = pygame.mouse.get_pos()
			self.dropdown_menu_bg = [self.mouse_pos[0], self.mouse_pos[1], configFile.flaw_dropdown_menu_x_size, configFile.flaw_dropdown_menu_y_size]
			self.dropdown_options_sprites = []
			self.option_border = int((configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * 0.1)
			self.option_x_size = int(configFile.flaw_dropdown_menu_x_size - 2 * self.option_border)
			self.option_y_size = int((configFile.flaw_dropdown_menu_y_size - (self.option_border * (configFile.flaw_dropdown_menu_options_amount +1)))/configFile.flaw_dropdown_menu_options_amount)
			self.options_positions = []
			for option in range(0, configFile.flaw_dropdown_menu_options_amount):
				self.options_positions.append((self.mouse_pos[0] + configFile.flaw_dropdown_menu_x_size / 2, self.mouse_pos[1] + (int((configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * option) + configFile.flaw_dropdown_menu_y_size / (2 * configFile.flaw_dropdown_menu_options_amount))))
			for option_name, position in zip(configFile.flaw_dropdown_menu_options, self.options_positions):
				self.dropdown_options_sprites.append(DropdownMenuOption(self.option_x_size, self.option_y_size, position, option_name, configFile.flaw_dropdown_menu_font_color, configFile.flaw_dropdown_menu_option_color))
			self.options_grouped_sprites = pygame.sprite.Group([*self.dropdown_options_sprites])
			self.dropdown_menu_flag = True

	def dropdown_menu(self):
		if self.dropdown_menu_flag == False:
			self.mouse_pos = pygame.mouse.get_pos()
			self.dropdown_menu_bg = [self.mouse_pos[0], self.mouse_pos[1], configFile.dropdown_menu_x_size, configFile.dropdown_menu_y_size]
			self.dropdown_options_sprites = []
			self.option_border = int((configFile.dropdown_menu_y_size / configFile.dropdown_menu_options_amount) * 0.1)
			self.option_x_size = int(configFile.dropdown_menu_x_size - 2 * self.option_border)
			self.option_y_size = int((configFile.dropdown_menu_y_size - (self.option_border * (configFile.dropdown_menu_options_amount +1)))/configFile.dropdown_menu_options_amount)
			self.options_positions = []
			for option in range(0, configFile.dropdown_menu_options_amount):
				self.options_positions.append((self.mouse_pos[0] + configFile.dropdown_menu_x_size / 2,
											   self.mouse_pos[1] + (int((configFile.dropdown_menu_y_size / configFile.dropdown_menu_options_amount) * option) + configFile.dropdown_menu_y_size / (
																				2 * configFile.dropdown_menu_options_amount))))
			for option_name, position in zip(configFile.dropdown_menu_options, self.options_positions):
				self.dropdown_options_sprites.append(
					DropdownMenuOption(self.option_x_size, self.option_y_size, position, option_name, configFile.dropdown_menu_font_color, configFile.dropdown_menu_option_color))
			self.options_grouped_sprites = pygame.sprite.Group([*self.dropdown_options_sprites])
			self.dropdown_menu_flag = True



	def reset_flaws_colors(self, flaws_to_Skip = [None, None]):
		if self.flaw_sprites != None:
			for flaw_list in self.flaw_sprites:
				for flaw in flaw_list:
					if flaw in flaws_to_Skip:
						pass
					else:
						if flaw.flaw_type == 'blue':
							flaw.change_color(configFile.b_layer_color)
						elif flaw.flaw_type == 'green':
							flaw.change_color(configFile.g_layer_color)
						elif flaw.flaw_type == 'yellow':
							flaw.change_color(configFile.y_layer_color)
						elif flaw.flaw_type == 'red':
							flaw.change_color(configFile.r_layer_color)

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

	def dragging_income(self, dragging_changes):
		sh, sw = self.winfo_reqheight(), self.winfo_reqwidth()
		temp_drag_diff_c_layer_items = dragging_changes[0]
		temp_drag_diff_h_layer_items = dragging_changes[1]
		temp_drag_diff_b_layer_items = dragging_changes[2]
		temp_drag_diff_g_layer_items = dragging_changes[3]
		temp_drag_diff_y_layer_items = dragging_changes[4]
		temp_drag_diff_r_layer_items = dragging_changes[5]

		new_c_layer_items = []
		new_h_layer_items = []
		new_b_layer_items = []
		new_g_layer_items = []
		new_y_layer_items = []
		new_r_layer_items = []
		for point, diff in zip(self.displayed_c_layer_items, temp_drag_diff_c_layer_items):
			new_c_layer_items.append([(point[0] - (diff[0] * sw)), (point[1] - (diff[1] * sh))])
		self.displayed_c_layer_items = new_c_layer_items
		for item, item_diff in zip(self.displayed_h_layer_items, temp_drag_diff_h_layer_items):
			item_list = []
			for point, diff in zip(item, item_diff):
				item_list.append([(point[0] - (diff[0] * sw)), (point[1] - (diff[1]) * sh)])
			new_h_layer_items.append(item_list)
		self.displayed_h_layer_items = new_h_layer_items
		for item, item_diff in zip(self.displayed_b_layer_items, temp_drag_diff_b_layer_items):
			item_list = []
			for point, diff in zip(item, item_diff):
				item_list.append([(point[0] - (diff[0] * sw)), (point[1] - (diff[1] * sh))])
			new_b_layer_items.append(item_list)
		self.displayed_b_layer_items = new_b_layer_items
		for item, item_diff in zip(self.displayed_g_layer_items, temp_drag_diff_g_layer_items):
			item_list = []
			for point, diff in zip(item, item_diff):
				item_list.append([(point[0] - (diff[0] * sw)), (point[1] - (diff[1] * sh))])
			new_g_layer_items.append(item_list)
		self.displayed_g_layer_items = new_g_layer_items
		for item, item_diff in zip(self.displayed_y_layer_items, temp_drag_diff_y_layer_items):
			item_list = []
			for point, diff in zip(item, item_diff):
				item_list.append([(point[0] - (diff[0] * sw)), (point[1] - (diff[1] * sh))])
			new_y_layer_items.append(item_list)
		self.displayed_y_layer_items = new_y_layer_items
		for item, item_diff in zip(self.displayed_r_layer_items, temp_drag_diff_r_layer_items):
			item_list = []
			for point, diff in zip(item, item_diff):
				item_list.append([(point[0] - (diff[0] * sw)), (point[1] - (diff[1] * sh))])
			new_r_layer_items.append(item_list)
		self.displayed_r_layer_items = new_r_layer_items

		self.updating_shapes = True
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
		self.screen.fill(configFile.bg_layer_color)
		if self.c_layer_items != None:
			pygame.draw.lines(self.screen, configFile.c_layer_color, True, self.displayed_c_layer_items)
		if self.h_layer_items != None:
			for item, item_center in zip(self.displayed_h_layer_items, self.h_layer_flaw_center_list):
				self.displayed_h_layer_flaws.append(FlawSprite(item, configFile.h_layer_color, item_center, 'hole'))
			self.flaw_sprites.append(self.displayed_h_layer_flaws)
		if self.b_layer_items != None:
			for item, item_center in zip(self.displayed_b_layer_items, self.b_layer_flaw_center_list):
				self.displayed_b_layer_flaws.append(FlawSprite(item, configFile.b_layer_color, item_center, 'blue'))
			self.flaw_sprites.append(self.displayed_b_layer_flaws)
		if self.g_layer_items != None:
			for item, item_center in zip(self.displayed_g_layer_items, self.g_layer_flaw_center_list):
				self.displayed_g_layer_flaws.append(FlawSprite(item, configFile.g_layer_color, item_center, 'green'))
			self.flaw_sprites.append(self.displayed_g_layer_flaws)
		if self.y_layer_items != None:
			for item, item_center in zip(self.displayed_y_layer_items, self.y_layer_flaw_center_list):
				self.displayed_y_layer_flaws.append(FlawSprite(item, configFile.y_layer_color, item_center, 'yellow'))
			self.flaw_sprites.append(self.displayed_y_layer_flaws)
		if self.r_layer_items != None:
			for item, item_center in zip(self.displayed_r_layer_items, self.r_layer_flaw_center_list):
				self.displayed_r_layer_flaws.append(FlawSprite(item, configFile.r_layer_color, item_center, 'red'))
			self.flaw_sprites.append(self.displayed_r_layer_flaws)

		if str(self.flaw_sprites) != '[]':
			self.all_sprites = pygame.sprite.Group([*self.flaw_sprites, self.cursor_sprite])
			self.flaw_grouped_sprites = pygame.sprite.Group([*self.flaw_sprites])

		if self.all_sprites != None:
			self.all_sprites.update()
			self.all_sprites.draw(self.screen)

		print('prev shapes created')

	def update_shapes(self):
		self.screen.fill(configFile.bg_layer_color)
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