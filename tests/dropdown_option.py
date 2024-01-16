class FlawDropdownMenu(pygame.sprite.Sprite):
	def __init__(self, flaw = None):
		super().__init__()
		self.flaw = flaw
		self.image = pygame.Surface((configFile.flaw_dropdown_menu_size, configFile.flaw_dropdown_menu_size))
		self.image.set_colorkey((0, 0, 0))
		self.rect = self.image.get_rect(center=(configFile.flaw_dropdown_menu_size/2, configFile.flaw_dropdown_menu_size/2))
		self.mask = pygame.mask.from_surface(self.image)
		self.option_border = int((configFile.flaw_dropdown_menu_size / configFile.flaw_dropdown_menu_options_amount) * 0.1)

		self.mouse_pos = pygame.mouse.get_pos()
		self.options_sprites = None
		self.options_positions = None
		self.option_x_size = int(configFile.flaw_dropdown_menu_size - 2 * self.option_border)
		self.option_y_size = int((configFile.flaw_dropdown_menu_size/5) - 2 * self.option_border)
		self.options_grouped_sprites = None
		self.create_options_flaws()

	def create_options_flaws(self):
		self.options_positions = []
		for option in range(0, configFile.flaw_dropdown_menu_options_amount):
			self.options_positions.append((configFile.flaw_dropdown_menu_size/2,(int((configFile.flaw_dropdown_menu_size / configFile.flaw_dropdown_menu_options_amount) * option)+configFile.flaw_dropdown_menu_size /  (2*configFile.flaw_dropdown_menu_options_amount))))
		self.options_sprites = []
		for option_name, position in zip(self.option_names, self.options_positions):
			self.options_sprites.append(FlawDropdownMenuOption(self.option_x_size, self.option_y_size, position, option_name))
		self.options_grouped_sprites = pygame.sprite.Group([*self.options_sprites])
	def update(self):
		pygame.draw.rect(self.image, configFile.flaw_dropdown_menu_color, self.rect, border_radius=0)
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.topleft = self.mouse_pos