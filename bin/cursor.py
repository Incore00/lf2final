import pygame
from bin import configFile

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

