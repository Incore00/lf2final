import tkinter as tk
import os
import pygame
import pyglet
from bin import configFile
from playsound import playsound
from bin.flaws import FlawSprite
from bin.dropdown import DropdownMenuOption
from bin.cursor import CursorSprite

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')

class Leathermain():
	def __init__(self, queue):
		root = tk.Tk()
		root.iconbitmap("images/icon.ico")
		root.title("LeatherView")
		sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
		root.geometry('%dx%d%+d+%d' % (sw, sh, 0, -sh))
		root.overrideredirect(True)
		LeatherWindow_main(root, queue, height=sh, width=sw).pack(side="top", fill="both", expand=True)

		root.mainloop()

class LeatherWindow_main(tk.Frame):
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
		# pygame.mouse.set_visible(False)

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

		self.temp_drawed_flaw = None
		self.assignation_flaw_mode = False
		self.assignation_flaw_points = []
		self.assignation_flaw_mode_started = False

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
			if item[0] == 'main_reload':
				self.updating_shapes = True
			else:
				self.queue.put(item)
		except:
			pass
		try:
			item = self.queue.get(0)
			if item[0] == 'main_load_data':
				self.load_data(item[1])
			else:
				self.queue.put(item)
		except:
			pass
		try:
			item = self.queue.get(0)
			if item[0] == 'main_zoom_in':
				self.zoom_in(item[1])
			else:
				self.queue.put(item)
		except:
			pass

		try:
			item = self.queue.get(0)
			if item[0] == 'main_zoom_out':
				self.zoom_out(item[1], True)
			else:
				self.queue.put(item)
		except:
			pass

		try:
			item = self.queue.get(0)
			if item[0] == 'main_dragging':
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
		if str(self.drawing_flaw_points) != '[]' and self.drawing_flaw_points != None and len(
				self.drawing_flaw_points) >= 2:
			pygame.draw.lines(self.screen, configFile.new_flaw_color, False, self.drawing_flaw_points)
		if self.drawing_flaw_started == True:
			self.drawing_flaw_points.append(pygame.mouse.get_pos())
		if self.temp_drawed_flaw != None:
			pygame.draw.polygon(self.screen, configFile.new_flaw_color, self.temp_drawed_flaw)
		if self.assignation_flaw_mode_started == True:
			self.assignation_flaw_points.append(pygame.mouse.get_pos())

		self.after(1, self.pygame_loop)

	def change_flaw_color (self, collide_list):
		for flaw in collide_list.keys():
			if flaw.flaw_type == 'hole':
				pass
			else:
				if self.max_color_flag != True:
					self.color = min(255, self.color + (3 / len(collide_list.keys())))
				else:
					self.color = max(0, self.color - (3 / len(collide_list.keys())))
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

		if str(collide_list) == '{}' and self.clicked_flaws == None or str(self.clicked_flaws) == '{}' and str(
				collide_list) != '{}':
			self.reset_flaws_colors()
			self.color = 0

	def layer_choose_menu (self, flaw_list, position):
		if len(flaw_list) == 1 and self.dropdown_layer_options_grouped_sprites == None:
			self.dropdown_layer_options_sprites = []
			self.dropdown_layer_menu_bg = [position[0], position[1], configFile.flaw_dropdown_menu_x_size,
										   configFile.flaw_dropdown_menu_y_size]
			self.option_border = int(
				(configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * 0.1)
			self.option_x_size = int(configFile.flaw_dropdown_menu_x_size - 2 * self.option_border)
			self.option_y_size = int((configFile.flaw_dropdown_menu_y_size - (self.option_border * (
						configFile.flaw_dropdown_menu_options_amount + 1))) / configFile.flaw_dropdown_menu_options_amount)
			self.layer_options_positions = []
			for option in range(0, 4):
				self.layer_options_positions.append((position[0] + configFile.flaw_dropdown_menu_x_size / 2,
													 position[1] + (int((
																					configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * option) + configFile.flaw_dropdown_menu_y_size / (
																				2 * configFile.flaw_dropdown_menu_options_amount))))
			for flaw in flaw_list.keys():
				self.flaw_layer = flaw.flaw_type
			for option_name, option_position in zip(configFile.flaw_dropdown_layer_menu_options,
													self.layer_options_positions):
				if option_name == 'Niebieska':
					self.dropdown_layer_options_sprites.append(
						DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
										   configFile.b_layer_color, configFile.flaw_dropdown_menu_option_color, None,
										   self.flaw_layer))
				elif option_name == 'Zielona':
					self.dropdown_layer_options_sprites.append(
						DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
										   configFile.g_layer_color, configFile.flaw_dropdown_menu_option_color, None,
										   self.flaw_layer))
				elif option_name == 'Żółta':
					self.dropdown_layer_options_sprites.append(
						DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
										   configFile.y_layer_color, configFile.flaw_dropdown_menu_option_color, None,
										   self.flaw_layer))
				elif option_name == 'Czerwona':
					self.dropdown_layer_options_sprites.append(
						DropdownMenuOption(self.option_x_size, self.option_y_size, option_position, option_name,
										   configFile.r_layer_color, configFile.flaw_dropdown_menu_option_color, None,
										   self.flaw_layer))
			self.dropdown_layer_options_grouped_sprites = pygame.sprite.Group([*self.dropdown_layer_options_sprites])

	def delete_option_func (self):
		for flaw in self.clicked_flaws.keys():
			if flaw.flaw_type == 'hole':
				flaw_index = self.h_layer_flaw_center_list.index(flaw.position)
				del self.h_layer_flaw_center_list[flaw_index]
				del self.displayed_h_layer_items[flaw_index]
				del self.displayed_h_layer_flaws[flaw_index]
			elif flaw.flaw_type == 'blue':
				flaw_index = self.b_layer_flaw_center_list.index(flaw.position)
				del self.b_layer_flaw_center_list[flaw_index]
				del self.displayed_b_layer_items[flaw_index]
				del self.displayed_b_layer_flaws[flaw_index]
			elif flaw.flaw_type == 'green':
				flaw_index = self.g_layer_flaw_center_list.index(flaw.position)
				del self.g_layer_flaw_center_list[flaw_index]
				del self.displayed_g_layer_items[flaw_index]
				del self.displayed_g_layer_flaws[flaw_index]
			elif flaw.flaw_type == 'yellow':
				flaw_index = self.y_layer_flaw_center_list.index(flaw.position)
				del self.y_layer_flaw_center_list[flaw_index]
				del self.displayed_y_layer_items[flaw_index]
				del self.displayed_y_layer_flaws[flaw_index]
			elif flaw.flaw_type == 'red':
				flaw_index = self.r_layer_flaw_center_list.index(flaw.position)
				del self.r_layer_flaw_center_list[flaw_index]
				del self.displayed_r_layer_items[flaw_index]
				del self.displayed_r_layer_flaws[flaw_index]

	def blue_assignation_func (self):
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

	def green_assignation_func (self):
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

	def yellow_assignation_func (self):
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

	def red_assignation_func (self):
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

	def event_checker (self):
		if self.dropdown_layer_options_grouped_sprites != None:
			dropdown_layer_options_collide_list = pygame.sprite.groupcollide(
				self.dropdown_layer_options_grouped_sprites, self.cursor_sprite, False, False,
				collided=pygame.sprite.collide_mask)
			if self.dropdown_layer_option_on_hoover != None:
				for option in self.dropdown_layer_option_on_hoover:
					if option in dropdown_layer_options_collide_list:
						continue
					else:
						option.on_leave()
			self.dropdown_layer_option_on_hoover = dropdown_layer_options_collide_list
			for option in dropdown_layer_options_collide_list.keys():
				if pygame.mouse.get_pos()[0] >= option.position[0] - option.x_size / 2 and pygame.mouse.get_pos()[0] <= \
						option.position[0] + option.x_size / 2 and pygame.mouse.get_pos()[1] <= option.position[
					1] + option.y_size / 2 and pygame.mouse.get_pos()[1] >= option.position[1] - option.y_size / 2:
					option.on_hoover()
					self.choosed_layer_menu_option = option
				else:
					option.on_leave()
		if self.options_grouped_sprites != None:
			dropdown_collide_list = pygame.sprite.groupcollide(self.options_grouped_sprites, self.cursor_sprite, False,
															   False, collided=pygame.sprite.collide_mask)
			if self.dropdown_option_on_hoover != None:
				for option in self.dropdown_option_on_hoover:
					if option in dropdown_collide_list:
						continue
					else:
						if option.on_leave() == 'Warstwa' and self.dropdown_layer_menu_bg != None:
							if pygame.mouse.get_pos()[0] >= self.dropdown_layer_menu_bg[0] and pygame.mouse.get_pos()[
								1] >= self.dropdown_layer_menu_bg[1] and pygame.mouse.get_pos()[0] <= \
									self.dropdown_layer_menu_bg[0] + self.dropdown_layer_menu_bg[2] and \
									pygame.mouse.get_pos()[1] <= self.dropdown_layer_menu_bg[1] + \
									self.dropdown_layer_menu_bg[3]:
								pass
							else:
								self.dropdown_layer_options_grouped_sprites = None
						else:
							option.on_leave()
			self.dropdown_option_on_hoover = dropdown_collide_list
			for option in dropdown_collide_list.keys():
				if pygame.mouse.get_pos()[0] >= option.position[0] - option.x_size / 2 and pygame.mouse.get_pos()[0] <= \
						option.position[0] + option.x_size / 2 and pygame.mouse.get_pos()[1] <= option.position[
					1] + option.y_size / 2 and pygame.mouse.get_pos()[1] >= option.position[1] - option.y_size / 2:
					if option.on_hoover() == 'Warstwa':
						self.layer_choose_menu(self.clicked_flaws, (
						option.position[0] + option.x_size / 2, option.position[1] - option.y_size / 2))
					self.choosed_menu_option = option
				else:
					if option.on_leave() == 'Warstwa' and self.dropdown_layer_menu_bg != None:

						if pygame.mouse.get_pos()[0] >= self.dropdown_layer_menu_bg[0] and pygame.mouse.get_pos()[1] >= \
								self.dropdown_layer_menu_bg[1] and pygame.mouse.get_pos()[0] <= \
								self.dropdown_layer_menu_bg[0] + self.dropdown_layer_menu_bg[2] and \
								pygame.mouse.get_pos()[1] <= self.dropdown_layer_menu_bg[1] + \
								self.dropdown_layer_menu_bg[3]:
							pass
						else:
							self.dropdown_layer_options_grouped_sprites = None
					else:
						option.on_leave()
		if self.flaw_grouped_sprites != None and self.dropdown_menu_flag == False:
			collide_list = pygame.sprite.groupcollide(self.flaw_grouped_sprites, self.cursor_sprite, False, False,
													  collided=pygame.sprite.collide_mask)
			if self.clicked_flaws != None:
				# tu dodawac co ma sie dziac po kliknieciu
				some_flaws = collide_list
				some_flaws.update(self.clicked_flaws)
				self.change_flaw_color(some_flaws)
			else:
				self.change_flaw_color(collide_list)
		for event in pygame.event.get():
			if event.type == pygame.MOUSEWHEEL:
				if event.y == 1 and self.edit_mode == False and self.drawing_mode == False and self.drawing_flaw_started == False and self.assignation_flaw_mode == False and self.assignation_flaw_mode_started == False:
					self.zoom_in(False)
				elif event.y != 1 and self.edit_mode == False and self.drawing_mode == False and self.drawing_flaw_started == False and self.assignation_flaw_mode == False and self.assignation_flaw_mode_started == False:
					self.zoom_out(False, True)
			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == 1 and self.assignation_flaw_mode == True:
					self.assignation_flaw_mode_started = True
				if event.button == 1 and self.displayed_c_layer_items != None and self.edit_mode == False and self.drawing_mode == False and self.drawing_flaw_started == False and self.assignation_flaw_mode == False and self.assignation_flaw_mode_started == False:
					if self.dropdown_menu_flag == True:
						self.dropdown_menu_flag = False
					if self.choosed_menu_option != None and self.dropdown_option_on_hoover != None and self.choosed_menu_option in self.dropdown_option_on_hoover.keys() and self.clicked_flaws != None:
						self.choosed_menu_option.on_click(self.clicked_flaws)
						print('clicked flaws 1', self.clicked_flaws)
						if self.choosed_menu_option.text == 'Usuń' and len(self.clicked_flaws) == 1:
							self.delete_option_func()
						elif self.choosed_menu_option.text == 'Przesuń' and len(self.clicked_flaws) == 1:
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
							self.edit_mode = True
						self.choosed_menu_option = None
					if self.choosed_menu_option != None and self.dropdown_option_on_hoover != None and self.choosed_menu_option in self.dropdown_option_on_hoover.keys() and self.clicked_flaws == None:
						if self.choosed_menu_option.text == 'Rysuj skaze':
							print('Rysuj skaze prev')
							self.choosed_menu_option.on_click()
							self.drawing_mode = True
							self.choosed_menu_option = None
					if self.choosed_layer_menu_option != None and self.dropdown_layer_option_on_hoover != None and self.choosed_layer_menu_option in self.dropdown_layer_option_on_hoover.keys():
						self.choosed_layer_menu_option.on_click(self.clicked_flaws)
						print('clicked flaws 2', self.clicked_flaws)
						if self.choosed_menu_option.text == 'Usuń' and len(self.clicked_flaws) == 1:
							self.delete_option_func()
						elif self.choosed_menu_option.text == 'Przesuń' and len(self.clicked_flaws) == 1:
							for flaw in self.clicked_flaws.keys():
								self.editted_flaw = flaw
							self.edit_mode = True
						if self.choosed_layer_menu_option.text == 'Niebieska':
							self.blue_assignation_func()
						elif self.choosed_layer_menu_option.text == 'Zielona':
							self.green_assignation_func()
						elif self.choosed_layer_menu_option.text == 'Żółta':
							self.yellow_assignation_func()
						elif self.choosed_layer_menu_option.text == 'Czerwona':
							self.red_assignation_func()
						self.choosed_layer_menu_option = None
					collide_list = pygame.sprite.groupcollide(self.flaw_grouped_sprites, self.cursor_sprite, False,
															  False, collided=pygame.sprite.collide_mask)
					if str(collide_list) != '{}':
						self.clicked_flaws = collide_list
						self.layerinfo_update(self.clicked_flaws)
					else:
						self.clicked_flaws = None
						self.layerinfo_update(self.clicked_flaws)
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
							self.editted_flaw_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'blue':
						self.editted_flaw_index = self.b_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_b_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'green':
						self.editted_flaw_index = self.g_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_g_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'yellow':
						self.editted_flaw_index = self.y_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_y_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
					elif self.editted_flaw.flaw_type == 'red':
						self.editted_flaw_index = self.r_layer_flaw_center_list.index(self.editted_flaw.position)
						for point in self.displayed_r_layer_items[self.editted_flaw_index]:
							self.editted_flaw_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
				elif event.button == 1 and self.drawing_mode == True:
					# rysowanie nowej skazy
					self.drawing_flaw_started = True
				elif event.button == 3 and self.displayed_c_layer_items != None:
					self.leather_draging = False
					collide_list = pygame.sprite.groupcollide(self.flaw_grouped_sprites, self.cursor_sprite, False,
															  False, collided=pygame.sprite.collide_mask)
					if self.clicked_flaws != None and len(self.clicked_flaws) == 1:
						print('option 2')
						self.flaw_dropdown_menu()
						self.updating_shapes = True
						break
					if str(collide_list) == '{}' and self.clicked_flaws == None or self.clicked_flaws == 0 and str(
							collide_list) == '{}':
						print('option 3')
						self.dropdown_menu()
						self.clicked_flaws = None
						self.layerinfo_update(self.clicked_flaws)
						self.updating_shapes = True

			elif event.type == pygame.MOUSEMOTION:
				sh, sw = self.winfo_reqheight(), self.winfo_reqwidth()
				if pygame.mouse.get_focused():
					mouse_x, mouse_y = pygame.mouse.get_pos()
					mou_x = mouse_x / sw
					mou_y = mouse_y / sh
					self.queue.put(['main_mouse_move', [mou_x, mou_y]])
				if self.leather_draging and self.edit_mode == False and self.drawing_mode == False and self.drawing_flaw_started == False and self.assignation_flaw_mode == False and self.assignation_flaw_mode_started == False:
					mouse_x, mouse_y = event.pos
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
				elif self.edit_mode == True and self.editted_flaw != None and self.editted_flaw_offset != None and str(
						self.editted_flaw_offset) != '[]':
					sh, sw = self.winfo_reqheight(), self.winfo_reqwidth()
					mouse_pos = pygame.mouse.get_pos()
					if self.editted_flaw_start_position == None:
						self.editted_flaw_start_position = self.editted_flaw.position
					if self.editted_flaw.flaw_type == 'hole':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_h_layer_items[self.editted_flaw_index],
												 self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw,
								 (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_h_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'blue':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_b_layer_items[self.editted_flaw_index],
												 self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw,
								 (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_b_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'green':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_g_layer_items[self.editted_flaw_index],
												 self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw,
								 (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_g_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'yellow':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_y_layer_items[self.editted_flaw_index],
												 self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw,
								 (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_y_layer_items[self.editted_flaw_index] = item_list
					if self.editted_flaw.flaw_type == 'red':
						item_list = []
						diff_list = []
						for point, offset in zip(self.displayed_r_layer_items[self.editted_flaw_index],
												 self.editted_flaw_offset):
							item_list.append([(offset[0] + mouse_pos[0]), offset[1] + mouse_pos[1]])
							diff_list.append(
								[(point[0] - (offset[0] + mouse_pos[0])) / sw,
								 (point[1] - (offset[1] + mouse_pos[1])) / sh])
						self.displayed_r_layer_items[self.editted_flaw_index] = item_list
					self.updating_shapes = True
			# jeszcze diff
			# self.editted_flaw.update_position([self.editted_flaw_offset[0] + mouse_pos[0], self.editted_flaw_offset[1] + mouse_pos[1]])

			elif event.type == pygame.MOUSEBUTTONUP:
				if event.button == 1:
					if self.assignation_flaw_mode == True:
						self.assignation_flaw_mode = False
					if self.assignation_flaw_mode_started == True:
						flaw_type = self.flaw_type_assignation_func(self.assignation_flaw_points)
						if flaw_type == 'blue':
							self.flaw_sprites = []
							self.displayed_b_layer_items.append(self.temp_drawed_flaw)
							self.lowest_x = self.temp_drawed_flaw[0][0]
							self.highest_x = self.temp_drawed_flaw[0][0]
							self.lowest_y = self.temp_drawed_flaw[0][1]
							self.highest_y = self.temp_drawed_flaw[0][1]
							for point in self.temp_drawed_flaw:
								if point[0] > self.highest_x:
									self.highest_x = point[0]
								if point[0] < self.lowest_x:
									self.lowest_x = point[0]
								if point[1] < self.lowest_y:
									self.lowest_y = point[1]
								if point[1] > self.highest_y:
									self.highest_y = point[1]
							flaw_center = [self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
										   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)]
							self.b_layer_flaw_center_list.append(flaw_center)
							self.displayed_b_layer_flaws.append(
								FlawSprite(self.temp_drawed_flaw, configFile.b_layer_color, flaw_center, 'blue'))
							self.flaw_sprites.append(self.displayed_h_layer_items)
							self.flaw_sprites.append(self.displayed_b_layer_flaws)
							self.flaw_sprites.append(self.displayed_g_layer_flaws)
							self.flaw_sprites.append(self.displayed_y_layer_flaws)
							self.flaw_sprites.append(self.displayed_r_layer_flaws)
							print('blue blue')
						elif flaw_type == 'green':
							self.flaw_sprites = []
							self.displayed_g_layer_items.append(self.temp_drawed_flaw)
							self.lowest_x = self.temp_drawed_flaw[0][0]
							self.highest_x = self.temp_drawed_flaw[0][0]
							self.lowest_y = self.temp_drawed_flaw[0][1]
							self.highest_y = self.temp_drawed_flaw[0][1]
							for point in self.temp_drawed_flaw:
								if point[0] > self.highest_x:
									self.highest_x = point[0]
								if point[0] < self.lowest_x:
									self.lowest_x = point[0]
								if point[1] < self.lowest_y:
									self.lowest_y = point[1]
								if point[1] > self.highest_y:
									self.highest_y = point[1]
							flaw_center = [self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
										   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)]
							self.g_layer_flaw_center_list.append(flaw_center)
							self.displayed_g_layer_flaws.append(
								FlawSprite(self.temp_drawed_flaw, configFile.b_layer_color, flaw_center, 'green'))
							self.flaw_sprites.append(self.displayed_h_layer_items)
							self.flaw_sprites.append(self.displayed_b_layer_flaws)
							self.flaw_sprites.append(self.displayed_g_layer_flaws)
							self.flaw_sprites.append(self.displayed_y_layer_flaws)
							self.flaw_sprites.append(self.displayed_r_layer_flaws)
						elif flaw_type == 'yellow':
							self.flaw_sprites = []
							self.displayed_y_layer_items.append(self.temp_drawed_flaw)
							self.lowest_x = self.temp_drawed_flaw[0][0]
							self.highest_x = self.temp_drawed_flaw[0][0]
							self.lowest_y = self.temp_drawed_flaw[0][1]
							self.highest_y = self.temp_drawed_flaw[0][1]
							for point in self.temp_drawed_flaw:
								if point[0] > self.highest_x:
									self.highest_x = point[0]
								if point[0] < self.lowest_x:
									self.lowest_x = point[0]
								if point[1] < self.lowest_y:
									self.lowest_y = point[1]
								if point[1] > self.highest_y:
									self.highest_y = point[1]
							flaw_center = [self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
										   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)]
							self.y_layer_flaw_center_list.append(flaw_center)
							self.displayed_y_layer_flaws.append(
								FlawSprite(self.temp_drawed_flaw, configFile.b_layer_color, flaw_center, 'yellow'))
							self.flaw_sprites.append(self.displayed_h_layer_items)
							self.flaw_sprites.append(self.displayed_b_layer_flaws)
							self.flaw_sprites.append(self.displayed_g_layer_flaws)
							self.flaw_sprites.append(self.displayed_y_layer_flaws)
							self.flaw_sprites.append(self.displayed_r_layer_flaws)
						elif flaw_type == 'red':
							self.flaw_sprites = []
							self.displayed_r_layer_items.append(self.temp_drawed_flaw)
							self.lowest_x = self.temp_drawed_flaw[0][0]
							self.highest_x = self.temp_drawed_flaw[0][0]
							self.lowest_y = self.temp_drawed_flaw[0][1]
							self.highest_y = self.temp_drawed_flaw[0][1]
							for point in self.temp_drawed_flaw:
								if point[0] > self.highest_x:
									self.highest_x = point[0]
								if point[0] < self.lowest_x:
									self.lowest_x = point[0]
								if point[1] < self.lowest_y:
									self.lowest_y = point[1]
								if point[1] > self.highest_y:
									self.highest_y = point[1]
							flaw_center = [self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
										   self.lowest_y + ((self.highest_y - self.lowest_y) / 2)]
							self.r_layer_flaw_center_list.append(flaw_center)
							self.displayed_r_layer_flaws.append(
								FlawSprite(self.temp_drawed_flaw, configFile.b_layer_color, flaw_center, 'red'))
							self.flaw_sprites.append(self.displayed_h_layer_items)
							self.flaw_sprites.append(self.displayed_b_layer_flaws)
							self.flaw_sprites.append(self.displayed_g_layer_flaws)
							self.flaw_sprites.append(self.displayed_y_layer_flaws)
							self.flaw_sprites.append(self.displayed_r_layer_flaws)

						self.all_sprites = pygame.sprite.Group([*self.flaw_sprites, self.cursor_sprite])
						self.flaw_grouped_sprites = pygame.sprite.Group([*self.flaw_sprites])

						self.updating_shapes = True
						self.assignation_flaw_mode_started = False
						self.assignation_flaw_points = []
						self.assignation_flaw_mode = False
						self.temp_drawed_flaw = None
					if self.edit_mode == True and self.editted_flaw_start_position != None:
						self.editted_flaw_start_position = None
						self.edit_mode = False
						self.editted_flaw_offset = None
					# self.editted_flaw = None

					if self.drawing_flaw_started == True and len(self.drawing_flaw_points) >= 2:
						self.drawing_mode = False
						self.drawing_flaw_started = False
						self.temp_drawed_flaw = self.drawing_flaw_points
						self.drawing_flaw_points = []
						self.assignation_flaw_mode = True
					self.leather_draging = False
					self.c_layer_items_offset = []
					self.h_layer_items_offset = []
					self.b_layer_items_offset = []
					self.g_layer_items_offset = []
					self.y_layer_items_offset = []
					self.r_layer_items_offset = []

	def layerinfo_update (self, clicked_flaws):
		print('clicked_flaws', clicked_flaws)
		flaw_id_list = []
		flaw_list = []
		flaw_type_list = []
		flaw_position_list = []
		if clicked_flaws != None:
			for flaw_key, flaw_value in clicked_flaws.items():
				iter = 0
				for list in self.flaw_sprites:
					for item in list:
						iter += 1
						if flaw_key == item:
							flaw_id_list.append(iter)
				flaw_list.append([flaw_key, flaw_value])
				flaw_type_list.append(flaw_key.flaw_type)
				flaw_position_list.append(flaw_key.position)
		self.parent.parent.layer_info.clicked_flaws_update(None, None, None, None)
		self.parent.parent.layer_info.clicked_flaws_update(flaw_id_list, flaw_list, flaw_type_list, flaw_position_list)

	def flaw_type_assignation_func (self, point_list):
		a_point = point_list[0]
		b_point = point_list[-1]
		dol = (a_point[0] - b_point[0])
		if dol == 0:
			dol = 0.001
		wspol_kier = (a_point[1] - b_point[1]) / dol
		print('espol kier', wspol_kier)
		if wspol_kier <= -1 and a_point[1] > b_point[1] or wspol_kier >= 1 and a_point[1] > b_point[1]:
			playsound('sounds\Q2.wav', False)
			return 'green'
		elif wspol_kier <= 1 and wspol_kier >= -1 and a_point[0] < b_point[0]:
			playsound('sounds\Q1.wav', False)
			return 'blue'
		elif wspol_kier <= 1 and wspol_kier >= -1 and a_point[0] > b_point[0]:
			playsound('sounds\Q3.wav', False)
			return 'yellow'
		elif wspol_kier <= 1 and a_point[1] < b_point[1] or wspol_kier >= -1 and a_point[1] < b_point[1]:
			playsound('sounds\Q4.wav', False)
			return 'red'

	def flaw_dropdown_menu (self):
		if self.dropdown_menu_flag == False:
			self.mouse_pos = pygame.mouse.get_pos()
			self.dropdown_menu_bg = [self.mouse_pos[0], self.mouse_pos[1], configFile.flaw_dropdown_menu_x_size,
									 configFile.flaw_dropdown_menu_y_size]
			self.dropdown_options_sprites = []
			self.option_border = int(
				(configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * 0.1)
			self.option_x_size = int(configFile.flaw_dropdown_menu_x_size - 2 * self.option_border)
			self.option_y_size = int((configFile.flaw_dropdown_menu_y_size - (self.option_border * (
						configFile.flaw_dropdown_menu_options_amount + 1))) / configFile.flaw_dropdown_menu_options_amount)
			self.options_positions = []
			for option in range(0, configFile.flaw_dropdown_menu_options_amount):
				self.options_positions.append((self.mouse_pos[0] + configFile.flaw_dropdown_menu_x_size / 2,
											   self.mouse_pos[1] + (int((
																					configFile.flaw_dropdown_menu_y_size / configFile.flaw_dropdown_menu_options_amount) * option) + configFile.flaw_dropdown_menu_y_size / (
																				2 * configFile.flaw_dropdown_menu_options_amount))))
			for option_name, position in zip(configFile.flaw_dropdown_menu_options, self.options_positions):
				self.dropdown_options_sprites.append(
					DropdownMenuOption(self.option_x_size, self.option_y_size, position, option_name,
									   configFile.flaw_dropdown_menu_font_color,
									   configFile.flaw_dropdown_menu_option_color))
			self.options_grouped_sprites = pygame.sprite.Group([*self.dropdown_options_sprites])
			self.dropdown_menu_flag = True

	def dropdown_menu (self):
		if self.dropdown_menu_flag == False:
			self.mouse_pos = pygame.mouse.get_pos()
			self.dropdown_menu_bg = [self.mouse_pos[0], self.mouse_pos[1], configFile.dropdown_menu_x_size,
									 configFile.dropdown_menu_y_size]
			self.dropdown_options_sprites = []
			self.option_border = int((configFile.dropdown_menu_y_size / configFile.dropdown_menu_options_amount) * 0.1)
			self.option_x_size = int(configFile.dropdown_menu_x_size - 2 * self.option_border)
			self.option_y_size = int((configFile.dropdown_menu_y_size - (self.option_border * (
						configFile.dropdown_menu_options_amount + 1))) / configFile.dropdown_menu_options_amount)
			self.options_positions = []
			for option in range(0, configFile.dropdown_menu_options_amount):
				self.options_positions.append((self.mouse_pos[0] + configFile.dropdown_menu_x_size / 2,
											   self.mouse_pos[1] + (int((
																					configFile.dropdown_menu_y_size / configFile.dropdown_menu_options_amount) * option) + configFile.dropdown_menu_y_size / (
																			2 * configFile.dropdown_menu_options_amount))))
			for option_name, position in zip(configFile.dropdown_menu_options, self.options_positions):
				self.dropdown_options_sprites.append(
					DropdownMenuOption(self.option_x_size, self.option_y_size, position, option_name,
									   configFile.dropdown_menu_font_color, configFile.dropdown_menu_option_color))
			self.options_grouped_sprites = pygame.sprite.Group([*self.dropdown_options_sprites])
			self.dropdown_menu_flag = True

	def clicked_flaw_editor (self, new_clicked_flaws):
		self.reset_flaws_colors(new_clicked_flaws)
		self.clicked_flaws = new_clicked_flaws

	def reset_flaws_colors (self, flaws_to_Skip=[None, None]):
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

	def dragging_income (self, dragging_changes):
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

	def calculate_rotation (self):
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

	def calculate_center (self):
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
			self.text_layer_items_pos_offset.append(
				[(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])

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
			new_text_layer_items.append(
				[round((offset[0] + screen_center[0]), 1), round(offset[1] + screen_center[1], 1)])
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

	def update_shapes (self):
		self.screen.fill(configFile.bg_layer_color)
		self.calculate_flaws_center()

		if self.c_layer_items != None:
			pygame.draw.lines(self.screen, configFile.c_layer_color, True, self.displayed_c_layer_items)
		if self.displayed_h_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_h_layer_flaws, self.displayed_h_layer_items,
													  self.h_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_b_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_b_layer_flaws, self.displayed_b_layer_items,
													  self.b_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_g_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_g_layer_flaws, self.displayed_g_layer_items,
													  self.g_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_y_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_y_layer_flaws, self.displayed_y_layer_items,
													  self.y_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)
		if self.displayed_r_layer_flaws != None:
			for flaw, flaw_points, flaw_center in zip(self.displayed_r_layer_flaws, self.displayed_r_layer_items,
													  self.r_layer_flaw_center_list):
				flaw.update_flaw(flaw_points, flaw_center)

		if self.all_sprites != None:
			self.all_sprites.update()
			self.all_sprites.draw(self.screen)

		pygame.display.flip()