import tkinter as tk
import os
import pygame
import pyglet
from bin import configFile

pyglet.font.add_file('fonts/OpenSans/OpenSans.ttf')

class Flaw(pygame.sprite.Sprite):
    def __init__(self, item, color, position):
        super().__init__()

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

        self.position = position

        self.new_item = []

        for point in item:
            self.new_item.append([point[0]-self.lowest_x,point[1]-self.lowest_y])

        self.color = color

        self.image = pygame.Surface((self.highest_x-self.lowest_x, self.highest_y-self.lowest_y))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=position)
    def update(self):
        self.image.fill(0)
        pygame.draw.polygon(self.image, self.color, self.new_item)
        self.mask = pygame.mask.from_surface(self.image)
    def change_color(self, color):
        self.color = color

class Leatherpreview(tk.Frame):
    def __init__ (self, parent, queue, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.queue = queue
        self.pack_propagate(0)
        self.grid_propagate(0)
        sw, sh = int(parent.winfo_reqwidth() * 0.817), int(parent.winfo_reqheight() * 0.817)
        print(sw, sh)
        self.configure(height=sh, width=sw)

        LeatherWindow_preview(self, queue, height=sh, width=sw).pack(side="top", fill="both", expand=True)

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
        self.screen = pygame.display.set_mode(window_size)
        self.main_surface = pygame.Surface(window_size)

        self.c_layer_items = None
        self.b_layer_items = None

        self.displayed_c_layer_items = None
        self.displayed_b_layer_items = None

        self.drawing_shapes = False

        self.leather_center = None

        self.kontur = None

        self.all_sprites = None

        self.pygame_loop()

    def pygame_loop (self):
        self.screen.blit(self.main_surface, (0, 0))
        pygame.display.flip()

        try:
            item = self.queue.get(0)
            if item[0] == 'preview_load_data':
                self.load_data(item[1])
            else:
                self.queue.put(item)
        except:
            pass

        if self.drawing_shapes == True:
            print('drawing True')
            self.draw_shapes()
            self.drawing_shapes = False

        self.update()
        self.after(1, self.pygame_loop)

    def load_data (self, leather):
        self.c_layer_items = leather[0]
        self.b_layer_items = leather[2]

        self.calculate_rotation()
        self.calculate_center()
        self.calculate_position()
        self.drawing_shapes = True
        print('preview data loaded')
    def calculate_rotation (self):
        new_c_layer_points = []
        new_b_layer_items = []

        for point in self.c_layer_items:
            new_c_layer_points.append([point[1], point[0]])
        self.displayed_c_layer_items = new_c_layer_points

        for item in self.b_layer_items:
            point_list = []
            for point in item:
                point_list.append([point[1], point[0]])
            new_b_layer_items.append(point_list)
        self.displayed_b_layer_items = new_b_layer_items

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
        self.b_layer_items_pos_offset = []

        for point in self.displayed_c_layer_items:
            self.c_layer_items_pos_offset.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])

        for item in self.displayed_b_layer_items:
            offset_list = []
            for point in item:
                offset_list.append([(point[0] - self.leather_center[0]), point[1] - self.leather_center[1]])
            self.b_layer_items_pos_offset.append(offset_list)

        new_c_layer_items = []
        new_b_layer_items = []

        sw, sh = self.winfo_reqwidth(), self.winfo_reqheight()
        screen_center = [sw / 2, sh / 2]

        for offset in self.c_layer_items_pos_offset:
            new_c_layer_items.append([offset[0] + screen_center[0], offset[1] + screen_center[1]])
        self.displayed_c_layer_items = new_c_layer_items

        for item, item_offset in zip(self.displayed_b_layer_items, self.b_layer_items_pos_offset):
            item_list = []
            for point, offset in zip(item, item_offset):
                item_list.append([(offset[0] + screen_center[0]), offset[1] + screen_center[1]])
            new_b_layer_items.append(item_list)
        self.displayed_b_layer_items = new_b_layer_items



    def draw_shapes (self):
        #self.main_surface.fill(configFile.bg_layer_color)
        self.sprite_list = []

        #if self.c_layer_items != None:
        #    self.sprite_list.append(Flaw(self.displayed_c_layer_items, configFile.c_layer_color))

        self.new_items = []
        self.new_half_items = []

        print('c_layer_amount', len(self.displayed_c_layer_items))

        for i in range(0, len(self.displayed_c_layer_items)):
            self.new_half_items.append(self.displayed_c_layer_items[i])

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
            position = (self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
                                self.lowest_y + ((self.highest_y - self.lowest_y) / 2))
            self.sprite_list.append(Flaw(item, configFile.b_layer_color, position))


        self.all_sprites = pygame.sprite.Group(self.sprite_list)
        self.all_sprites.update()
        self.all_sprites.draw(self.main_surface)

        for item in self.sprite_list:
            pygame.draw.circle(self.main_surface, (255, 0, 0), item.position, 10)

        print(self.sprite_list)

        print('prev draw')