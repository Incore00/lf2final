import pygame
from bin import configFile
from playsound import playsound
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
