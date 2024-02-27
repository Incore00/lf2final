import pygame
from bin import configFile

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
			pygame.draw.lines(self.image, self.color, True, self.new_item, configFile.flaw_line_width)
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

