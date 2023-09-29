


class Leather():
	class c_layer_point():
		def __init__ (self, x_coord, y_coord):
			self.x_coord = x_coord
			self.y_coord = y_coord

	class h_layer_item():
		class h_layer_item_point():
			def __init__ (self, x_coord, y_coord):
				self.x_coord = x_coord
				self.y_coord = y_coord
		def __init__ (self, item):
			self.point_list = []
			for point in item:
				self.point_list.append(self.h_layer_item_point(point[0], point[1]))

	class b_layer_item():
		class b_layer_item_point():
			def __init__ (self, x_coord, y_coord):
				self.x_coord = x_coord
				self.y_coord = y_coord
		def __init__ (self, item):
			self.point_list = []
			for point in item:
				self.point_list.append(self.b_layer_item_point(point[0], point[1]))

	class g_layer_item():
		class g_layer_item_point():
			def __init__ (self, x_coord, y_coord):
				self.x_coord = x_coord
				self.y_coord = y_coord
		def __init__ (self, item):
			self.point_list = []
			for point in item:
				self.point_list.append(self.g_layer_item_point(point[0], point[1]))

	class y_layer_item():
		class y_layer_item_point():
			def __init__ (self, x_coord, y_coord):
				self.x_coord = x_coord
				self.y_coord = y_coord
		def __init__ (self, item):
			self.point_list = []
			for point in item:
				self.point_list.append(self.y_layer_item_point(point[0], point[1]))

	class r_layer_item():
		class r_layer_item_point():
			def __init__ (self, x_coord, y_coord):
				self.x_coord = x_coord
				self.y_coord = y_coord
		def __init__ (self, item):
			self.point_list = []
			for point in item:
				self.point_list.append(self.r_layer_item_point(point[0], point[1]))

	def __init__ (self, c_layer_points, h_layer_items, b_layer_items, g_layer_items, y_layer_items, r_layer_items):
		self.c_layer_point_list = []
		self.h_layer_item_list = []
		self.b_layer_item_list = []
		self.g_layer_item_list = []
		self.y_layer_item_list = []
		self.r_layer_item_list = []

		self.c_layer_point_list_to_display = []
		self.h_layer_point_list_to_display = []
		self.b_layer_point_list_to_display = []
		self.g_layer_point_list_to_display = []
		self.y_layer_point_list_to_display = []
		self.r_layer_point_list_to_display = []

		for item in c_layer_points:
			self.c_layer_point_list.append(self.c_layer_point(item[0], item[1]))
		for item in h_layer_items:
			self.h_layer_item_list.append(self.h_layer_item(item))
		for item in b_layer_items:
			self.b_layer_item_list.append(self.b_layer_item(item))
		for item in g_layer_items:
			self.g_layer_item_list.append(self.g_layer_item(item))
		for item in y_layer_items:
			self.y_layer_item_list.append(self.y_layer_item(item))
		for item in r_layer_items:
			self.r_layer_item_list.append(self.r_layer_item(item))

		for point in self.c_layer_point_list:
			self.c_layer_point_list_to_display.append([int(point.y_coord/5), -1* int(point.x_coord)/5])
		for item in self.h_layer_item_list:
			item_list = []
			for point in item.point_list:
				item_list.append([int(point.y_coord/5), -1* int(point.x_coord)/5])
			self.h_layer_point_list_to_display.append(item_list)
		for item in self.b_layer_item_list:
			item_list = []
			for point in item.point_list:
				item_list.append([int(point.y_coord/5), -1* int(point.x_coord)/5])
			self.b_layer_point_list_to_display.append(item_list)
		for item in self.g_layer_item_list:
			item_list = []
			for point in item.point_list:
				item_list.append([int(point.y_coord/5), -1* int(point.x_coord)/5])
			self.g_layer_point_list_to_display.append(item_list)
		for item in self.y_layer_item_list:
			item_list = []
			for point in item.point_list:
				item_list.append([int(point.y_coord/5), -1* int(point.x_coord)/5])
			self.y_layer_point_list_to_display.append(item_list)
		for item in self.r_layer_item_list:
			item_list = []
			for point in item.point_list:
				item_list.append([int(point.y_coord/5), -1* int(point.x_coord)/5])
			self.r_layer_point_list_to_display.append(item_list)

