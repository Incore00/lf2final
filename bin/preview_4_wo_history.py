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

        self.positioning_window = LeatherWindow_preview_sprites(self, self.queue, height=self.sh, width=self.sw)
        self.positioning_window.pack(side="top", fill="both", expand=True)

class CursorSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
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
    def update(self):
        self.image.fill(0)
        pygame.draw.polygon(self.image, self.color, self.new_item)
        self.mask = pygame.mask.from_surface(self.image)
    def change_color (self, color):
        self.color = color

class LeatherWindow_preview_sprites(tk.Frame):
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
        #self.main_surface = pygame.Surface(window_size)

        self.drawing_sprites_flag = False
        self.max_flag = False

        self.red = 255

        item1 = [[100,100], [200,100], [200, 200], [100, 200]]
        item2 = [[300,300], [400,300], [400, 400], [300, 400]]
        cursor_image = pygame.image.load('cursor.png').convert_alpha()

        self.sprite1 = FlawSprite(item1, (0, 0, 255), (150,150))
        self.sprite2 = FlawSprite(item2, (0, 255, 0), (350, 350))
        self.sprite3 = CursorSprite(0, 0, cursor_image)

        self.all_sprites = pygame.sprite.Group([self.sprite1, self.sprite2, self.sprite3])

        self.pygame_loop()

    def pygame_loop(self):
        self.draw_sprites()

        self.event_checker()

        self.after(1, self.pygame_loop)

    def event_checker(self):
        if pygame.sprite.collide_mask(self.sprite3, self.sprite1):
            print('collision!')
            if self.max_flag != True:
                self.red = min(255, self.red + 10)
            else:
                self.red = max(0, self.red - 10)
            if self.red == 255:
                self.max_flag = True
            elif self.red == 0:
                self.max_flag = False

        self.sprite1.change_color((0, 0, self.red))
        if pygame.sprite.collide_mask(self.sprite3, self.sprite2):
            if self.max_flag != True:
                self.red = min(255, self.red + 10)
            else:
                self.red = max(0, self.red - 10)
            if self.red == 255:
                self.max_flag = True
            elif self.red == 0:
                self.max_flag = False

        self.sprite2.change_color((0, self.red, 0))
    def draw_sprites(self):
        self.all_sprites.update()
        self.screen.fill((0, 0, 0))
        self.all_sprites.draw(self.screen)
        pygame.display.flip()




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
        self.h_layer_items = None
        self.b_layer_items = None
        self.g_layer_items = None
        self.y_layer_items = None
        self.r_layer_items = None

        self.displayed_c_layer_items = None
        self.displayed_h_layer_items = None
        self.displayed_b_layer_items = None
        self.displayed_g_layer_items = None
        self.displayed_y_layer_items = None
        self.displayed_r_layer_items = None

        self.hole_flaw_center_list = []
        self.blue_flaw_center_list = []
        self.green_flaw_center_list = []
        self.yellow_flaw_center_list = []
        self.red_flaw_center_list = []

        self.c_layer_items_offset = []
        self.h_layer_items_offset = []
        self.b_layer_items_offset = []
        self.g_layer_items_offset = []
        self.y_layer_items_offset = []
        self.r_layer_items_offset = []

        self.leather_center = None
        self.zoom_tick = 0.99

        self.drawing_shapes = False
        self.leather_draging = False
        self.sprites_created = False
        self.destroy_flag = False

        print('I am alive')

        self.pygame_loop()

    def pygame_loop (self):
        self.screen.blit(self.main_surface, (0, 0))
        pygame.display.flip()

        if self.parent.parent.leather_tools.edit_slider.get() == 1:
            self.sprites_created = True

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

        if self.drawing_shapes == True:
            self.draw_shapes()
            self.drawing_shapes = False

        self.event_checker()

        #print('edit slider:', self.parent.parent.leather_tools.edit_slider.get()) zwraca 0 lub 1 jesli przesuniety

        if self.parent.parent.leather_tools.edit_slider.get() == 1 and self.destroy_flag == False:
            self.destroy_flag = True
            self.calculate_flaws_center()
            print('destroy and go flaws_to_sprites')
            self.parent.flaws_to_sprites(self.hole_flaw_center_list, self.blue_flaw_center_list,
                                         self.green_flaw_center_list, self.yellow_flaw_center_list,
                                         self.red_flaw_center_list, self.displayed_c_layer_items,
                                         self.displayed_h_layer_items, self.displayed_b_layer_items,
                                         self.displayed_g_layer_items, self.displayed_y_layer_items,
                                         self.displayed_r_layer_items)
            pass

        self.update()
        self.after(1, self.pygame_loop)

    def calculate_flaws_center(self):
        self.hole_flaw_center_list = []
        self.blue_flaw_center_list = []
        self.green_flaw_center_list = []
        self.yellow_flaw_center_list = []
        self.red_flaw_center_list = []

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
                self.hole_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
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
                self.blue_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
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
                self.green_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
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
                self.yellow_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
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
                self.red_flaw_center_list.append([self.lowest_x + ((self.highest_x - self.lowest_x) / 2),
                                       self.lowest_y + ((self.highest_y - self.lowest_y) / 2)])
    def load_data (self, leather):
        self.c_layer_items = leather[0]
        self.h_layer_items = leather[1]
        self.b_layer_items = leather[2]
        self.g_layer_items = leather[3]
        self.y_layer_items = leather[4]
        self.r_layer_items = leather[5]

        self.calculate_rotation()
        self.calculate_center()
        self.calculate_position()
        self.calculate_zoom()
        self.drawing_shapes = True
        print('preview data loaded')

    def event_checker (self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    self.zoom_in(False)
                elif event.y != 1:
                    self.zoom_out(False, True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.leather_draging = True
                    mouse_x, mouse_y = event.pos
                    for point in self.displayed_c_layer_items:
                        self.c_layer_items_offset.append([(point[0] - mouse_x), point[1] - mouse_y])
                    for item in self.displayed_h_layer_items:
                        offset_list = []
                        for point in item:
                            offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
                        self.h_layer_items_offset.append(offset_list)
                    for item in self.displayed_b_layer_items:
                        offset_list = []
                        for point in item:
                            offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
                        self.b_layer_items_offset.append(offset_list)
                    for item in self.displayed_g_layer_items:
                        offset_list = []
                        for point in item:
                            offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
                        self.g_layer_items_offset.append(offset_list)
                    for item in self.displayed_y_layer_items:
                        offset_list = []
                        for point in item:
                            offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
                        self.y_layer_items_offset.append(offset_list)
                    for item in self.displayed_r_layer_items:
                        offset_list = []
                        for point in item:
                            offset_list.append([(point[0] - mouse_x), point[1] - mouse_y])
                        self.r_layer_items_offset.append(offset_list)

            elif event.type == pygame.MOUSEMOTION:
                if self.leather_draging:
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
                    for point, offset in zip(self.displayed_c_layer_items, self.c_layer_items_offset):
                        new_c_layer_items.append([(offset[0] + mouse_x), (offset[1] + mouse_y)])
                        self.temp_drag_diff_c_layer_items.append(
                            [(point[0] - (offset[0] + mouse_x)) / sw, (point[1] - (offset[1] + mouse_y)) / sh])
                    self.displayed_c_layer_items = new_c_layer_items
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

                    dragging_changes = [self.temp_drag_diff_c_layer_items, self.temp_drag_diff_h_layer_items,
                                        self.temp_drag_diff_b_layer_items, self.temp_drag_diff_g_layer_items,
                                        self.temp_drag_diff_y_layer_items, self.temp_drag_diff_r_layer_items]
                    self.queue.put(['main_dragging', dragging_changes])
                    self.drawing_shapes = True

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.leather_draging = False
                    self.c_layer_items_offset = []
                    self.h_layer_items_offset = []
                    self.b_layer_items_offset = []
                    self.g_layer_items_offset = []
                    self.y_layer_items_offset = []
                    self.r_layer_items_offset = []

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


        self.drawing_shapes = True

    def calculate_rotation (self):
        new_c_layer_points = []
        new_h_layer_items = []
        new_b_layer_items = []
        new_g_layer_items = []
        new_y_layer_items = []
        new_r_layer_items = []
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

        new_c_layer_items = []
        new_h_layer_items = []
        new_b_layer_items = []
        new_g_layer_items = []
        new_y_layer_items = []
        new_r_layer_items = []

        sw, sh = self.winfo_reqwidth(), self.winfo_reqheight()
        screen_center = [sw / 2, sh / 2]

        for offset in self.c_layer_items_pos_offset:
            new_c_layer_items.append([round((offset[0] + screen_center[0]), 1), round((offset[1] + screen_center[1]), 1)])
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
        self.drawing_shapes = True

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

    def zoom_in (self, flag):
        if flag == False:
            self.queue.put(['main_zoom_in', True])
        center_point = [self.winfo_reqwidth() / 2, self.winfo_reqheight() / 2]
        new_layer = []
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
        self.drawing_shapes = True

    def zoom_out (self, queue_flag, drawing_flag):
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

        if drawing_flag == True:
            self.drawing_shapes = True

    def draw_shapes (self):
        self.main_surface.fill(configFile.bg_layer_color)
        # Draw shapes
        if self.c_layer_items != None:
            pygame.draw.lines(self.main_surface, configFile.c_layer_color, True, self.displayed_c_layer_items)
        if self.h_layer_items != None:
            for item in self.displayed_h_layer_items:
                pygame.draw.lines(self.main_surface, configFile.h_layer_color, True, item)
        if self.g_layer_items != None:
            for item in self.displayed_g_layer_items:
                if configFile.g_layer_linetype == "lines":
                    pygame.draw.lines(self.main_surface, configFile.g_layer_color, True, item)
                elif configFile.g_layer_linetype == "polygon":
                    pygame.draw.polygon(self.main_surface, configFile.g_layer_color, item)
        if self.b_layer_items != None:
            for item in self.displayed_b_layer_items:
                if configFile.b_layer_linetype == "lines":
                    pygame.draw.lines(self.main_surface, configFile.b_layer_color, True, item)
                elif configFile.b_layer_linetype == "polygon":
                    pygame.draw.polygon(self.main_surface, configFile.b_layer_color, item)
        if self.y_layer_items != None:
            for item in self.displayed_y_layer_items:
                if configFile.y_layer_linetype == "lines":
                    pygame.draw.lines(self.main_surface, configFile.y_layer_color, True, item)
                elif configFile.y_layer_linetype == "polygon":
                    pygame.draw.polygon(self.main_surface, configFile.y_layer_color, item)
        if self.r_layer_items != None:
            for item in self.displayed_r_layer_items:
                if configFile.r_layer_linetype == "lines":
                    pygame.draw.lines(self.main_surface, configFile.r_layer_color, True, item)
                elif configFile.r_layer_linetype == "polygon":
                    pygame.draw.polygon(self.main_surface, configFile.r_layer_color, item)
