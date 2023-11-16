import math
import pygame


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class Line(pygame.sprite.Sprite):
    def __init__(self, item, color, position):
        super().__init__()
        self.item = item
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

        self.new_item = []

        for point in item:
            self.new_item.append([point[0]-self.lowest_x,point[1]-self.lowest_y])

        print('item',item)

        print('new item', self.new_item)

        self.color = color

        self.image = pygame.Surface((self.highest_x-self.lowest_x, self.highest_y-self.lowest_y))
        self.image.set_colorkey((0, 0, 0))
        print(position)
        self.rect = self.image.get_rect(center=position)
    def update(self):
        self.image.fill(0)
        pygame.draw.polygon(self.image, self.color, self.item)
        self.mask = pygame.mask.from_surface(self.image)
    def change_color(self, color):
        self.color = color




pygame.init()
window = pygame.display.set_mode((300, 300))
#pygame.mouse.set_visible(False)
window.fill((255, 0, 0))
clock = pygame.time.Clock()

item = [[1024.5, 780.4], [1020.5, 780.0], [1016.5, 779.6], [1009.5, 777.6], [1006.5, 776.4], [1001.5, 773.8000000000001],
        [998.5, 771.6], [995.5, 769.2], [993.5, 767.2], [991.5, 763.8000000000001], [988.5, 757.6], [987.5, 754.4],
        [987.5, 750.2], [987.5, 749.4], [989.5, 749.6], [989.5, 750.2], [989.5, 754.0], [990.5, 757.0],
        [993.5, 762.8000000000001], [995.5, 766.0], [997.5, 767.8000000000001], [999.5, 770.0], [1002.5, 772.0],
        [1006.5, 774.6], [1010.5, 775.8000000000001], [1016.5, 777.6], [1020.5, 778.2], [1024.5, 778.4], [1031.5, 778.4],
        [1039.5, 777.8000000000001], [1046.5, 775.6], [1049.5, 774.4], [1055.5, 772.0], [1058.5, 770.4], [1065.5, 765.2],
        [1069.5, 760.4], [1070.5, 758.4], [1072.5, 753.8000000000001], [1073.5, 751.4], [1073.5, 748.8000000000001],
        [1072.5, 746.4], [1071.5, 741.6], [1067.5, 736.0], [1066.5, 733.6], [1061.5, 728.6], [1056.5, 724.0],
        [1054.5, 721.8000000000001], [1051.5, 719.4], [1048.5, 717.4], [1042.5, 714.2], [1038.5, 712.6], [1035.5, 711.4],
        [1028.5, 709.6], [1025.5, 709.2], [1018.5, 708.8000000000001], [1009.5, 709.0], [1005.5, 709.6], [1002.5, 710.8000000000001],
        [1000.5, 711.6], [999.5, 710.0], [1001.5, 709.0], [1004.5, 707.8000000000001], [1009.5, 707.0], [1018.5, 706.8000000000001],
        [1025.5, 707.2], [1028.5, 707.6], [1035.5, 709.6], [1039.5, 710.8000000000001], [1043.5, 712.4], [1043.5, 712.4],
        [1049.5, 715.8000000000001], [1052.5, 717.8000000000001], [1055.5, 720.2], [1058.5, 722.4], [1063.5, 727.2], [1063.5, 727.2],
        [1063.5, 727.2], [1067.5, 732.2], [1069.5, 735.0], [1073.5, 740.8000000000001], [1074.5, 745.8000000000001],
        [1075.5, 748.8000000000001], [1075.5, 751.8000000000001], [1074.5, 754.4], [1072.5, 759.2], [1070.5, 761.6],
        [1066.5, 766.6], [1066.5, 766.6], [1066.5, 766.8000000000001], [1059.5, 772.0], [1059.5, 772.0], [1056.5, 773.8000000000001],
        [1056.5, 773.8000000000001], [1050.5, 776.2], [1047.5, 777.6], [1039.5, 779.8000000000001], [1031.5, 780.4], [1024.5, 780.4]]

position = (0,0)
sprite_image = pygame.image.load('cursor.png').convert_alpha()
moving_object = SpriteObject(0, 0, sprite_image)
line_object = Line(item, (255, 255, 0), position)
all_sprites = pygame.sprite.Group([moving_object, line_object])
red = 0
max_flag = False


run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    all_sprites.update()
    window.fill((0, 0, 0))

    if pygame.sprite.collide_mask(moving_object, line_object):
        if max_flag != True:
            red = min(255, red + 10)
        else:
            red = max(0, red - 10)
        if red == 255:
            max_flag = True
        elif red == 0:
            max_flag = False

    else:
        red = 0

    line_object.change_color((255-red, red, red))
    all_sprites.draw(window)
    pygame.display.flip()

pygame.quit()
exit()